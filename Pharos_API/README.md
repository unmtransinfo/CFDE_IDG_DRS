# Pharos FastAPI - CFDE Demo

A FastAPI service that connects to the Pharos GraphQL API to retrieve data about drug targets, diseases, and ligands.

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
