from flask import Flask, render_template, jsonify, request
import json
from datetime import datetime
import os
from ai_threat_detector import CRPFThreatDetector

app = Flask(__name__)
detector = CRPFThreatDetector()

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/threat-summary')
def threat_summary():
    """API endpoint for threat summary"""
    try:
        report = detector.generate_threat_report()
        return jsonify(report)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/location-stats')
def location_stats():
    """API endpoint for location-wise statistics"""
    try:
        logs_df = detector.fetch_logs(24)
        if logs_df.empty:
            return jsonify({'error': 'No data available'})
        
        location_stats = logs_df.groupby('location').agg({
            'message': 'count',
            'severity': lambda x: (x == 'high').sum()
        }).to_dict('index')
        
        return jsonify(location_stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/real-time-alerts')
def real_time_alerts():
    """API endpoint for real-time alerts"""
    try:
        report = detector.generate_threat_report()
        recent_threats = [t for t in report.get('threats', []) 
                         if t['severity'] == 'high']
        return jsonify(recent_threats[:10])  # Last 10 high-severity threats
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
