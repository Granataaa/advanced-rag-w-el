-----

## Istruzioni per l'Utilizzo del Progetto con Docker

Questo documento descrive come avviare il progetto utilizzando Docker per un ambiente di esecuzione standardizzato e portabile.

### Prerequisiti

1.  **Docker Desktop** installato e configurato (con WSL 2 su Windows).
2.  Per l'accelerazione GPU, assicurati di avere i **driver NVIDIA** e il **runtime Docker** configurati correttamente.

-----

### 1\. Configurazione Iniziale

#### **Configurare le Variabili d'Ambiente**

Crea un file `.env` nella directory principale del progetto (es. `rag_api/.env`) con le seguenti variabili per l'API di OpenAI:

```ini
OPENAI_API_KEY=your_api_key_here
ORGANIZATION=your_organization_here
PROJECT=your_project_here
URL=your_api_url_here
```

#### **Configurare i File JSON**

Modifica i file di configurazione, assicurandoti che l'host del server sia impostato su **"0.0.0.0"** per consentire al container di accettare connessioni dall'esterno.

1.  **config.json** (nella directory principale):
    ```json
    {
      "server": {
        "host": "0.0.0.0",
        "port": 5005
      },
      "directoryVideo": {
        "path": "Insert/Path/Directory/With/All/The/Course"
      }
    }
    ```
2.  **react-client/public/config.json**:
    ```json
    {
      "api_base_url": "http://localhost:5005"
    }
    ```

> **Nota:** La mappatura delle porte di Docker gestirà la connessione tra `localhost:5005` (dal tuo browser) e `0.0.0.0:5005` (all'interno del container).

-----

### 2\. Preparazione dei File

#### **Posizionare i Video**

Assicurati che tutti i file video siano posizionati nella cartella specificata nel tuo `config.json` locale. Docker monterà questa directory all'interno del container per permettere al server di accedervi.

-----

### 3\. Build e Avvio del Container

#### **Costruire l'Immagine Docker**

Nella directory principale del progetto, esegui il seguente comando per costruire l'immagine Docker. Questo processo installerà tutte le dipendenze e preparerà l'ambiente.

```bash
docker build -t nome_immagine .
```

#### **Avviare il Container**

Dopo aver costruito l'immagine, avvia il container utilizzando il seguente comando. Questo comando mapperà le porte necessarie per il frontend e il backend e abiliterà l'accelerazione GPU.

```bash
docker run -it --rm \
-p 5005:5005 \
-p 3000:3000 \
--gpus all \
--env-file ./rag_api/.env \
nome_immagine
```

> **Spiegazione dei flag:**
>
>   * `-it`: Permette l'interazione con il terminale del container.
>   * `--rm`: Rimuove il container quando viene fermato.
>   * `-p 5005:5005`: Mappa la porta 5005 del tuo computer a quella del container per l'API.
>   * `-p 3000:3000`: Mappa la porta 3000 del tuo computer a quella del container per il client React.
>   * `--gpus all`: Abilita l'accesso a tutte le GPU disponibili.
>   * `--env-file ./rag_api/.env`: Carica le variabili d'ambiente dal file `.env`.

-----

### 4\. Esecuzione dei Servizi all'Interno del Container

Dopo aver avviato il container, avrai un terminale in esecuzione. Per avviare i servizi, devi aprire nuovi terminali e connetterti al container in esecuzione.

#### **Aprire nuovi terminali e connettersi al container**

Per ogni servizio, apri un nuovo terminale e usa il comando `docker exec` per entrare nel container. Puoi trovare il nome o l'ID del container con `docker ps`.

```bash
docker exec -it <CONTAINER_ID_O_NOME> bash
```

#### **Avviare il Server API**

Nel primo terminale connesso, avvia il server API:

```bash
cd rag_api
python server.py
```

#### **Avviare il Client React**

Nel secondo terminale connesso, avvia il client React:

```bash
cd reactApi/react-client
npm start
```

Ora il progetto è in esecuzione e accessibile tramite `http://localhost:3000` nel tuo browser.

-----

### Documentazione API

La documentazione dell'API è disponibile all'indirizzo:
`http://localhost:5005/ui`

-----

### Note Finali

Se incontri problemi di connessione (come `ERR_CONNECTION_REFUSED` o `ERR_EMPTY_RESPONSE`), verifica che le mappature delle porte in `docker run` corrispondano a quelle usate nel codice e che il tuo firewall non stia bloccando il traffico.


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