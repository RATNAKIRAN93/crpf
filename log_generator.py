import random
import json
from datetime import datetime, timedelta
import time
import requests

class CRPFLogGenerator:
    def __init__(self):
        self.locations = [
            "New Delhi HQ", "Mumbai Office", "Kolkata Regional", 
            "Chennai Center", "Bangalore Unit", "Hyderabad Base",
            "Ahmedabad Station", "Pune Division", "Jaipur Post",
            "Lucknow Command"
        ]
        
        self.log_types = [
            "authentication", "network", "system", "application", 
            "firewall", "endpoint", "database"
        ]
        
        self.normal_messages = [
            "User login successful",
            "System backup completed",
            "Network connection established",
            "Application started successfully",
            "Database query executed",
            "Firewall rule updated",
            "File access granted"
        ]
        
        self.threat_messages = [
            "Failed login attempt for user admin",
            "Unauthorized access attempt detected",
            "Suspicious network activity from external IP",
            "Malware signature detected in file transfer",
            "Privilege escalation attempt by user",
            "Brute force attack detected on SSH",
            "DDoS attack pattern identified",
            "Data exfiltration attempt blocked"
        ]
    
    def generate_log_entry(self, is_threat=False):
        """Generate a single log entry"""
        location = random.choice(self.locations)
        log_type = random.choice(self.log_types)
        
        if is_threat:
            message = random.choice(self.threat_messages)
            severity = random.choice(["high", "high", "medium"])  # Bias toward high
        else:
            message = random.choice(self.normal_messages)
            severity = random.choice(["low", "low", "medium"])    # Bias toward low
        
        return {
            "@timestamp": datetime.now().isoformat(),
            "message": message,
            "location": location,
            "logtype": log_type,
            "severity": severity,
            "host": f"{location.lower().replace(' ', '-')}-server",
            "source": f"/var/log/{log_type}.log"
        }
    
    def generate_batch(self, count=100, threat_ratio=0.15):
        """Generate a batch of log entries"""
        logs = []
        threat_count = int(count * threat_ratio)
        
        # Generate threat logs
        for _ in range(threat_count):
            logs.append(self.generate_log_entry(is_threat=True))
        
        # Generate normal logs
        for _ in range(count - threat_count):
            logs.append(self.generate_log_entry(is_threat=False))
        
        return logs
    
    def send_to_elasticsearch(self, logs, es_host="localhost:9200"):
        """Send logs to Elasticsearch"""
        for log in logs:
            try:
                index_name = f"crpf-logs-{datetime.now().strftime('%Y.%m.%d')}"
                url = f"http://{es_host}/{index_name}/_doc"
                
                response = requests.post(url, 
                                       headers={"Content-Type": "application/json"},
                                       data=json.dumps(log))
                
                if response.status_code not in [200, 201]:
                    print(f"Failed to send log: {response.status_code}")
                    
            except Exception as e:
                print(f"Error sending log: {e}")
    
    def continuous_generation(self, interval=10, batch_size=20):
        """Continuously generate and send logs"""
        print("Starting continuous log generation...")
        
        while True:
            try:
                logs = self.generate_batch(batch_size)
                self.send_to_elasticsearch(logs)
                print(f"Generated and sent {len(logs)} logs at {datetime.now()}")
                time.sleep(interval)
                
            except KeyboardInterrupt:
                print("Stopping log generation...")
                break
            except Exception as e:
                print(f"Error in continuous generation: {e}")
                time.sleep(5)

if __name__ == "__main__":
    generator = CRPFLogGenerator()
    
    # Generate initial batch of logs
    print("Generating initial log data...")
    initial_logs = generator.generate_batch(500, threat_ratio=0.2)
    generator.send_to_elasticsearch(initial_logs)
    print(f"Generated {len(initial_logs)} initial logs")
    
    # Start continuous generation
    generator.continuous_generation(interval=15, batch_size=10)
