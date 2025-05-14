# Istruzioni per l'utilizzo del progetto

## Prerequisiti
1. Avere Conda installato
2. Avere React e npm installati

## Configurazione iniziale

### 1. Configurare l'ambiente Conda
Importare l'environment.yml:
```bash
conda env create -f environment.yml
```

### 2. Configurare le variabili d'ambiente
Creare un file .env nella root del progetto con le seguenti variabili per l'API di OpenAI:
```bash
OPENAI_API_KEY=your_api_key_here
ORGANIZATION=your_organization_here
PROJECT=your_project_here
URL=your_api_url_here
```

### 3. Preparare i file video
Scaricare i video e posizionarli nella cartella:
```bash
reactApi/react-client/public/video/nomeCorso
```

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

## File importanti
whisperXuniNet.ipynb: contiene lo script per lo speech-to-text (controllare dove mettere i video in modo da utilizzarlo)
denseR.ipynb: crea gli embeddings

## Note finali
Se qualcosa non dovesse funzionare o se ho dimenticato qualche passaggio, sentitevi liberi di contattarmi o aprire una issue nel repository.