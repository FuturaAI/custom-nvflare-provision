# Guida Step-by-Step

## 1. Sviluppo e Test Locale
**N.B. La parte di sviluppo e test non è necessaria per testare il federate con la struttura già presente**
### A. Test nel Notebook
```
notebooks/training/local_training.ipynb
```
- Sviluppa e testa l'architettura del modello
- Configura le trasformazioni del dataset
- Verifica il pipeline di training
- Valida le performance del modello
- Testa l'inferenza locale

### B. Adattamento alla Struttura NVFlare
Converti il codice testato nella struttura `pt/`:
```
pt/
├── learners/      # Implementa la logica di training e trasformazioni
├── networks/      # Porta l'architettura del modello
└── utils/         # Implementa dataset e data splitter
```
- Assicurati che i nomi delle classi corrispondano a quelli usati nei job builder
- Mantieni coerenti le trasformazioni del dataset
- Verifica che i path siano corretti

## 2. Setup Iniziale del Progetto
```bash
# Eseguire il setup del progetto
./launch_provision.sh <nome_progetto>
```

- Verifica che la directory `images` sia presente con la struttura corretta
- Controlla il completamento di tutte le operazioni di setup
- Verifica la creazione delle directory in workspace

## 3. Verifica delle Directory Generate
```
workspace/
└── nome_progetto/
    └── prod_00/
        ├── localhost/
        ├── site-1/
        └── site-2/
```
- Controlla che le immagini siano state correttamente distribuite
- Verifica la presenza dei file di configurazione

## 3. Avvio dei Server
```bash
# Avviare i server in ordine
./fl_start.sh <nome_progetto> prod_00
```
- Attendi il completamento dell'avvio di ogni server
- Verifica che tutti i server siano attivi

## 4. Accesso Admin Console
```bash
# Avviare la console di amministrazione
./fl_admin.sh <nome_progetto> prod_00
```
- Verifica la connessione di tutti i client con `check all`

## 5. Configurazione e Sottomissione Job
```bash
# Generare la configurazione del job
python job_builder.py        # Per training standard
# oppure
python job_builder_HE.py     # Per training con crittografia omomorfica

# Nella console admin
submit_job job_name
```

## 6. Monitoraggio Training
Nella console admin:
- Usa `check_status job_id` per monitorare il progresso
- Controlla i log per eventuali errori
- Monitora le metriche di training

## 7. Download e Validazione Risultati
```bash
# Nella console admin
download_job job_id
```
- I risultati saranno in `workspace/<nome_progetto>/prod_00/admin@nvidia.com/transfer`
- Utilizza i notebook in `notebooks/advanced/` per la validazione:
  - `nvflare_inference.ipynb` per modelli standard
  - `nvflare_inference_HE.ipynb` per modelli con HE

## 8. Chiusura Corretta
Nella console admin:
```bash
# Chiusura in ordine
shutdown client site-1
shutdown client site-2
shutdown server
```

## Note Importanti
- Segui l'ordine esatto degli step
- Verifica il completamento di ogni fase prima di procedere
- Controlla i log in caso di errori
- Backup dei risultati importanti prima della chiusura

## Troubleshooting
- Controlla `/tmp/nvflare/` per log dettagliati
- Verifica lo stato dei server con `check all`
- In caso di errori, riavvia i server in ordine
- Verifica i path nei file di configurazione

## Inferenza con NVFlare
Per i dettagli completi sulla fase di inferenza e validazione dei modelli addestrati, fare riferimento al README.md nella cartella `notebooks/advanced_nvflare/`:
- Struttura e utilizzo delle cartelle `models/` e `tenseal_context/`
- Differenze tra inferenza standard e HE
- Gestione dei path e dei contesti di crittografia
- Note importanti sulla validazione dei modelli

Per maggiori dettagli consultare:
```
notebooks/advanced_nvflare/README.md
```