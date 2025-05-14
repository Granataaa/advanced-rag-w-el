from openai import OpenAI
from dotenv import load_dotenv
import requests
import os
import numpy as np
import json

load_dotenv()
key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
  organization=os.getenv("ORGANIZATION"),
  project=os.getenv("PROJECT"),
)

url = os.getenv("URL")

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {key}"
}

def normalize(vecs):
    return vecs / np.linalg.norm(vecs, axis=1, keepdims=True)

def AIRequest(mess):

    payload = {
        "model": "gpt-4o",
        "messages": mess,
        "temperature": 1.0
    }
    response = requests.post(url, json=payload, headers=headers)
    r = ""
    if response.status_code == 200:
        result = response.json()
        r = result['choices'][0]['message']['content']
    else:
        print(f"Errore: {response.status_code}, Dettagli: {response.text}")
    return r

def normRes(res):


    # Step 1: rimuovi blocco di codice markdown se presente
    res = res.strip("```").strip()

    # (opzionale) se ha un prefisso tipo "json\n", rimuovilo:
    if res.startswith("json"):
        res = res[4:].strip()

    clean_str = res.replace("\n", "").replace("\\", "").replace("chunk", "")

    final_data = json.loads(clean_str)

    return final_data

def CreateBenchmark(text, chunks):

    content = f""" devo creare un benchmark per il mio dense retrieval. Ti dò un testo {text} e la divisione di quel testo in chunk {chunks}, 
    tu crei una struttura di questo tipo:
    [
        "query": "Qual è la capitale della Francia?",
        "gold_answer": "sourceTesto-solonumIDdelchunk", # chunk corretto
        "relevant_docs": ["sourceTesto-chunkID", "sourceTesto-solonumIDdelchunk"],  # ID dei documenti rilevanti 
    ]
    e crei 4 query su quel testo sempre seguendo questo schema.
    1 domanda fattuale, 1 domanda che richiede sintesi, 1 domanda che richiede inferenza e 1 domanda vaga o mal posta (per testare robustezza)
    """

    mess = [
        {"role": "system", "content": "rispondi in formato json e non aggiungere altro."},
        {"role": "user", "content": content},
    ]
    
    res = AIRequest(mess)
    print(res)
    res = normRes(res)
    print(res)

    with open("benchmark.json", "a", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
        f.write("\n")  # Ensure each appended JSON object is on a new line



if __name__ == "__main__":

    folder = "datasetOnlyTextUni/onlyTextLessonsTurbo"
    file = "economia_applicata_clean_24_Lez006.txt"
    with open(f"{folder}/{file}", "r", encoding="utf-8") as f:
        text = f.read()

    with open("chunks_metadata3001.json", "r", encoding="utf-8") as f:
        chunks = json.load(f)
    
    filtered_chunks = [
        {"source": chunk["source"], "text": chunk["text"], "chunk_id": chunk["chunk_id"]}
        for chunk in chunks
        if chunk["source"] == file
    ]

    CreateBenchmark(text, filtered_chunks)