import argparse
import json
import os
from pathlib import Path

import openai

KNOWLEDGE_BASE = Path("knowledge_base.json")


def load_kb():
    if KNOWLEDGE_BASE.exists():
        with open(KNOWLEDGE_BASE, "r") as f:
            return json.load(f)
    return {"tasks": []}


def save_kb(kb):
    with open(KNOWLEDGE_BASE, "w") as f:
        json.dump(kb, f, indent=2)


def add_task(description: str):
    kb = load_kb()
    task_id = len(kb["tasks"]) + 1
    kb["tasks"].append({
        "id": task_id,
        "description": description,
        "steps": [],
        "status": "pending",
    })
    save_kb(kb)
    print(f"Added task {task_id}: {description}")


def breakdown_task(task: dict, client: openai.OpenAI) -> str:
    prompt = (
        "Break down the following task into a numbered list of actionable steps\n\n"
        f"Task: {task['description']}"
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    steps_text = response.choices[0].message.content.strip()
    task["steps"] = [s.strip() for s in steps_text.split("\n") if s.strip()]
    return steps_text


def process_tasks(client: openai.OpenAI):
    kb = load_kb()
    for task in kb["tasks"]:
        if task["status"] == "pending":
            print(f"Processing task {task['id']}: {task['description']}")
            steps = breakdown_task(task, client)
            print("Suggested steps:\n" + steps)
            input("Press enter when task is done...")
            task["status"] = "done"
    save_kb(kb)
    print("All pending tasks processed.")


def view_tasks():
    kb = load_kb()
    for task in kb["tasks"]:
        print(f"[{task['status']}] {task['id']}: {task['description']}")
        for step in task.get("steps", []):
            print(f"  - {step}")


def main():
    parser = argparse.ArgumentParser(description="Simple promptware demo")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_p = subparsers.add_parser("add", help="Add a new task")
    add_p.add_argument("description", help="Task description")

    subparsers.add_parser("process", help="Process pending tasks")
    subparsers.add_parser("view", help="View all tasks")

    args = parser.parse_args()

    if args.command == "add":
        add_task(args.description)
        return

    if args.command == "process":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise SystemExit(
                "OPENAI_API_KEY environment variable is required for processing tasks"
            )
        client = openai.OpenAI(api_key=api_key)
        process_tasks(client)
    elif args.command == "view":
        view_tasks()


if __name__ == "__main__":
    main()
