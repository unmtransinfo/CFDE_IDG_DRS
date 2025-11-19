# Pharos FastAPI - CFDE Demo

A FastAPI service that connects to the Pharos GraphQL API to retrieve data about drug targets, diseases, and ligands.

## Lead Developers
- **Manjil Pradhan** - University of New Mexico
- **Praveen Kumar** - University of New Mexico

## Live Demo

**API Base URL:** https://qjempg3k6t.us-east-2.awsapprunner.com

**Interactive Documentation:** https://qjempg3k6t.us-east-2.awsapprunner.com/docs

## Running Locally

### Prerequisites
- Python 3.11 or higher
- pip

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/unmtransinfo/CFDE_IDG_DRS.git
   cd CFDE_IDG_DRS/Pharos_API
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create `.env` file**
   ```bash
   echo "PHAROS_API_URL=https://pharos-api.ncats.io/graphql" > .env
   ```

5. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

6. **Access the API**
   - API: http://localhost:8000
   - Interactive Docs: http://localhost:8000/docs

## Example Usage

1. Single Entity Queries

Get Target Information

# JSON format (default)
curl "https://qjempg3k6t.us-east-2.awsapprunner.com/targets/EGFR"

# CSV format
curl "https://qjempg3k6t.us-east-2.awsapprunner.com/targets/EGFR?format=csv"

# TSV format
curl "https://qjempg3k6t.us-east-2.awsapprunner.com/targets/EGFR?format=tsv"

Get Ligand Information

# JSON format
curl "https://qjempg3k6t.us-east-2.awsapprunner.com/ligands/aspirin"

# CSV format
curl "https://qjempg3k6t.us-east-2.awsapprunner.com/ligands/haloperidol?format=csv"

Get Disease Information

# By disease name
curl "https://qjempg3k6t.us-east-2.awsapprunner.com/diseases/asthma"

# By MONDO ID
curl "https://qjempg3k6t.us-east-2.awsapprunner.com/diseases/mondo/MONDO:0004979"

2. Cross-Relational Queries

Target → Diseases

Get all diseases associated with a specific target:
# JSON format
curl "https://qjempg3k6t.us-east-2.awsapprunner.com/targets/EGFR/diseases"

# CSV format (downloadable)
curl "https://qjempg3k6t.us-east-2.awsapprunner.com/targets/EGFR/diseases?format=csv" -o
egfr_diseases.csv

# Limit number of diseases
curl "https://qjempg3k6t.us-east-2.awsapprunner.com/targets/TP53/diseases?max_diseases=10"

Target → Ligands

Get all ligands (drugs/compounds) that target a specific protein:
# JSON format
curl "https://qjempg3k6t.us-east-2.awsapprunner.com/targets/EGFR/ligands"

# CSV format
curl "https://qjempg3k6t.us-east-2.awsapprunner.com/targets/EGFR/ligands?format=csv" -o
egfr_ligands.csv

# Limit results
curl "https://qjempg3k6t.us-east-2.awsapprunner.com/targets/BRAF/ligands?max_ligands=20"

Disease → Targets

Get all targets associated with a specific disease:
# JSON format
curl "https://qjempg3k6t.us-east-2.awsapprunner.com/diseases/asthma/targets"

# CSV format
curl "https://qjempg3k6t.us-east-2.awsapprunner.com/diseases/cancer/targets?format=csv" -o
cancer_targets.csv

Ligand → Targets

Get all targets for a specific ligand/drug:
# JSON format
curl "https://qjempg3k6t.us-east-2.awsapprunner.com/ligands/aspirin/targets"

# CSV format
curl "https://qjempg3k6t.us-east-2.awsapprunner.com/ligands/imatinib/targets?format=csv" -o
imatinib_targets.csv

3. Batch/Bulk Data Fetching

Batch Targets

Retrieve multiple targets in a single request:
# JSON format
curl -X POST "https://qjempg3k6t.us-east-2.awsapprunner.com/targets/batch" \
   -H "Content-Type: application/json" \
   -d '{
   "gene_symbols": ["EGFR", "TP53", "BRAF", "KRAS"],
   "format": "json"
   }'

# CSV format (save to file)
curl -X POST "https://qjempg3k6t.us-east-2.awsapprunner.com/targets/batch" \
   -H "Content-Type: application/json" \
   -d '{
   "gene_symbols": ["EGFR", "TP53", "BRAF", "KRAS", "ALK", "RET"],
   "format": "csv"
   }' -o targets_batch.csv

Batch Ligands

Retrieve multiple ligands in a single request:
# JSON format
curl -X POST "https://qjempg3k6t.us-east-2.awsapprunner.com/ligands/batch" \
   -H "Content-Type: application/json" \
   -d '{
   "ligand_ids": ["aspirin", "imatinib", "haloperidol"],
   "format": "json"
   }'

