# Codebase Genius - Deployment Guide

## Local Development Deployment

### Prerequisites

- Python 3.10+
- Git
- OpenAI API key or Google Gemini API key
- ~2GB disk space for dependencies

### Step 1: Clone Project

```bash
cd /path/to/workspace
git clone <repo-url>
cd CodebaseGenius
```

### Step 2: Backend Setup

#### Create Virtual Environment

```bash
# Windows
cd BE
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

#### Install Dependencies

```bash
pip install -r requirements.txt
pip install jac  # If not in requirements
```

#### Configure Environment

```bash
cp .env.example .env

# Edit .env with your keys
# OPENAI_API_KEY=sk_...
# or
# GEMINI_API_KEY=...
```

#### Validate Setup

```bash
# Check JAC installation
jac --version

# Test imports
python -c "import jac; import byllm; print('OK')"
```

#### Start Backend

```bash
jac serve main.jac
```

Expected output:
```
Loading main.jac...
JAC server running on http://localhost:8000
Ready to accept connections
Walkers available:
  - codebase_genius
  - analyze_files
  - generate_documentation
  - review_code
  - get_sessions
  - get_projects
```

### Step 3: Frontend Setup

#### Install Dependencies

```bash
# In new terminal
cd CodebaseGenius/FE
pip install -r requirements.txt
```

#### Start Streamlit

```bash
streamlit run app.py
```

Expected output:
```
Collecting usage statistics...

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

### Step 4: Verify Integration

1. Open http://localhost:8501
2. Go to **Repository Upload** tab
3. Paste test path (e.g., WasteTracker)
4. Click **Load Repository**
5. Go to **Code Analysis** tab
6. Run Structure Analysis
7. Should see progress bar → results

✅ If successful, local deployment complete!

## Docker Deployment

### Prerequisites

- Docker installed
- docker-compose (optional but recommended)

### Create Dockerfile for Backend

```dockerfile
# Dockerfile (in BE directory)
FROM python:3.10-slim

WORKDIR /app

# Install JAC
RUN pip install jac byllm jac-cloud

# Copy requirements and install
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application
COPY . .

# Copy .env (or set via docker-compose)
COPY .env .

EXPOSE 8000

CMD ["jac", "serve", "main.jac"]
```

### Create Dockerfile for Frontend

```dockerfile
# Dockerfile (in FE directory)
FROM python:3.10-slim

WORKDIR /app

RUN pip install streamlit requests python-dotenv

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501"]
```

### Docker Compose

Create `docker-compose.yml` in root:

```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./BE
      dockerfile: Dockerfile
    container_name: codebase-genius-backend
    ports:
      - "8000:8000"
    environment:
      OPENAI_API_KEY: ${OPENAI_API_KEY}
      GEMINI_API_KEY: ${GEMINI_API_KEY}
      MAX_FILES_TO_ANALYZE: 100
      MAX_FILE_SIZE_MB: 5
    volumes:
      - ./projects:/app/projects
    restart: unless-stopped

  frontend:
    build:
      context: ./FE
      dockerfile: Dockerfile
    container_name: codebase-genius-frontend
    ports:
      - "8501:8501"
    depends_on:
      - backend
    environment:
      BACKEND_URL: http://backend:8000
    volumes:
      - ./FE:/app
    restart: unless-stopped
```

### Deploy with Docker Compose

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Kubernetes Deployment

### Create ConfigMaps and Secrets

```bash
# ConfigMap for settings
kubectl create configmap codebase-genius-config \
  --from-literal=MAX_FILES_TO_ANALYZE=100 \
  --from-literal=MAX_FILE_SIZE_MB=5

# Secret for API keys
kubectl create secret generic codebase-genius-secrets \
  --from-literal=OPENAI_API_KEY=sk_... \
  --from-literal=GEMINI_API_KEY=...
```

### Backend Deployment

```yaml
# backend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: codebase-genius-backend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: codebase-genius-backend
  template:
    metadata:
      labels:
        app: codebase-genius-backend
    spec:
      containers:
      - name: backend
        image: codebase-genius-backend:latest
        ports:
        - containerPort: 8000
        envFrom:
        - configMapRef:
            name: codebase-genius-config
        - secretRef:
            name: codebase-genius-secrets
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "2000m"
        livenessProbe:
          httpGet:
            path: /walker/get_projects
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /walker/get_projects
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 10

---
apiVersion: v1
kind: Service
metadata:
  name: codebase-genius-backend
spec:
  selector:
    app: codebase-genius-backend
  ports:
  - port: 8000
    targetPort: 8000
  type: ClusterIP
```

### Frontend Deployment

```yaml
# frontend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: codebase-genius-frontend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: codebase-genius-frontend
  template:
    metadata:
      labels:
        app: codebase-genius-frontend
    spec:
      containers:
      - name: frontend
        image: codebase-genius-frontend:latest
        ports:
        - containerPort: 8501
        env:
        - name: BACKEND_URL
          value: "http://codebase-genius-backend:8000"
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "1000m"

---
apiVersion: v1
kind: Service
metadata:
  name: codebase-genius-frontend
spec:
  selector:
    app: codebase-genius-frontend
  ports:
  - port: 8501
    targetPort: 8501
  type: LoadBalancer
```

### Deploy to Kubernetes

```bash
# Create namespace
kubectl create namespace codebase-genius

# Create secrets in namespace
kubectl -n codebase-genius create secret generic codebase-genius-secrets \
  --from-literal=OPENAI_API_KEY=sk_...

# Deploy
kubectl apply -f backend-deployment.yaml -n codebase-genius
kubectl apply -f frontend-deployment.yaml -n codebase-genius

# Check status
kubectl -n codebase-genius get pods
kubectl -n codebase-genius get svc
```

