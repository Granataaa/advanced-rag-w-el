from rag_service import loading, query_rag
import json
import time

# Caricamento modello e benchmark
loading()
with open("../benchmark_revisited_1_fixed_corrected.json", "r", encoding="utf-8") as f:
    benchmark = json.load(f)

# Inizializzazione metriche
metrics = {
    "exact_match": 0,
    "recall": 0,
    "precision": 0,
    "mrr": 0,
    "total_queries": 0,  # Conta tutte le query
    "total_defined_queries": 0  # Conta solo le query con gold_answer definita
}

for item in benchmark:
    
    q = item["query"]
    gold_answer = item["gold_answer"]
    relevant_docs = set(item["relevant_docs"])  # Usa un set per confronti più veloci

    # Incrementa il conteggio delle query totali
    metrics["total_queries"] += 1

    # Exact Match (considera tutte le query, incluse quelle ambigue)
    retrieved_docs = []
    if gold_answer is None:
        if not retrieved_docs:  # Nessuna risposta attesa e nessuna risposta recuperata
            metrics["exact_match"] += 1
        continue  # Salta il calcolo di Recall, Precision e MRR per le domande ambigue

    # Incrementa il conteggio delle query con risposte definite
    metrics["total_defined_queries"] += 1

    # Recupera i top-10 risultati con il sistema RAG completo (dense + LLM)
    results = query_rag(q, 10, "true")["chunks"]

    # Ottieni i documenti filtrati dall'LLM
    retrieved_docs = [f"{res['source']}-{res['chunk_id']}" for res in results]

    # Exact Match (solo per query con gold_answer definita)
    if retrieved_docs and retrieved_docs[0] == gold_answer:
        metrics["exact_match"] += 1

    # Recall su tutti i documenti filtrati
    relevant_found = sum(1 for doc in retrieved_docs if doc in relevant_docs)
    metrics["recall"] += relevant_found / len(relevant_docs) if relevant_docs else 0

    # Precision su tutti i documenti filtrati
    metrics["precision"] += relevant_found / len(retrieved_docs) if retrieved_docs else 0

    # MRR (considera il primo documento rilevante tra tutti)
    for rank, doc in enumerate(retrieved_docs, start=1):
        if doc == gold_answer:
            metrics["mrr"] += 1 / rank
            break

    time.sleep(30)

# Normalizzazione delle metriche
metrics["exact_match"] /= metrics["total_queries"]  # Dividi per tutte le query
for key in ["recall", "precision", "mrr"]:
    metrics[key] /= metrics["total_defined_queries"]  # Dividi solo per le query con risposte definite

# Salvataggio risultati
with open("benchmark_rag_complete_results.json", "w", encoding="utf-8") as f:
    json.dump(metrics, f, indent=2)

# Stampa report
print("\n=== Risultati del Benchmark con RAG Completo ===")
print(f"Query totali: {metrics['total_queries']}")
print(f"Query con risposte definite: {metrics['total_defined_queries']}")
print(f"Exact Match (top-1): {metrics['exact_match']:.2%}")
print(f"Recall: {metrics['recall']:.2%}")
print(f"Precision: {metrics['precision']:.2%}")
print(f"MRR: {metrics['mrr']:.4f}")