#!/bin/bash
# Startup script for Persona Forge sentiment-ag-ui

echo "🚀 Starting Persona Forge Backend and Frontend..."
echo ""

# Kill any existing processes on the ports
echo "🧹 Cleaning up existing processes..."
lsof -ti :8001 | xargs kill -9 2>/dev/null
lsof -ti :3000 | xargs kill -9 2>/dev/null

# Start backend
echo "🔧 Starting FastAPI backend on port 8001..."
cd /home/david-barnes/Documents/persona-forge-langgraph-master
nohup .venv/bin/python -m uvicorn ag_ui_backend:app --host 0.0.0.0 --port 8001 --reload > backend.log 2>&1 &
BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"

# Wait for backend to start
sleep 3

# Check backend health
echo "🏥 Checking backend health..."
HEALTH=$(curl -s http://localhost:8001/health)
if echo "$HEALTH" | grep -q "healthy\|agent_available"; then
    echo "   ✅ Backend is running!"
else
    echo "   ⚠️  Backend might have issues. Check backend.log"
fi

# Start frontend
echo ""
echo "🎨 Starting Next.js frontend..."
cd sentiment-ag-ui
npm run dev &
FRONTEND_PID=$!
echo "   Frontend PID: $FRONTEND_PID"

echo ""
echo "✨ All services started!"
echo ""
echo "📊 Services:"
echo "   Backend:  http://localhost:8001"
echo "   Frontend: http://localhost:3000 (or next available port)"
echo "   Neo4j:    bolt://localhost:7687"
echo ""
echo "📝 Logs:"
echo "   Backend:  tail -f backend.log"
echo ""
echo "🛑 To stop services:"
echo "   kill $BACKEND_PID $FRONTEND_PID"
echo "   or: pkill -f 'uvicorn ag_ui_backend' && pkill -f 'next dev'"
