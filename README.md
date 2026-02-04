# TaskFlow - Team Project Management System

Postgres-based task management with Kanban UI for the agent team.

**🌐 Live:** http://guenther.tail360cf1.ts.net:8090  
**📖 API Docs:** http://guenther.tail360cf1.ts.net:8090/docs  
**📊 Dashboard:** http://guenther.tail360cf1.ts.net:3030

## Architecture

**Backend:**
- FastAPI (Python)
- SQLAlchemy ORM
- PostgreSQL database
- RESTful API

**Frontend:**
- Existing Kanban dashboard (~/clawd/dashboard/)
- Connects to TaskFlow API
- Real-time updates

**Integration:**
- All agents can create/update tasks via API
- CLI tool for quick task management
- Skill file for agent access

## Quick Start

```bash
# 1. Set up database
createdb taskflow

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations
python migrate.py

# 4. Start server
python main.py

# 5. Access dashboard
http://localhost:8080
```

## API Endpoints

Base URL: `http://guenther.tail360cf1.ts.net:8090`

- `GET /tasks` - List all tasks
- `POST /tasks` - Create task
- `PATCH /tasks/{id}` - Update task
- `DELETE /tasks/{id}` - Delete task
- `GET /tasks/by-assignee/{assignee}` - Tasks for specific agent
- `GET /stats` - Task statistics

## Database Schema

**tasks table:**
- id (uuid, primary key)
- title (text)
- description (text)
- assignee (text: mira/felix/werner/sophie/martin/jon)
- status (text: backlog/todo/in-progress/review/done)
- priority (text: low/medium/high/urgent)
- category (text: dev/finance/marketing/admin/client)
- created_at (timestamp)
- updated_at (timestamp)
- due_date (timestamp, nullable)
- created_by (text)

## Agent Skill

All agents have access via `taskflow` skill - see `/skills/taskflow/SKILL.md`

## Development

- Backend: `/home/clawd/dev/taskflow/`
- Dashboard: `/home/clawd/clawd/dashboard/` (integrated)
- Port: 8080 (backend API)
- Port: 3030 (dashboard - existing)

## Status

Created: 2026-02-04
Status: In Development
Owner: Mira
