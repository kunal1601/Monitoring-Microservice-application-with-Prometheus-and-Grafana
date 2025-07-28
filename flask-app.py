from flask import Flask
from prometheus_client import Counter, generate_latest

app = Flask(__name__)
hits = Counter('hits_total', 'Total page hits')

@app.route('/')
def index():
    
    hits.inc()
    hostname = socket.gethostname()
    try:
        ip_address = requests.get("https://api.ipify.org").text
    except Exception:
        ip_address = "Could not fetch IP"
    
    return f"""
    <h1>This function is monitored by Prometheus</h1>
    <p><strong>Hostname:</strong> {hostname}</p>
    <p><strong>Public IP:</strong> {ip_address}</p>
    """
@app.route('/metrics')
def metrics():
    return generate_latest(hits), 200, {'Content-Type': 'text/plain; version=0.0.4'}

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

