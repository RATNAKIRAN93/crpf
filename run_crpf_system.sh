#!/bin/bash

echo "🛡️ Starting CRPF Centralized Log Analyzer System..."

# Start ELK Stack and Wazuh
echo "Starting logging infrastructure..."
docker-compose up -d

# Wait for Elasticsearch to be ready
echo "Waiting for Elasticsearch to start..."
until curl -s "localhost:9200" > /dev/null; do
    echo "Waiting for Elasticsearch..."
    sleep 10
done

echo "✅ Elasticsearch is ready!"

# Wait for Kibana
echo "Waiting for Kibana to start..."
until curl -s "localhost:5601" > /dev/null; do
    echo "Waiting for Kibana..."
    sleep 10
done

echo "✅ Kibana is ready!"

# Generate initial test data
echo "Generating test log data..."
python3 log_generator.py &
LOG_GENERATOR_PID=$!

# Start the web dashboard
echo "Starting web dashboard..."
python3 dashboard.py &
DASHBOARD_PID=$!

echo ""
echo "🎉 CRPF Log Analyzer System is now running!"
echo ""
echo "📊 Access points:"
echo "   - Web Dashboard: http://localhost:5000"
echo "   - Kibana: http://localhost:5601"
echo "   - Elasticsearch: http://localhost:9200"
echo ""
echo "Press Ctrl+C to stop all services"

# Cleanup function
cleanup() {
    echo ""
    echo "Stopping all services..."
    kill $LOG_GENERATOR_PID 2>/dev/null
    kill $DASHBOARD_PID 2>/dev/null
    docker-compose down
    echo "✅ All services stopped"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Keep script running
wait
