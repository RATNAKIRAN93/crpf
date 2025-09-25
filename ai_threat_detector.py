import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import DBSCAN
import re
import json
from datetime import datetime
import elasticsearch
from elasticsearch import Elasticsearch

class CRPFThreatDetector:
    def __init__(self):
        self.es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.anomaly_detector = IsolationForest(contamination=0.1, random_state=42)
        
        # CRPF-specific threat patterns
        self.threat_patterns = {
            'failed_login': r'Failed (password|login|authentication)',
            'privilege_escalation': r'(sudo|admin|root|administrator).*failed',
            'suspicious_network': r'(port scan|brute force|DDoS|malware)',
            'file_access': r'(unauthorized|denied|forbidden).*access',
            'system_compromise': r'(backdoor|trojan|virus|malicious)',
            'data_exfiltration': r'(download|transfer|copy).*sensitive'
        }
    
    def fetch_logs(self, hours=24):
        """Fetch recent logs from Elasticsearch"""
        query = {
            "query": {
                "range": {
                    "@timestamp": {
                        "gte": f"now-{hours}h",
                        "lte": "now"
                    }
                }
            },
            "size": 10000
        }
        
        try:
            response = self.es.search(index="crpf-logs-*", body=query)
            logs = []
            for hit in response['hits']['hits']:
                source = hit['_source']
                logs.append({
                    'timestamp': source.get('@timestamp'),
                    'message': source.get('message', ''),
                    'location': source.get('location', 'unknown'),
                    'logtype': source.get('logtype', 'system'),
                    'severity': self._determine_severity(source.get('message', ''))
                })
            return pd.DataFrame(logs)
        except Exception as e:
            print(f"Error fetching logs: {e}")
            return pd.DataFrame()
    
    def _determine_severity(self, message):
        """Determine log severity based on content"""
        message_lower = message.lower()
        if any(keyword in message_lower for keyword in ['error', 'failed', 'denied', 'unauthorized']):
            return 'high'
        elif any(keyword in message_lower for keyword in ['warning', 'timeout', 'retry']):
            return 'medium'
        else:
            return 'low'
    
    def detect_pattern_threats(self, logs_df):
        """Detect threats using predefined patterns"""
        threats = []
        
        for pattern_name, pattern in self.threat_patterns.items():
            matches = logs_df[logs_df['message'].str.contains(pattern, case=False, na=False)]
            
            for _, log in matches.iterrows():
                threat = {
                    'type': pattern_name,
                    'timestamp': log['timestamp'],
                    'location': log['location'],
                    'message': log['message'],
                    'severity': 'high',
                    'detection_method': 'pattern_matching'
                }
                threats.append(threat)
        
        return threats
    
    def detect_anomalies(self, logs_df):
        """Detect anomalies using machine learning"""
        if len(logs_df) < 10:
            return []
        
        # Feature extraction
        message_features = self.vectorizer.fit_transform(logs_df['message'].fillna(''))
        
        # Anomaly detection
        anomaly_scores = self.anomaly_detector.fit_predict(message_features.toarray())
        
        anomalies = []
        for idx, score in enumerate(anomaly_scores):
            if score == -1:  # Anomaly detected
                log = logs_df.iloc[idx]
                anomaly = {
                    'type': 'anomalous_behavior',
                    'timestamp': log['timestamp'],
                    'location': log['location'],
                    'message': log['message'],
                    'severity': 'medium',
                    'detection_method': 'ml_anomaly'
                }
                anomalies.append(anomaly)
        
        return anomalies
    
    def generate_threat_report(self):
        """Generate comprehensive threat analysis report"""
        logs_df = self.fetch_logs(24)
        
        if logs_df.empty:
            return {"error": "No logs available for analysis"}
        
        # Detect threats
        pattern_threats = self.detect_pattern_threats(logs_df)
        ml_anomalies = self.detect_anomalies(logs_df)
        
        # Combine all threats
        all_threats = pattern_threats + ml_anomalies
        
        # Generate statistics
        stats = {
            'total_logs_analyzed': len(logs_df),
            'total_threats_detected': len(all_threats),
            'high_severity_threats': len([t for t in all_threats if t['severity'] == 'high']),
            'locations_affected': len(set([t['location'] for t in all_threats])),
            'threat_types': {}
        }
        
        # Count threat types
        for threat in all_threats:
            threat_type = threat['type']
            stats['threat_types'][threat_type] = stats['threat_types'].get(threat_type, 0) + 1
        
        return {
            'timestamp': datetime.now().isoformat(),
            'statistics': stats,
            'threats': all_threats,
            'recommendations': self._generate_recommendations(all_threats)
        }
    
    def _generate_recommendations(self, threats):
        """Generate security recommendations based on detected threats"""
        recommendations = []
        
        if any(t['type'] == 'failed_login' for t in threats):
            recommendations.append("Implement stronger password policies and account lockout mechanisms")
        
        if any(t['type'] == 'privilege_escalation' for t in threats):
            recommendations.append("Review and restrict administrative privileges")
        
        if any(t['type'] == 'suspicious_network' for t in threats):
            recommendations.append("Strengthen firewall rules and implement intrusion detection")
        
        if len(threats) > 10:
            recommendations.append("Increase monitoring frequency and alert thresholds")
        
        return recommendations

# Initialize and run analysis
if __name__ == "__main__":
    detector = CRPFThreatDetector()
    report = detector.generate_threat_report()
    
    # Save report
    with open(f'threat_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print("Threat analysis completed. Report saved.")
