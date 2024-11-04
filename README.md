# NVFlare Custom Provision
## Setup NVFlare

## Descrizione
Script di automazione per la creazione e configurazione di nuovi progetti NVFlare. Lo script gestisce automaticamente il processo di provisioning e la configurazione iniziale del progetto, inclusa la gestione della distribuzione dei dataset di immagini.

## Prerequisiti
- Python 3.x
- NVFlare installato
- File richiesti nella stessa cartella:
  - `project_builder.py`
  - `preconfig_project_folders.py`
  - `prebuild_images_split.py`
  - Directory `images` contenente le immagini da distribuire, le immagini devono essere divise in cartelle con il nome della label come         nell'esempio

## Come Utilizzare lo Script

### Sintassi Base
```bash
./launch_provision.sh <nome_progetto>
```

### Esempio Pratico
```bash
./launch_provision.sh progetto_ml
```

### Passaggi Eseguiti dallo Script
1. Crea un nuovo progetto con il nome specificato
2. Genera il file di configurazione `nvflare_project_config_<nome_progetto>.yml`
3. Esegue il provisioning NVFlare
4. Configura la struttura delle cartelle del progetto
5. Esegue lo split e la distribuzione delle immagini tra i siti

### Output Atteso
Lo script creerà:
- Una nuova directory del progetto
- File di configurazione necessari
- Struttura base delle cartelle per NVFlare
- Directory di immagini suddivise per ogni client

### Struttura delle Directory per le Immagini
```
workspace/
└── nome_progetto/
    └── prod_XX/
        ├── localhost/
        │   └── local/
        │       └── images/
        │           └── split_images/
        ├── site-1/
        │   └── local/
        │       └── images/
        │           └── split_images/
        └── site-2/
            └── local/
                └── images/
                    └── split_images/
```

## Gestione delle Risorse
Lo script configura automaticamente le risorse per ogni client:
- Aggiorna i file `resources.json` per ogni client
- Configura l'utilizzo della GPU (1 GPU per client)
- Gestisce l'allocazione della memoria GPU

## Note Importanti
- Eseguire lo script dalla directory dove sono presenti i file di supporto
- Il nome del progetto non deve contenere spazi
- Attendere il completamento di tutti i passaggi prima di utilizzare il progetto
- Verificare che la directory `images` sia presente prima dell'esecuzione

## Script di Avvio Multi-Server

### Descrizione
Script per l'avvio automatico sequenziale dei server NVFlare (localhost e siti client) con un intervallo di tempo prestabilito tra ogni avvio.

### Sintassi
```bash
./fl_start.sh <nome_progetto> <prod_directory>
```

### Parametri
- `nome_progetto`: Nome del progetto (es. "test1")
- `prod_directory`: Nome della directory prod (es. "prod_00")

### Esempio
```bash
./fl_start.sh test1 prod_00
```

### Sequenza di Esecuzione
1. Avvio del server localhost
2. Attesa di 7 secondi
3. Avvio di site-1
4. Attesa di 7 secondi
5. Avvio di site-2

### Gestione
- I timestamp vengono mostrati per ogni avvio
- I server vengono avviati in background

### Note
- Eseguire dalla directory root del progetto
- Richiede la struttura standard delle cartelle di NVFlare
- Verifica automaticamente l'esistenza delle directory necessarie

## Configurazione dei Job

### Job Builder Base

### Descrizione
Script Python per la configurazione automatica dei job di training federated. Gestisce la configurazione del server e dei client, impostando parametri di training e workflow di federated learning.

### Prerequisiti
- File di configurazione `config/job_builder_setup.json`
- Moduli personalizzati:
  - `pt.utils.data_splitter`
  - `pt.networks.nets`
  - `pt.learners.custom_learner`

### Utilizzo
```bash
python job_builder.py
```
Lo script chiederà interattivamente:
1. Il nome del progetto
2. La sottodirectory del progetto (es. 'prod_00')

