#!/bin/bash
# TaskFlow Setup Script

set -e

echo "🚀 Setting up TaskFlow..."

# 1. Create database
echo "📦 Creating database..."
if ! psql -lqt | cut -d \| -f 1 | grep -qw taskflow; then
    createdb taskflow
    echo "✅ Database 'taskflow' created"
else
    echo "✅ Database 'taskflow' already exists"
fi

# 2. Install Python dependencies
echo "📦 Installing dependencies..."
pip install -q -r requirements.txt
echo "✅ Dependencies installed"

# 3. Initialize database tables
echo "📦 Initializing database tables..."
python3 -c "from database import init_db; init_db()"
echo "✅ Tables created"

# 4. Make CLI executable
echo "📦 Setting up CLI..."
chmod +x cli.py
if [ ! -L /usr/local/bin/taskflow ]; then
    sudo ln -sf $(pwd)/cli.py /usr/local/bin/taskflow
fi
echo "✅ CLI installed (taskflow command available)"

# 5. Start server
echo "🚀 Starting TaskFlow API server..."
echo "   URL: http://localhost:8080"
echo "   Docs: http://localhost:8080/docs"
echo ""
echo "To start server manually: cd $(pwd) && python3 main.py"
echo "To use CLI: taskflow --help"
echo ""

nohup python3 main.py > taskflow.log 2>&1 &
echo $! > taskflow.pid

sleep 2

if curl -s http://localhost:8080/ > /dev/null; then
    echo "✅ TaskFlow API running (PID: $(cat taskflow.pid))"
    echo ""
    echo "🎉 Setup complete!"
    echo ""
    echo "Next steps:"
    echo "  1. Try: taskflow stats"
    echo "  2. Try: taskflow create 'Test task' --assignee mira"
    echo "  3. Visit dashboard: http://guenther.tail360cf1.ts.net:3030"
else
    echo "❌ Server failed to start. Check taskflow.log"
    exit 1
fi