# CSV format
curl -X POST "https://qjempg3k6t.us-east-2.awsapprunner.com/ligands/batch" \
   -H "Content-Type: application/json" \
   -d '{
   "ligand_ids": ["aspirin", "metformin", "imatinib", "erlotinib"],
   "format": "csv"
   }' -o ligands_batch.csv

Batch Diseases

Retrieve multiple diseases in a single request:
# JSON format
curl -X POST "https://qjempg3k6t.us-east-2.awsapprunner.com/diseases/batch" \
   -H "Content-Type: application/json" \
   -d '{
   "disease_names": ["asthma", "diabetes", "cancer"],
   "format": "json"
   }'

# CSV format
curl -X POST "https://qjempg3k6t.us-east-2.awsapprunner.com/diseases/batch" \
   -H "Content-Type: application/json" \
   -d '{
   "disease_names": ["asthma", "diabetes", "cancer", "alzheimer disease"],
   "format": "csv"
   }' -o diseases_batch.csv

4. Search Functionality

Search Targets

# Search for kinase targets
curl "https://qjempg3k6t.us-east-2.awsapprunner.com/targets?search=kinase&limit=10"

# Search with pagination
curl "https://qjempg3k6t.us-east-2.awsapprunner.com/targets?search=receptor&skip=0&limit=20"

# Export search results as CSV
curl "https://qjempg3k6t.us-east-2.awsapprunner.com/targets?search=kinase&limit=50&format=csv" -o
kinase_targets.csv

Search Ligands

# Search for aspirin-related compounds
curl "https://qjempg3k6t.us-east-2.awsapprunner.com/ligands?search=aspirin&limit=10"

# Export search results
curl "https://qjempg3k6t.us-east-2.awsapprunner.com/ligands?search=inhibitor&limit=50&format=csv" -o
inhibitors.csv

Search Diseases

# Search for cancer-related diseases
curl "https://qjempg3k6t.us-east-2.awsapprunner.com/diseases?search=cancer&limit=10"

# Export search results
curl
"https://qjempg3k6t.us-east-2.awsapprunner.com/diseases?search=inflammatory&limit=50&format=csv" -o
inflammatory_diseases.csv

5. Health Check

# Check API health status
curl "https://qjempg3k6t.us-east-2.awsapprunner.com/health"

Docker Deployment

Build and run using Docker:
docker build -t pharos-api .
docker run -p 8000:8000 --env-file .env pharos-api

AWS ECR Deployment

Reauthenticate to ECR:
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin
166810338829.dkr.ecr.us-east-2.amazonaws.com

Rebuild the image:
docker build -t pharos-api .

Tag the image:
docker tag pharos-api:latest 166810338829.dkr.ecr.us-east-2.amazonaws.com/pharos-api:latest

Push the image:
docker push 166810338829.dkr.ecr.us-east-2.amazonaws.com/pharos-api:latest

API Endpoints Summary

| Endpoint                         | Method | Description                   |
|----------------------------------|--------|-------------------------------|
| /targets/{gene_symbol}           | GET    | Get target information        |
| /targets/{gene_symbol}/diseases  | GET    | Get diseases for target       |
| /targets/{gene_symbol}/ligands   | GET    | Get ligands for target        |
| /targets/batch                   | POST   | Batch fetch multiple targets  |
| /targets?search=term             | GET    | Search targets                |
| /ligands/{ligand_id}             | GET    | Get ligand information        |
| /ligands/{ligand_id}/targets     | GET    | Get targets for ligand        |
| /ligands/batch                   | POST   | Batch fetch multiple ligands  |
| /ligands?search=term             | GET    | Search ligands                |
| /diseases/{disease_name}         | GET    | Get disease information       |
| /diseases/{disease_name}/targets | GET    | Get targets for disease       |
| /diseases/batch                  | POST   | Batch fetch multiple diseases |
| /diseases?search=term            | GET    | Search diseases               |
| /health                          | GET    | Health check                  |

Galaxy Integration

All endpoints support Galaxy-compatible CSV/TSV output formats. Simply add ?format=csv or
?format=tsv to any endpoint URL.

Contributing

This project is part of the CFDE (Common Fund Data Ecosystem) IDG (Illuminating the Druggable
Genome) Data Resource Services initiative.






## Example Usage

**Get target data as JSON:**
```
http://localhost:8000/targets/EGFR
```

**Download as CSV:**
```
http://localhost:8000/targets/EGFR?format=csv
```

**Download as TSV:**
```
http://localhost:8000/targets/EGFR?format=tsv
```

## Docker Deployment

Build and run using Docker:
```bash
docker build -t pharos-api .
docker run -p 8000:8000 --env-file .env pharos-api
```

Reauthenticate to ECR
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 166810338829.dkr.ecr.us-east-2.amazonaws.com

Rebuild the image
docker build -t pharos-api .

Tag the image again
docker tag pharos-api:latest 166810338829.dkr.ecr.us-east-2.amazonaws.com/pharos-api:latest

Push the image
docker push 166810338829.dkr.ecr.us-east-2.amazonaws.com/pharos-api:latest