### Input Richiesti
```
Insert the project name, must be the same name of a folder in the workspace:
> test1

Insert the project sub dir (e.g. 'prod_00'):
> prod_00
```

### Componenti Configurati
1. **Server**:
   - Data splitter personalizzato
   - Model persistor
   - Aggregator per i modelli
   - Model selector e locator
   - Workflow di Scatter and Gather
   - Cross-site model evaluation

2. **Client**:
   - Custom learner per training
   - Executor per task di training e validazione
   - Configurazione risorse GPU

### Output
- Genera i file di configurazione dei job nella directory:
  ```
  workspace/<nome_progetto>/<project_sub_dir>/admin@nvidia.com/transfer/jobs
  ```

### Parametri Principali
- `NUM_ROUNDS`: Numero di round di training
- `AGGREGATION_EPOCHS`: Epoche per aggregazione
- `min_clients`: Numero minimo di client richiesti
- Configurazione GPU per ogni client (1 GPU, 1GB memoria)

### Note sulla Configurazione
- I parametri di training sono configurabili nel file `job_builder_setup.json`
- La configurazione include setup per training distribuito e validazione cross-site
- Risorse GPU vengono allocate automaticamente per ogni client
- Il percorso di output dipende dalla sottodirectory specificata

### Job Builder con Crittografia Omomorfica (HE)
È disponibile una versione alternativa del job builder che implementa la crittografia omomorfica per una maggiore sicurezza durante il training federato.

```bash
python job_builder_HE.py
```

#### Caratteristiche HE
- Utilizza `HEModelShareableGenerator` per la generazione sicura dei modelli condivisi
- Implementa filtri di serializzazione specifici per HE
- Aggiunge componenti di crittografia/decrittografia per client e server
- Configura aggregatori specifici per HE (`HEInTimeAccumulateWeightedAggregator`)

#### Note Importanti per HE
- Richiede il file di configurazione `config/job_builder_HE_setup.json`
- Learning rate ridotto (0.0007) per stabilità con HE
- È necessario rimuovere alcune configurazioni da `config_fed_client.json`
- Prestazioni leggermente inferiori ma maggiore sicurezza dei dati

[... contenuto precedente fino alla sezione Script di Avvio Multi-Server ...]

## Console di Amministrazione NVFlare

### Descrizione
La console di amministrazione (admin console) è lo strumento principale per gestire e monitorare i server NVFlare, eseguire job e gestire lo shutdown dei componenti.

### Avvio Console Admin
```bash
./fl_admin.sh <nome_progetto> <prod_directory>
```

### Esempio
```bash
./fl_admin.sh test1 prod_00
```

### Comandi Principali Admin Console

#### Gestione Server e Client
```bash
# Verifica stato dei componenti
check all      # Controlla lo stato di tutti i componenti
check server   # Controlla lo stato del server
check client   # Controlla lo stato dei client

# Shutdown componenti
shutdown client site-1    # Shutdown del client site-1
shutdown client site-2    # Shutdown del client site-2
shutdown server          # Shutdown del server
```

#### Gestione Job
```bash
# Lista e gestione job
list_jobs             # Mostra tutti i job disponibili
submit_job job_name   # Sottomette un nuovo job
abort_job job_id      # Interrompe un job in esecuzione
```

### Ordine Corretto di Shutdown
1. Terminare prima i client:
   ```bash
   shutdown client site-1
   shutdown client site-2
   ```
2. Poi terminare il server:
   ```bash
   shutdown server
   ```
3. Attendere la conferma di shutdown per ogni componente

### Note Importanti
- Utilizzare **sempre** la console admin per lo shutdown dei componenti
- Lo shutdown manuale o forzato dei processi può lasciare il sistema in uno stato inconsistente
- Assicurarsi di seguire l'ordine corretto di shutdown (prima client, poi server)
- Verificare sempre lo stato dei componenti prima di eseguire operazioni critiche

## Notebooks per Training e Inference

### Descrizione
La directory `notebooks` nella root del progetto contiene Jupyter notebooks per l'esecuzione di training standalone e inference. Questi notebook sono utili per:
- Test preliminari del modello
- Verifica del training locale
- Esecuzione di inference
- Debug del pipeline di training

