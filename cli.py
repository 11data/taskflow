#!/usr/bin/env python3
"""
TaskFlow CLI - Quick task management from command line
"""
import requests
import json
import sys
from datetime import datetime

API_URL = "http://localhost:8090"


def list_tasks(assignee=None, status=None):
    """List tasks"""
    params = {}
    if assignee:
        params["assignee"] = assignee
    if status:
        params["status"] = status
    
    response = requests.get(f"{API_URL}/tasks", params=params)
    tasks = response.json()
    
    if not tasks:
        print("No tasks found")
        return
    
    print(f"\n{'ID':<38} {'Title':<30} {'Assignee':<10} {'Status':<15} {'Priority':<10}")
    print("-" * 110)
    for task in tasks:
        print(f"{task['id']:<38} {task['title'][:30]:<30} {task['assignee']:<10} {task['status']:<15} {task['priority']:<10}")


def create_task(title, description, assignee, status="backlog", priority="medium", category="dev", created_by="cli"):
    """Create new task"""
    data = {
        "title": title,
        "description": description,
        "assignee": assignee,
        "status": status,
        "priority": priority,
        "category": category,
        "created_by": created_by,
    }
    
    response = requests.post(f"{API_URL}/tasks", json=data)
    if response.status_code == 201:
        task = response.json()
        print(f"✅ Task created: {task['id']}")
        print(f"   Title: {task['title']}")
        print(f"   Assignee: {task['assignee']}")
        print(f"   Status: {task['status']}")
    else:
        print(f"❌ Error creating task: {response.text}")


def update_task(task_id, **kwargs):
    """Update task"""
    data = {k: v for k, v in kwargs.items() if v is not None}
    
    response = requests.patch(f"{API_URL}/tasks/{task_id}", json=data)
    if response.status_code == 200:
        task = response.json()
        print(f"✅ Task updated: {task['id']}")
        print(f"   Title: {task['title']}")
        print(f"   Status: {task['status']}")
    else:
        print(f"❌ Error updating task: {response.text}")


def delete_task(task_id):
    """Delete task"""
    response = requests.delete(f"{API_URL}/tasks/{task_id}")
    if response.status_code == 204:
        print(f"✅ Task deleted: {task_id}")
    else:
        print(f"❌ Error deleting task: {response.text}")


def show_stats():
    """Show task statistics"""
    response = requests.get(f"{API_URL}/stats")
    stats = response.json()
    
    print("\n📊 TaskFlow Statistics")
    print("=" * 50)
    print(f"Total Tasks: {stats['total']}")
    print("\nBy Status:")
    for status, count in stats['by_status'].items():
        print(f"  {status:15} {count:3}")
    print("\nBy Assignee:")
    for assignee, count in stats['by_assignee'].items():
        print(f"  {assignee:15} {count:3}")


def main():
    """Main CLI entry point"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  taskflow list [--assignee ASSIGNEE] [--status STATUS]")
        print("  taskflow create TITLE --assignee ASSIGNEE [--description DESC] [--status STATUS] [--priority PRIORITY]")
        print("  taskflow update TASK_ID [--status STATUS] [--assignee ASSIGNEE] [--priority PRIORITY]")
        print("  taskflow delete TASK_ID")
        print("  taskflow stats")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "list":
        assignee = None
        status = None
        for i, arg in enumerate(sys.argv[2:]):
            if arg == "--assignee" and i + 3 < len(sys.argv):
                assignee = sys.argv[i + 3]
            if arg == "--status" and i + 3 < len(sys.argv):
                status = sys.argv[i + 3]
        list_tasks(assignee, status)
    
    elif command == "create":
        if len(sys.argv) < 3:
            print("Error: Title required")
            sys.exit(1)
        
        title = sys.argv[2]
        description = None
        assignee = "mira"  # default
        status = "backlog"
        priority = "medium"
        category = "dev"
        
        for i, arg in enumerate(sys.argv[3:]):
            if arg == "--description" and i + 4 < len(sys.argv):
                description = sys.argv[i + 4]
            if arg == "--assignee" and i + 4 < len(sys.argv):
                assignee = sys.argv[i + 4]
            if arg == "--status" and i + 4 < len(sys.argv):
                status = sys.argv[i + 4]
            if arg == "--priority" and i + 4 < len(sys.argv):
                priority = sys.argv[i + 4]
            if arg == "--category" and i + 4 < len(sys.argv):
                category = sys.argv[i + 4]
        
        create_task(title, description, assignee, status, priority, category)
    
    elif command == "update":
        if len(sys.argv) < 3:
            print("Error: Task ID required")
            sys.exit(1)
        
        task_id = sys.argv[2]
        kwargs = {}
        
        for i, arg in enumerate(sys.argv[3:]):
            if arg == "--status" and i + 4 < len(sys.argv):
                kwargs["status"] = sys.argv[i + 4]
            if arg == "--assignee" and i + 4 < len(sys.argv):
                kwargs["assignee"] = sys.argv[i + 4]
            if arg == "--priority" and i + 4 < len(sys.argv):
                kwargs["priority"] = sys.argv[i + 4]
            if arg == "--title" and i + 4 < len(sys.argv):
                kwargs["title"] = sys.argv[i + 4]
        
        update_task(task_id, **kwargs)
    
    elif command == "delete":
        if len(sys.argv) < 3:
            print("Error: Task ID required")
            sys.exit(1)
        
        task_id = sys.argv[2]
        delete_task(task_id)
    
    elif command == "stats":
        show_stats()
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
