# Currency Converter App

A simple currency converter application with:
- **Backend**: Flask REST API
- **Frontend**: Basic HTML/JS UI
- **Packaging**: Docker & Helm
- **Deployment**: Local Kubernetes cluster via Terraform + Kind
- **GitOps**: ArgoCD
- **CI/CD**: GitHub Actions (build, test, Docker push, Helm updates)

---

## 📦 Prerequisites

- [Python 3.11+](https://www.python.org/)
- [Docker](https://docs.docker.com/get-docker/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [Helm 3](https://helm.sh/docs/intro/install/)
- [Terraform](https://developer.hashicorp.com/terraform/downloads)
- [kind](https://kind.sigs.k8s.io/)
- [ArgoCD](https://argo-cd.readthedocs.io/en/stable/getting_started/)

---

## 🛠 Build, Test & Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/your-username/currency-converter-app.git
cd currency-converter-app
```

### 2. Create & activate virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r app/requirements.txt
```

### 4. Run tests
```bash
pytest --maxfail=1 --disable-warnings -q
flake8 app tests
```

### 5. Run the app locally
```bash
export FLASK_APP=app/main.py
flask run
```
App will be available at: [http://localhost:8080](http://localhost:8080)

---

## 🐳 Build & Run with Docker

### Build Docker image
```bash
docker build -t currency-converter:local .
```

### Run Docker container
```bash
docker run -p 8080:8080 currency-converter:local
```

---

## ☸ Install via Helm Chart

### 1. Package and install chart
```bash
helm install currency-converter helm/currency-converter/
```

### 2. Upgrade chart (after changes)
```bash
helm upgrade currency-converter helm/currency-converter/
```

### 3. Uninstall
```bash
helm uninstall currency-converter
```

---

## 🌱 Local Kubernetes Cluster with Terraform + Kind

### 1. Initialize Terraform
```bash
cd k8s-iac
terraform init
```

### 2. Apply cluster configuration
```bash
terraform apply -auto-approve
```

This will create a local Kind cluster and configure `kubectl`.

### 3. access k8s cluster using kubectl
```bash
export KUBECONFIG=./kubeconfig.yaml
kubectl get nodes
```

---

## 🚀 Setup ArgoCD

### 1. Install ArgoCD on local cluster
```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

### 2. Port forward ArgoCD UI
```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```
UI: [https://localhost:8080](https://localhost:8080)  
Default admin password:
```bash
kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath="{.data.password}" | base64 -d
```

### 3. Connect app repo
Create an ArgoCD application pointing to this repo’s `argoCD/argocd-app.yaml` chart.

---

## ⚡ CI/CD Pipeline (GitHub Actions)

- **develop branch**
  - Runs tests (pytest, flake8) on every push.
  - Builds & pushes Docker image → Docker Hub
  - Updates Helm chart (`Chart.yaml` and `values.yaml`) with new version & image tag and push back to develop branch
  - ArgoCD picks up changes and deploys automatically.
- **main branch (on PR merge)**
  - create and push git tags  

---

## 🧪 Run Tests

Local:
```bash
pytest
```

In CI/CD:  
Tests are automatically executed on push/PR via GitHub Actions.

---

## 🌐 Access the UI

### Locally
- Flask: [http://localhost:8080](http://localhost:8080)

### Docker
- [http://localhost:8080](http://localhost:8080)

### Kubernetes
- Port forward service:
  ```bash
  kubectl port-forward svc/currency-converter 8080:80
  ```
- Open: [http://localhost:8080](http://localhost:8080)

---

## 💱 How to Use the App

1. Enter an amount in the input field.  
2. Select source and target currency (USD, EUR, GBP, JPY).  
3. Click **Convert**.  
4. Result will be displayed instantly.

---
