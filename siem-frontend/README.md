# CRPF IT System Log Analyzer – README

## Overview  
This repository contains a containerized, self-managed SIEM solution built on the Elastic Stack (8.11.0) to collect, analyze, and visualize logs, metrics, and security alerts for the Central Reserve Police Force (CRPF). It supports distributed edge deployments across 500+ sites, ensures data sovereignty, and enforces government-grade compliance.

***

## Table of Contents  
- [Features](#features)  
- [Architecture](#architecture)  
- [Prerequisites](#prerequisites)  
- [Installation & Setup](#installation--setup)  
- [Usage](#usage)  
  - [Data Ingestion](#data-ingestion)  
  - [Dashboard & SIEM](#dashboard--siem)  
  - [Metrics & Uptime](#metrics--uptime)  
- [Security & Compliance](#security--compliance)  
- [Customization](#customization)  
- [Troubleshooting](#troubleshooting)  
- [Project Uniqueness](#project-uniqueness)  
- [Contributors](#contributors)  

***

## Features  
- **Centralized Fleet Management:** Unified Elastic Agent enrollment via Fleet Server  
- **Log Ingestion:** Filebeat with Docker autodiscover; enriches logs with metadata  
- **Metrics Collection:** Metricbeat modules for system and Docker metrics  
- **Uptime Monitoring:** Heartbeat checks for critical services (APM, Kibana, Elasticsearch)  
- **APM Integration:** APM Server collects application traces  
- **Real-time Dashboards:** Prebuilt “CRPF Security Overview” with drill-down analytics  
- **Security Detection:** Elastic Security prebuilt rules auto-installed and bulk-enabled  
- **Compliance Reporting:** Audit trails and regulatory report templates  
- **Edge-Ready:** Local processing for intermittent connectivity; central aggregation when online

***

## Architecture  
```text
┌─────────────────────────────┐
│        Central Hub          │
│ ┌─────────┐  ┌────────────┐ │
│ │Elasticsearch Cluster (1-3│ │
│ │  or Single Node)          │ │
│ └─────────┘  └────────────┘ │
│       │       │            │
│   Kibana   Fleet Server    │
└─────┼──────────────┼────────┘
      │              │
┌─────▼────┐     ┌───▼────┐     ┌───────────┐
│Filebeat  │     │Metric- │ ... │Elastic    │
│(500+ Edge│     │beat    │     │Agent      │
│Hosts/VMs)│     │Agents  │     │Containers │
└──────────┘     └────────┘     └───────────┘
```

***

## Prerequisites  
- Docker and Docker Compose (v3.8+)  
- Linux host with `vm.max_map_count≥262144`  
- Ports: 9200, 5601, 8220 exposed  
- Minimum host resources: 8 GB RAM, 4 CPU cores

***

## Installation & Setup  

1. **Clone repository**  
   ```bash
   git clone <repo-url>
   cd crpf-log-analyzer
   ```

2. **Configure `.env`**  
   ```ini
   ELASTIC_VERSION=8.11.0
   ELASTIC_PASSWORD=YourElasticPassword
   KBN_ENCRYPTION_KEY=32+charEncryptionKeyHere
   FLEET_SERVER_SERVICE_TOKEN=           # will be auto-populated
   ```

3. **Ensure host settings**  
   ```bash
   sudo sysctl -w vm.max_map_count=262144
   ```

4. **Launch services**  
   ```bash
   docker compose up -d elasticsearch
   # wait for health
   docker compose up -d
   ```

5. **Bootstrap Fleet Server**  
   ```bash
   chmod +x bootstrap.sh
   ./bootstrap.sh
   ```

***

## Usage  

### Data Ingestion  
- **Filebeat**  
  - Harvest local and Docker logs  
  - Mount `/var/lib/docker/containers` and `/var/run/docker.sock`  
- **Metricbeat**  
  - System and Docker metrics modules enabled in `metricbeat.yml`  
- **Heartbeat & APM**  
  - Uptime checks and performance traces  

### Dashboard & SIEM  
- Navigate to **http://localhost:5601** → Discover → **filebeat-logs**  
- Open **CRPF Security Overview** dashboard  
- Adjust time picker (Last 24 hours, etc.) and interact  

### Metrics & Uptime  
- In Kibana → Observability → Metrics → Host overview  
- In Observability → Uptime → view service status  

***

## Security & Compliance  
- TLS disabled for dev; enable SSL in production via environment vars  
- RBAC: use superuser or scoped `kibana_admin` role with feature privileges  
- Encryption key ensures secure saved objects  
- Service tokens/enrollment tokens via Security API  

***

## Customization  
- **Add New Log Source:** Update `filebeat.inputs` in `filebeat.yml`  
- **Add Detection Rules:** Modify or import custom rules via Detection Engine API  
- **Extend Dashboard:** Create new visualizations in UI or via Saved Objects API  

***

## Troubleshooting  
- **Empty Dashboard:** Expand time range; verify indices exist  
- **Container Startup Failure:** Check `vm.max_map_count` and ulimits  
- **Authentication Errors:** Confirm `elastic` credentials and `kbn-xsrf` header  

***

## Project Uniqueness  
- Government-grade SIEM tailored for CRPF  
- Edge-friendly with local processing  
- Multi-location correlation across 500+ sites  
- Cost-optimized open-source solution  

***

## Contributors  
- **Ratna Kiran Kodali** (20221CCS0097) – DevOps, Beats config, Fleet scripting  
- **Mahesh D U** (20221CCS0116) – Dashboard design, Saved Objects API  
- **Komal U** (20221CCS0159) – Security rules integration, compliance reporting  

***

*End of README*