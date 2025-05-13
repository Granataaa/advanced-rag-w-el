from rag_service import loading, query_rag
import json

# Caricamento del modello e del benchmark
loading()
with open("../benchmark.json", "r", encoding="utf-8") as f:
    bench = json.load(f)

# Inizializzazione delle metriche
metrics = {
    "exact_match": 0,
    "recall@1": 0,
    "recall@3": 0,
    "recall@5": 0,
    "precision@1": 0,
    "precision@3": 0,
    "precision@5": 0,
    "mrr": 0,
    "total_queries": len(bench)
}

for y in bench:
    q = y["query"]
    gold_answer = y["gold_answer"]
    
    # Recupera i top-3 risultati per calcolare recall@3/precision@3
    results = query_rag(q, 5, "false")["chunks"]
    
    # Estrai gli ID dei documenti recuperati (es. "doc-123")
    retrieved_docs = [f"{res['source']}-{res['chunk_id']}" for res in results]
    
    # Calcolo delle metriche
    # 1. Exact Match (primo risultato)
    metrics["exact_match"] += 1 if (retrieved_docs and retrieved_docs[0] == gold_answer) else 0
    
    # 2. Recall@k e Precision@k (k=1 e k=3)
    for k in [1, 3, 5]:
        relevant_found = sum(1 for doc in retrieved_docs[:k] if doc == gold_answer)
        metrics[f"recall@{k}"] += relevant_found / 1  # Assume 1 doc rilevante per query
        metrics[f"precision@{k}"] += relevant_found / k
    
    # 3. MRR (Mean Reciprocal Rank)
    for rank, doc in enumerate(retrieved_docs, start=1):
        if doc == gold_answer:
            metrics["mrr"] += 1 / rank
            break

# Normalizzazione delle metriche (media su tutte le query)
for key in metrics:
    if key != "total_queries":
        metrics[key] /= metrics["total_queries"]

# Salva i risultati in un file JSON
with open("benchmark_results.json", "w", encoding="utf-8") as f:
    json.dump(metrics, f, indent=2)

# Stampa il report
print("\n=== Risultati del Benchmark ===")
print(f"Query totali: {metrics['total_queries']}")
print(f"Exact Match (top-1): {metrics['exact_match']:.2%}")
print(f"Recall@1: {metrics['recall@1']:.2%}")
print(f"Recall@3: {metrics['recall@3']:.2%}")
print(f"Recall@5: {metrics['recall@5']:.2%}")
print(f"Precision@1: {metrics['precision@1']:.2%}")
print(f"Precision@3: {metrics['precision@3']:.2%}")
print(f"Precision@5: {metrics['precision@5']:.2%}")
print(f"MRR: {metrics['mrr']:.4f}")