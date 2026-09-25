# 1. Configuration
cp .env.example .env
# Editer .env : renseigner la cle d'API du modele

# 2. Deposer les documents a indexer
cp -r /chemin/vers/vos/documents/* ./documents/

# 3. Demarrer la pile
cd docker && docker compose up -d --build

# 4. Attendre que tout soit en bonne sante
docker compose ps
# docurag-qdrant     running (healthy)
# docurag-api        running (healthy)   <- peut prendre 2-3 min
# docurag-interface  running

# 5. Premiere ingestion (complete)
curl -X POST http://localhost:8000/ingest \
     -H "Content-Type: application/json" \
     -d '{"tout_reconstruire": true}'

# Suivre l'avancement
docker compose logs -f api

# 6. Verifier
curl -X POST http://localhost:8000/query \
     -H "Content-Type: application/json" \
     -d '{"question": "Quelle est la politique de conges ?"}'

# 7. Interface : http://localhost:8501
#    Documentation de l'API : http://localhost:8000/docs

# --- Mises a jour ulterieures : incrementales ---
curl -X POST http://localhost:8000/ingest \
     -H "Content-Type: application/json" \
     -d '{"tout_reconstruire": false}'
