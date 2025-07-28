
# 📙 Microservice Monitoring with Prometheus & Grafana (Manual Docker + Ansible)

This project demonstrates how to monitor a Dockerized Python microservice along with system metrics using **Prometheus** and **Grafana**. No pre-built images, no Docker Compose, no Kubernetes — just **pure manual setup** with **Docker** and **Ansible**.

---

## 🧱 Tech Stack

- 🐍 Python Flask (microservice exposing `/metrics`)
- 🐳 Docker
- ⚙️ Prometheus
- 📊 Grafana
- 💻 Node Exporter
- 📜 Ansible (to automate Docker container setup)

---

## 📁 Project Structure

```
Monitoring-Microservice-application-with-Prometheus-and-Grafana/
├── Dockerfile.microservice
├── Dockerfile.prometheus
├── Dockerfile.node_exporter
├── Dockerfile.grafana
├── flask-app.py
├── prometheus.yml
├── playbook.yaml
├── inventory (optional if not using /etc/ansible/hosts)
```

---

## 🚀 Step-by-Step Setup

### 1️⃣ Run the Ansible Playbook

```bash
ansible-playbook -i inventory playbook.yaml
```

The `playbook.yaml` does the following:
- Builds Docker images manually
- Runs containers for:
  - Flask Microservice (5000)
  - Node Exporter (9100)
  - Prometheus (9090)
  - Grafana (3000)

Make sure the inventory file contains:
```ini
[local]
localhost ansible_connection=local
```

---

## 🧱 prometheus.yml (for Flask & Node Exporter)

```yaml
global:
  scrape_interval: 5s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'microservice'
    static_configs:
      - targets: ['172.17.0.1:5000']

  - job_name: 'node_exporter'
    static_configs:
      - targets: ['172.17.0.1:9100']
```

> Use `docker network inspect bridge` to confirm `172.17.0.1`.

---

## 🔢 Validate Prometheus Metrics

Visit: `http://<EC2-PUBLIC-IP>:9090/targets`

You should see:
- Microservice target → UP
- Node Exporter → UP
- Prometheus self → UP

To confirm metrics, visit:

```
http://<EC2-IP>:5000/metrics
```

Should display:
```
# HELP hits_total Total page hits
# TYPE hits_total counter
hits_total 0.0
```

---

## 📊 Grafana Setup

```bash
docker run -d -p 3000:3000 --name=grafana grafana/grafana
```

Login at: `http://<your-host>:3000`

- Username: `admin`
- Password: `admin`

### Add Prometheus Data Source

- Go to ⚙️ > Data Sources > Add New
- Type: Prometheus
- URL: `http://<prometheus-container-ip>:9090`
- Save & Test ✅

---

## 📈 Sample Prometheus Queries

```promql
hits_total
process_resident_memory_bytes
rate(node_cpu_seconds_total{mode!="idle"}[1m])
```

---

## 💼 Author

- 👨‍💻 Kunal Sharma
- 🔗 GitHub: [https://github.com/kunal1601/Monitoring-Microservice-application-with-Prometheus-and-Grafana](https://github.com/kunal1601/Monitoring-Microservice-application-with-Prometheus-and-Grafana)

---

## ✅ Summary

| Component     | Port | Role                          |
| ------------- | ---- | ----------------------------- |
| Flask App     | 5000 | Microservice exposing metrics |
| Node Exporter | 9100 | Exporting EC2 metrics         |
| Prometheus    | 9090 | Monitoring targets            |
| Grafana       | 3000 | Dashboard visualization       |

➡️ No Docker Compose. No Kubernetes. Just Docker + Ansible DevOps magic ✨

---

