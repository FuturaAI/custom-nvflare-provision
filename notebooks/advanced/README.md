# Advanced Notebooks

Questa directory contiene i notebook e le risorse necessarie per l'inferenza sui modelli addestrati, sia con training federato standard che con crittografia omomorfica (HE).

## Struttura
```
advanced/
├── models/                      # Directory per i modelli addestrati
├── tenseal_context/            # Directory per contesti di crittografia
├── nvflare_inference.ipynb     # Inferenza standard
└── nvflare_inference_HE.ipynb  # Inferenza per modelli HE
```

## Notebooks Disponibili

### nvflare_inference.ipynb
- Inferenza su modelli addestrati con training federato standard
- Caricamento diretto dei modelli PyTorch
- Non richiede componenti di crittografia

### nvflare_inference_HE.ipynb
- Inferenza su modelli addestrati con crittografia omomorfica
- Richiede i contesti di crittografia appropriati
- Utilizza TenSEAL per la gestione dei modelli crittografati

## Directory di Supporto

### models/
- Contiene i modelli addestrati
- Supporta sia modelli standard che HE
- I modelli devono essere copiati qui dopo il training

### tenseal_context/
- Contiene i contesti necessari per la crittografia omomorfica
- Richiesto solo per l'inferenza HE
- Deve contenere i file di contesto appropriati per la decrittografia

## Utilizzo
1. Copiare il modello addestrato nella cartella `models/`
2. Per HE: assicurarsi che i contesti di crittografia siano in `tenseal_context/`
3. Eseguire il notebook appropriato in base al tipo di modello:
   - `nvflare_inference.ipynb` per modelli standard
   - `nvflare_inference_HE.ipynb` per modelli HE

## Note
- Entrambi i notebook testano fino a 1000 immagini per default
- I risultati includono predizioni per singola immagine e accuratezza globale
- Verificare sempre la corrispondenza tra il tipo di modello e il notebook utilizzato