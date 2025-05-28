# Istruzioni per l'utilizzo del progetto

## Prerequisiti
1. Avere Conda installato
2. Avere React e npm installati

## Configurazione iniziale

### 1. Configurare l'ambiente Conda
Importare l'environment.yml se su windows:
```bash
conda env create -f environment.yml
```
su altri sistemi invece importare:
```bash
conda env create -f environment_crossplatform.yml
```
> **Nota:** Prima di importare l'ambiente, assicurati di aver selezionato la versione corretta del CUDA Toolkit compatibile con la tua GPU e con i pacchetti richiesti dal progetto.
> Cambiare nel file .yml le righe con accanto il commento con la versione corretta.
> Puoi verificare la versione scaricata in questo modo:
> ```bash
> nvcc --version
> ```
> oppure
> ```bash
> nvidia-smi
> ```

### 2. Configurare le variabili d'ambiente
Creare un file .env nella root del progetto con le seguenti variabili per l'API di OpenAI:
```bash
OPENAI_API_KEY=your_api_key_here
ORGANIZATION=your_organization_here
PROJECT=your_project_here
URL=your_api_url_here
```
Moficare anche i file di configurazione:
1. config.json (nella directory principale)
 - con le specifiche del server e il path da cui prendere i video per lo speech-to-text
2. reactApi/react-client/public/config.json
 - con le specifiche del server

### 3. Preparare i file video
Scaricare i video e posizionarli in DUE cartelle:
```bash
reactApi/react-client/public/video/nomeCorso
```
e quella che hai messo nel config.json

## Elaborazione 
Se si vuole rifare lo speech-to-text e gli embeddings utilizzare questi script:
1. whisperXuniNet.ipynb: Speech-to-Text
2. extractionText.ipynb: Post-elaborazione testi (obbligatorio dopo Whisper)
3. denseR.ipynb: Generazione embeddings

## Avvio del progetto

### 1. Avviare il server API
```bash
cd rag_api
python server.py
```
Il server si avvierà sulla porta 5000 in locale.

### 2. Avviare il client React
```bash
cd reactApi/react-client
npm start
```
Il client si avvierà sulla porta 3000 in locale

## Documentazione API
La documentazione dell'API è disponibile all'indirizzo:
http://127.0.0.1:5000/ui

## Note finali
Se qualcosa non dovesse funzionare o se ho dimenticato qualche passaggio, sentitevi liberi di contattarmi o aprire una issue nel repository.