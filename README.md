# FarAlpha Kubernetes Assignment**

### **Author: Amitabh**

---

#  **1. Overview**

This project demonstrates deploying a **Python Flask application** connected to a **MongoDB database** using **Kubernetes on Minikube**. It includes:

* Flask application with `/` and `/data` endpoints
* MongoDB StatefulSet with authentication
* Persistent storage using PV/PVC
* Internal ClusterIP service for MongoDB
* Horizontal Pod Autoscaler (HPA)
* Resource Requests & Limits
* DNS explanation inside Kubernetes
* Autoscaling test results
* Complete deployment instructions

---

#  **2. Project Structure**

```
faralpha-assignment/
│
├── flask-app/
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
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
```

---

# 🐳 **3. Docker Build & Push Instructions**

### Build the Docker image:

```bash
cd flask-app
docker build -t amitabhkr19/flask-mongo:v1 .
```

### Push to Docker Hub:

```bash
docker push amitabhkr19/flask-mongo:v1
```

---

# ⚙️ **4. Minikube Setup**

Start Minikube using Docker driver:

```bash
minikube start --driver=docker --cpus=2 --memory=2500mb --disk-size=7g
```

Enable Metrics Server (required for HPA):

```bash
minikube addons enable metrics-server
```

Check cluster:

```bash
kubectl get nodes
```

---

# 🍃 **5. Deploy MongoDB to Kubernetes**

### Apply all MongoDB-related YAML files:

```bash
kubectl apply -f k8s/mongodb-secret.yaml
kubectl apply -f k8s/mongodb-pv.yaml
kubectl apply -f k8s/mongodb-pvc.yaml
kubectl apply -f k8s/mongodb-statefulset.yaml
kubectl apply -f k8s/mongodb-service.yaml
```

Check pod:

```bash
kubectl get pods
```

Expected:

```
mongodb-0   Running
```

---

# 🧪 **6. Deploy Flask App to Kubernetes**

```bash
kubectl apply -f k8s/flask-deployment.yaml
kubectl apply -f k8s/flask-service.yaml
```

Check:

```bash
kubectl get pods
kubectl get svc
```

---

# 🌐 **7. Accessing the Flask App**

Get service URL:

```bash
minikube service flask-service
```

OR manually:

```
http://<minikube-ip>:32000
```

Example:

```
http://192.168.49.2:32000/
```

### Test endpoints:

```bash
curl http://192.168.49.2:32000/
```

Insert data:

```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"name":"amitabh"}' \
http://192.168.49.2:32000/data
```

Retrieve data:

```bash
curl http://192.168.49.2:32000/data
```

---

# 📈 **8. Horizontal Pod Autoscaler (HPA)**

Apply HPA:

```bash
kubectl apply -f k8s/hpa.yaml
```

Check status:

```bash
kubectl get hpa
```

Expected:

```
flask-hpa   2/70%   2   5   2
```

---

# 🔥 **9. Autoscaling Load Test**

Run a load generator:

```bash
kubectl run -i --tty load-generator --image=busybox --rm \
-- /bin/sh -c "while true; do wget -q -O- http://flask-service:5000/; done"
```

In another terminal:

```bash
kubectl get hpa -w
```

Watch replicas scale:

```bash
kubectl get pods -w
```

### 📸 Add screenshots here:

* [x] `kubectl get hpa -w` showing scale up
* [x] `kubectl get pods -w` showing more pods created
* [x] Load generator terminal window
* [x] CPU usage behavior

---

# 🧠 **10. How DNS Works in Kubernetes**

Kubernetes provides internal DNS resolution using **CoreDNS**.

### Flask connects to MongoDB using service DNS:

```
mongodb-service.default.svc.cluster.local
```

This resolves automatically to the ClusterIP of the MongoDB Service.

### Flow:

Flask Pod → CoreDNS → Service → MongoDB Pod

This enables:

* No hardcoded IPs
* Automatic failover
* Stable endpoints

---

# 🧰 **11. Resource Requests & Limits Explanation**

### **Why Requests?**

`resources.requests`
→ Minimum guaranteed CPU/memory
→ Scheduler uses this to place pods safely

### **Why Limits?**

`resources.limits`
→ Hard upper boundary
→ Prevents a pod from consuming all cluster resources

### **Values used:**

```
requests:
  cpu: 0.2
  memory: 250Mi

limits:
  cpu: 0.5
  memory: 500Mi
```

Good balance for demo applications.

---

# 🧩 **12. Design Choices**

### ✔ StatefulSet for MongoDB

MongoDB requires stable network identity and persistent storage → StatefulSet ideal.

### ✔ PV/PVC

Ensures database data is NOT lost between pod restarts.

### ✔ Secret for Authentication

Stores MongoDB root username/password securely.

### ✔ ClusterIP Service for MongoDB

Internal-only access. Flask pods can reach it, outside world cannot.

### ✔ NodePort for Flask

Allows access from browser/cURL via Minikube IP.

### ✔ HPA on CPU

Matches assignment requirement:
Scale from **2 to 5 replicas** if CPU > 70%.

---

# 🧪 **13. Testing Scenarios (As Required)**

### 🔘 Test 1 — Insert Data

Use POST `/data`
→ Check MongoDB entry insertion.

### 🔘 Test 2 — Retrieve Data

Use GET `/data`
→ Confirm JSON list returned.

### 🔘 Test 3 — Autoscaling

Run load generator
→ Observe scaling to 3, 4, then 5 pods.

### 🔘 Test 4 — Pod Restarts

Delete a pod manually:

```
kubectl delete pod flask-app-XXXXX
```

Deployment automatically recreates it.

### 🔘 Test 5 — MongoDB Persistence

Restart pods:

```
kubectl delete pod mongodb-0
```

PVC ensures data persists.

---

# 🧹 **14. Cleanup (Optional)**

```bash
kubectl delete -f k8s/
minikube stop
```

---

# 🎯 **15. Final Notes**

* All required components from the assignment PDF are fully implemented
* All screenshots must be added before submission
* The project runs end-to-end on Minikube
* This README can be included directly in your submission ZIP
