# Dockerfile
# Base image con Miniconda (e quindi Python) e supporto CUDA
# Scegli un'immagine base adatta: per CUDA 11.8 potresti cercare 'nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04' 
# e poi installare Conda, oppure usare un'immagine che abbia già Miniconda e CUDA.
# Per semplicità, useremo una base con Miniconda e assumeremo che le dipendenze Conda gestiranno il CUDA Toolkit corretto.
# Se hai problemi con CUDA, potremmo dover usare una base nvidia/cuda e installare Conda manualmente.
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# Imposta la directory di lavoro all'interno del container
WORKDIR /app

# 1. Configurare l'ambiente Conda
# Copia i file dell'ambiente Conda. 
# Decidi quale usare in base al sistema di build di Docker (di solito Linux).
# Se il tuo sistema di build è Linux, usa environment_crossplatform.yml
# Se hai bisogno di usare l'ambiente Windows, dovresti pensare a una strategia di build diversa o usare WSL/Linux per la build.
COPY environment_crossplatform.yml .

# Crea l'ambiente Conda.
# Aggiungi qui eventuali canali aggiuntivi necessari per i pacchetti specifici di CUDA/PyTorch.
# CONDA_OVERRIDE_CUDA: Questo è cruciale se l'ambiente Conda deve gestire le versioni CUDA.
# Tuttavia, l'approccio più robusto è assicurarsi che l'immagine base NVIDIA-CUDA sia compatibile.
# Se l'environment_crossplatform.yml ha dipendenze CUDA, assicurati che siano presenti anche i canali necessari.
RUN conda env create -f environment_crossplatform.yml && \
    echo "conda activate myenv" > ~/.bashrc && \
    /opt/conda/envs/myenv/bin/conda clean -afy

# Rendi l'ambiente Conda disponibile per le future istruzioni
ENV PATH /opt/conda/envs/myenv/bin:$PATH
ENV CONDA_DEFAULT_ENV myenv

# 2. Installare Node.js e npm (per React)
# Aggiungiamo un repository per Node.js per avere una versione più recente
RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - && \
    apt-get update && \
    apt-get install -y nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copia l'intero progetto nella directory di lavoro del container
COPY . .

# Installare le dipendenze di React
WORKDIR /app/reactApi/react-client
RUN npm install

# Costruire l'applicazione React per la produzione (opzionale, ma consigliato per deployment)
# RUN npm run build

# Torna alla directory root del progetto all'interno del container
WORKDIR /app

# Espone le porte che useranno il server API (5000) e il client React (3000)
EXPOSE 5000
EXPOSE 3000

# Nessun CMD qui, perché useremo docker-compose per avviare i servizi separatamente.