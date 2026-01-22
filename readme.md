# RAG Chatbot - Service Client (Dockerized)

Chatbot **RAG (Retrieval-Augmented Generation)** pour le service client, construit avec :

- **LangChain** - Framework pour applications LLM
- **ChromaDB** - Base de donnees vectorielle
- **Ollama** - Embeddings locaux (nomic-embed-text)
- **Google Gemini** - LLM (gemini-3-flash-preview)
- **Pandas** - Chargement des donnees Excel

Le chatbot repond aux questions en utilisant une base de connaissances chargee depuis un fichier Excel.

---

## Structure du Projet

```
.
├── main.py                         # Application principale
├── Modele_RAG_ServiceClient.xlsx   # Base de connaissances (FAQ service client)
├── chroma_db/                      # Base de donnees vectorielle persistante
├── Dockerfile                      # Image Docker de l'application
├── docker-compose.yml              # Orchestration des services
├── requirements.txt                # Dependances Python
└── readme.md
```

---

## Prerequis

- **Docker** et **Docker Compose**
- **Cle API Google** (pour Gemini)

### Verifier l'installation

```bash
docker --version
docker compose --version
```

---

## Lancement du Projet

### 1. Cloner le depot

```bash
git clone <url-du-repository>
cd chat-bot-RAG-Rugby--christian
```

### 2. Configurer la cle API Google

Creer un fichier `.env` a la racine du projet :

```bash
GOOGLE_API_KEY=votre_cle_api_google
```

### 3. Construire et demarrer les services

```bash
docker compose up --build
```

Cela demarre :
- **Ollama** (serveur d'embeddings sur le port 11434)

### 4. Telecharger le modele d'embeddings (premiere execution uniquement)

Dans un nouveau terminal :

```bash
docker exec -it ollama ollama pull nomic-embed-text
```

### 5. Acceder a l'application

Ouvrir dans le navigateur : **http://localhost:7860**

---

## Persistance des Donnees

Les donnees sont persistees via des volumes Docker :

| Volume | Contenu |
|--------|---------|
| `ollama_data` | Modeles Ollama |
| `chroma_data` | Base vectorielle ChromaDB |

Arreter ou redemarrer les conteneurs ne supprime pas les donnees.

---

## Arreter le Projet

Arreter les services :

```bash
docker compose down
```

Arreter et supprimer les volumes (supprime modeles et embeddings) :

```bash
docker compose down -v
```

---

## Technologies

| Technologie | Utilisation |
|-------------|-------------|
| Python 3.11 | Langage principal |
| LangChain | Framework RAG |
| ChromaDB | Stockage vectoriel |
| Ollama | Embeddings (nomic-embed-text) |
| Google Gemini | LLM (gemini-3-flash-preview) |
| Pandas/openpyxl | Lecture fichiers Excel |
| Docker | Conteneurisation |

---

## Notes

- Le fichier Excel `Modele_RAG_ServiceClient.xlsx` doit contenir les colonnes : `category`, `intent`, `question`, `answer`, `context`
- Le premier demarrage peut etre lent (telechargement des modeles)