## Cloud Deployment

### AWS Deployment (ECS/Fargate)

1. **Create ECR Repositories**

```bash
aws ecr create-repository --repository-name codebase-genius-backend
aws ecr create-repository --repository-name codebase-genius-frontend
```

2. **Build and Push Images**

```bash
# Build backend
docker build -t codebase-genius-backend:latest BE/
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <ACCOUNT>.dkr.ecr.us-east-1.amazonaws.com
docker tag codebase-genius-backend:latest <ACCOUNT>.dkr.ecr.us-east-1.amazonaws.com/codebase-genius-backend:latest
docker push <ACCOUNT>.dkr.ecr.us-east-1.amazonaws.com/codebase-genius-backend:latest

# Repeat for frontend
```

3. **Create ECS Task Definition and Service**

See AWS ECS documentation for detailed task definitions.

### Google Cloud Deployment (Cloud Run)

```bash
# Build backend
gcloud builds submit BE/ --tag gcr.io/PROJECT/codebase-genius-backend

# Deploy backend
gcloud run deploy codebase-genius-backend \
  --image gcr.io/PROJECT/codebase-genius-backend \
  --platform managed \
  --set-env-vars OPENAI_API_KEY=sk_... \
  --port 8000

# Repeat for frontend
```

## Production Best Practices

### 1. Environment Configuration

Use .env files with strong secrets management:

```bash
# Use AWS Secrets Manager, Azure Key Vault, etc.
# Never commit .env files
# Use separate .env.prod, .env.staging
```

### 2. Logging and Monitoring

Add logging to `main.jac`:

```jac
walker codebase_genius {
    has logger;
    
    can log_event(level: str, message: str) {
        print(f"[{level}] {message}");
    }
}
```

### 3. Rate Limiting

Implement rate limiting in frontend:

```python
# In app.py
from datetime import datetime, timedelta

if "last_request" not in st.session_state:
    st.session_state.last_request = datetime.now()

time_since_last = datetime.now() - st.session_state.last_request
if time_since_last < timedelta(seconds=1):
    st.warning("Please wait before next request")
    st.stop()

st.session_state.last_request = datetime.now()
```

### 4. Error Handling

Add try-catch blocks:

```python
# In app.py
try:
    response = requests.post(url, json=data, timeout=30)
    response.raise_for_status()
except requests.exceptions.Timeout:
    st.error("Backend request timed out")
except requests.exceptions.ConnectionError:
    st.error("Cannot connect to backend")
except Exception as e:
    st.error(f"Error: {str(e)}")
```

### 5. Security Headers

For production frontend, add headers:

```python
# In app.py
import streamlit as st

st.set_page_config(
    page_title="Codebase Genius",
    page_icon="🧠",
    layout="wide"
)

# Add custom headers in deployment (nginx/Caddy)
```

### 6. HTTPS/TLS

```nginx
# nginx configuration
server {
    listen 443 ssl;
    server_name yourdomain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:8501;
    }
    
    location /api {
        proxy_pass http://localhost:8000;
    }
}
```

### 7. Database Backup

JAC uses embedded Jarcdb. Backup the `.jac` database:

```bash
# Periodic backup
0 */6 * * * cp -r /path/to/jarcdb /backup/jarcdb_$(date +\%s)
```

### 8. Load Balancing

```yaml
# docker-compose.yml with load balancer
version: '3.8'
services:
  nginx:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - backend-1
      - backend-2
      - frontend
  
  backend-1:
    build: ./BE
    expose:
      - "8000"
  
  backend-2:
    build: ./BE
    expose:
      - "8000"
  
  frontend:
    build: ./FE
    expose:
      - "8501"
```

## Monitoring and Observability

### Health Checks

```bash
# Check backend
curl http://localhost:8000/walker/get_projects

# Check frontend
curl http://localhost:8501
```

### Logging

Capture logs from containers:

```bash
# Docker
docker logs -f codebase-genius-backend

# Kubernetes
kubectl logs -f deployment/codebase-genius-backend

# Docker Compose
docker-compose logs -f backend
```

### Metrics

Monitor:
- API response times
- File analysis duration
- Documentation generation time
- Error rates
- Memory usage

## Troubleshooting Deployment

### Backend won't start

```bash
# Check JAC installation
jac --version

# Check Python version
python --version  # Should be 3.10+

# Check imports
python -c "import jac; import byllm"

# Check port
netstat -an | grep 8000
```

### Frontend can't connect to backend

```bash
# Verify backend URL in app.py
BASE_URL = "http://localhost:8000"  # If local
BASE_URL = "http://backend:8000"    # If Docker
BASE_URL = "http://service-name:8000"  # If Kubernetes

# Test connection
curl http://backend:8000/walker/get_projects
```

### Out of memory

```bash
# Reduce MAX_FILES_TO_ANALYZE
# Increase container memory limits
# Add swap space
```

### Slow performance

```bash
# Check LLM API rate limits
# Add caching layer (Redis)
# Use faster model (gpt-3.5-turbo)
# Reduce file size limits
```

## Next Steps

1. ✅ Deploy locally
2. ✅ Test all features
3. 🐳 Containerize (Docker)
4. ☸️ Deploy to Kubernetes
5. ☁️ Deploy to cloud (AWS/GCP/Azure)
6. 📊 Add monitoring
7. 🔒 Secure with HTTPS
8. 🚀 Go to production!

---

**Ready for production? 🚀**