### Struttura Directory
```
notebooks/
├── datasets/                # Dove viene salvato lo split delle immagini
├── local_training.ipynb     # Training standalone con validazione integrata
├── model_checkpoints/       # Dove vengono salvati i best_models.pth
└── inference.ipynb          # Esecuzione inference
```

### Utilizzo dei Notebooks

1. **Training Locale (local_training.ipynb)**:
   - Permette di testare l'architettura del modello
   - Verifica il pipeline di training
   - Include fase di validazione integrata
   - Utile per debug preliminare
   - Permette di verificare le performance del modello

2. **Inference (inference.ipynb)**:
   - Esecuzione di predizioni su nuovi dati
   - Test del modello addestrato
   - Valutazione delle performance

### Note Importanti
- I notebooks utilizzano la stessa struttura dati del training federato
- Assicurarsi che l'ambiente Python abbia tutte le dipendenze necessarie
- Utili per verificare il corretto funzionamento prima del training federato
- Possono essere utilizzati per confrontare risultati locali e federati

## Struttura Moduli PyTorch (pt/)

### Descrizione
La directory `pt` contiene i componenti per l'implementazione del federated learning con PyTorch da utilizzare con NVFlare. La struttura presente è un esempio di riferimento che mostra come organizzare il codice dopo averlo testato nei notebook.

### Workflow di Sviluppo
1. Il codice viene inizialmente sviluppato e testato nei notebook (`notebooks/`)
2. Una volta validata l'implementazione nei notebook standalone
3. Si crea la struttura appropriata in `pt/` per l'integrazione con NVFlare
4. I componenti in `pt/` vengono utilizzati esclusivamente per il training federato

### Struttura e Funzionalità

#### 1. Utils (utils/)
Contiene gli strumenti per la gestione dei dati:
- **Gestione Dataset**: Implementazione di dataset personalizzati per il caricamento e la gestione delle immagini
- **Data Splitting**: Strumenti per la distribuzione dei dati tra i vari siti di training
- **Utility Generali**: Funzioni di supporto e costanti utilizzate nel progetto

#### 2. Networks (networks/)
Contiene le implementazioni delle reti neurali:
- Definizione dell'architettura della rete
- Configurazione dei layer
- Parametri del modello

#### 3. Learners (learners/)
Gestisce la logica di training:
- Implementazione del training loop
- Gestione della validazione
- Integrazione con NVFlare per il federated learning
- Configurazione dei parametri di training

### Note Importanti
- Il codice presente è un esempio di riferimento
- Lo sviluppo iniziale avviene nei notebook standalone
- I componenti in `pt/` sono specifici per NVFlare
- La struttura segue le convenzioni richieste da NVFlare

### ⚠️ Punti di Attenzione

#### 1. Configurazione dei Job
Quando si configurano i job (in `job_builder.py` o `job_builder_HE.py`), i nomi delle classi e i percorsi devono corrispondere esattamente alla struttura presente in `pt/`:

```python
# Questi import devono corrispondere alla struttura attuale
from pt.utils.data_splitter import CustomDataSplitter
from pt.networks.nets import CustomModel
from pt.learners.custom_learner import CustomLearner
```

#### 2. Trasformazioni Dataset
Le trasformazioni attuali nel codice sono specifiche per il dataset di esempio (immagini in scala di grigi):
```python
transforms_train = [
    transforms.Grayscale(num_output_channels=1),
    transforms.Resize((224, 224)),
    # altre trasformazioni specifiche per immagini in scala di grigi
]
```

⚠️ Queste trasformazioni **devono essere modificate** in base al proprio dataset:
- Adattare le dimensioni di resize
- Modificare il numero di canali (es. 3 per RGB)
- Aggiustare la normalizzazione in base alle statistiche del dataset
- Personalizzare le augmentation in base al tipo di dati
- Rimuovere trasformazioni non pertinenti