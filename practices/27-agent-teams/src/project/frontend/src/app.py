"""
Sample Frontend Application — Streamlit Dashboard

A minimal Streamlit application structure for Agent Teams to work on.
This is a Python equivalent of the original React frontend.

Usage:
    pip install streamlit requests
    streamlit run app.py
"""

from dataclasses import dataclass
from typing import Optional

import streamlit as st
import requests

# ── Types ────────────────────────────────────────────────────────────────


@dataclass
class Task:
    id: str
    title: str
    status: str  # "todo" | "in-progress" | "done"
    assignee: Optional[str] = None


@dataclass
class DashboardData:
    tasks: list[Task]
    total_count: int
    completed_count: int


# ── API Client ───────────────────────────────────────────────────────────

API_BASE = "http://localhost:5000"


def fetch_dashboard() -> DashboardData:
    """Fetch dashboard data from the backend API."""
    response = requests.get(f"{API_BASE}/api/dashboard")
    response.raise_for_status()
    data = response.json()
    tasks = [
        Task(
            id=t["id"],
            title=t["title"],
            status=t["status"],
            assignee=t.get("assignee"),
        )
        for t in data["tasks"]
    ]
    return DashboardData(
        tasks=tasks,
        total_count=data["total_count"],
        completed_count=data["completed_count"],
    )


# ── UI Components ────────────────────────────────────────────────────────


def render_task_item(task: Task) -> None:
    """Render a single task item."""
    status_colors = {
        "todo": "red",
        "in-progress": "orange",
        "done": "green",
    }
    color = status_colors.get(task.status, "gray")
    assignee_str = f" @{task.assignee}" if task.assignee else ""
    st.markdown(
        f"- :{color}[{task.status}] **{task.title}**{assignee_str}"
    )


def render_task_list(tasks: list[Task]) -> None:
    """Render the task list."""
    for task in tasks:
        render_task_item(task)


# ── Main App ─────────────────────────────────────────────────────────────


def main() -> None:
    """Main Streamlit app."""
    st.set_page_config(page_title="Task Dashboard", layout="wide")
    st.title("Task Dashboard")

    try:
        data = fetch_dashboard()

        st.subheader(
            f"{data.completed_count}/{data.total_count} tasks completed"
        )

        render_task_list(data.tasks)

    except requests.ConnectionError:
        st.error(
            "Cannot connect to the backend API. "
            "Make sure the Flask server is running on port 5000."
        )
    except Exception as e:
        st.error(f"Error: {e}")


if __name__ == "__main__":
    main()
