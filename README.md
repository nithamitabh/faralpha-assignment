# FarAlpha Kubernetes Assignment  
**Author:** Amitabh  
**Date:** 29 Nov 2025  

This project demonstrates deployment of a **Python Flask application** connected to a **MongoDB database** inside a **Kubernetes cluster running on Minikube**.  
It includes:

- Flask app with GET/POST endpoints  
- MongoDB StatefulSet with authentication  
- Persistent storage (PV/PVC)  
- Kubernetes Services (ClusterIP + NodePort)  
- Horizontal Pod Autoscaler  
- DNS explanation  
- Resource limits & design choices  
- Autoscaling test results  

---

# 📁 Project Structure

```

faralpha-assignment/
│
├── flask-app/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
│
└── k8s/
├── flask-deployment.yaml
├── flask-service.yaml
├── mongodb-secret.yaml
├── mongodb-pv.yaml
├── mongodb-pvc.yaml
├── mongodb-statefulset.yaml
├── mongodb-service.yaml
└── hpa.yaml

````

---

# 🐳 Docker Build & Push Instructions

Build the image:

```bash
cd flask-app
docker build -t amitabhkr19/flask-mongo:v1 .
````

Push to Docker Hub:

```bash
docker push amitabhkr19/flask-mongo:v1
```
Docker Hub Repository:
- [Docker Hub Repo link](https://hub.docker.com/r/amitabhkr19/flask-mongo)


---

# ⚙️ Minikube Setup

Start Minikube:

```bash
minikube start --driver=docker --cpus=2 --memory=2500mb --disk-size=7g
```

Enable metrics server:

```bash
minikube addons enable metrics-server
```

Verify node:

```bash
kubectl get nodes
```

![Minikube Setup](screenshots/Screenshot%20from%202025-11-29%2004-45-00.png)

---

# 🍃 Deploy MongoDB (StatefulSet)

Apply all MongoDB YAMLs:

```bash
kubectl apply -f k8s/mongodb-secret.yaml
kubectl apply -f k8s/mongodb-pv.yaml
kubectl apply -f k8s/mongodb-pvc.yaml
kubectl apply -f k8s/mongodb-statefulset.yaml
kubectl apply -f k8s/mongodb-service.yaml
```

Check pods:

```bash
kubectl get pods
```

---

# 🚀 Deploy Flask App

```bash
kubectl apply -f k8s/flask-deployment.yaml
kubectl apply -f k8s/flask-service.yaml
```

Check:

```bash
kubectl get pods
kubectl get svc
```

![Flask Deployment](screenshots/Screenshot%20from%202025-11-29%2004-42-30.png)

---

# 🌐 Access the Flask Service

Get external URL:

```bash
minikube service flask-service
```

Example:

```
http://192.168.49.2:32000/
```

### Test GET `/`

```bash
curl http://192.168.49.2:32000/
```

### Test POST `/data`

```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"name":"amitabh"}' \
http://192.168.49.2:32000/data
```

### Test GET `/data`

```bash
curl http://192.168.49.2:32000/data
```

![API Testing](screenshots/Screenshot%20from%202025-11-29%2004-43-06.png)

---

# 📈 Horizontal Pod Autoscaler (HPA)

Apply HPA:

```bash
kubectl apply -f k8s/hpa.yaml
```

Check HPA:

```bash
kubectl get hpa
```


![HPA Status](screenshots/Screenshot%20from%202025-11-29%2004-45-23.png)

---

# 🔥 Autoscaling Test (CPU Based)

Start load generator:

```bash
kubectl run -i --tty load-generator --image=busybox --rm \
-- /bin/sh -c "while true; do wget -q -O- http://flask-service:5000/; done"
```

In another terminal:

```bash
kubectl get hpa -w
```

Watch scaling from 2 → 3 → 4 → 5 pods:

```bash
kubectl get pods -w
```

---

# 🧠 Kubernetes DNS Explanation

Inside Kubernetes, services are resolved automatically by **CoreDNS**.

Flask connects to MongoDB using:

```
mongodb-service.default.svc.cluster.local
```

Resolution flow:

```
Flask Pod → CoreDNS → Service → MongoDB Pod
```

No hardcoded IP needed → stable communication.

---

# 🧰 Resource Requests & Limits

Used in `flask-deployment.yaml`:

```yaml
resources:
  requests:
    cpu: "0.2"
    memory: "250Mi"
  limits:
    cpu: "0.5"
    memory: "500Mi"
```

### Why?

* **Requests**: guaranteed resources
* **Limits**: prevent resource abuse
* Ensures stability + efficient scheduling

---

# 🧩 Design Choices

✔ **StatefulSet for MongoDB** – stable identity, persistent storage
✔ **PVC/PV** – MongoDB data survives restarts
✔ **ClusterIP for MongoDB** – internal-only access
✔ **NodePort for Flask** – external access for testing
✔ **Secrets** – secure DB credentials
✔ **HPA** – automatic scaling based on CPU

---

# 🧪 Testing Scenarios (Cookie Points)

* POST + GET on `/data`
* Autoscaling with load generator
* Pod recreation after manual deletion
* MongoDB persistence after MongoDB pod restart
* Service reachability via DNS

---

# 🧹 Cleanup (Optional)

```bash
kubectl delete -f k8s/
minikube stop
```

---

# 🎉 Final Notes

All components required by the assignment are implemented:

✔ Flask API
✔ MongoDB StatefulSet
✔ PV/PVC
✔ Secrets
✔ Deployments
✔ Services
✔ Autoscaler
✔ DNS explained
✔ Resource limits
✔ Screenshots included


