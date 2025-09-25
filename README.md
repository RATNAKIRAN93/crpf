# CRPF Centralized IT System Log Analyzer

## Project Overview
A comprehensive Security Information and Event Management (SIEM) system designed for the Central Reserve Police Force (CRPF) to analyze IT system logs across 500+ locations for centralized threat detection and cybersecurity monitoring.

## Features
- ✅ Centralized log collection from multiple CRPF locations
- ✅ AI-driven threat detection using machine learning
- ✅ Real-time security monitoring dashboard
- ✅ Pattern-based threat identification
- ✅ Automated security recommendations
- ✅ Scalable ELK Stack implementation
- ✅ Wazuh integration for enhanced security monitoring

## Technology Stack
- **Backend**: Python, Flask, Elasticsearch, Wazuh
- **Frontend**: HTML5, Bootstrap, Chart.js
- **ML/AI**: Scikit-learn, TensorFlow
- **Infrastructure**: Docker, Docker Compose
- **Monitoring**: ELK Stack (Elasticsearch, Logstash, Kibana)

## Quick Start
1. Clone repository in GitHub Codespaces
2. Run: `chmod +x run_crpf_system.sh && ./run_crpf_system.sh`
3. Access dashboard at http://localhost:5000

## System Architecture
- **Log Collection**: Filebeat agents collect logs from various sources
- **Processing**: Elasticsearch indexes and stores log data
- **Analysis**: AI engine processes logs for threat detection
- **Visualization**: Kibana and custom dashboard for monitoring
- **Alerting**: Real-time threat notifications and recommendations

## Project Benefits
- Centralized security monitoring for 500+ CRPF locations
- Automated threat detection reduces manual analysis time
- Cost-effective open-source solution
- Scalable architecture for future expansion
- Compliance with government cybersecurity standards
