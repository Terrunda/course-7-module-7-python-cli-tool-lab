import argparse
import sys
import io
from lib.models import Task, User

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


users = {}

def add_task(args):

    user = users.get(args.user) or User(args.user)
    users[args.user] = user
    task = Task(args.title)
    user.add_task(task)
    print(f"📌 Task '{args.title}' added to {args.user}.")

def complete_task(args):
    user = users.get(args.user)
    if user:
        for task in user.tasks:
            if task.title == args.title:
                task.complete()
                print(f"✅ Task '{args.title}' completed.")
                return
        print("❌ Task not found.")
    else:
        print("❌ User not found.")

def main():
    parser = argparse.ArgumentParser(description="Task Manager CLI")
    subparsers = parser.add_subparsers(dest="command") # Added dest for easier debugging

    add_parser = subparsers.add_parser("add-task", help="Add a new task")
    add_parser.add_argument("user")
    add_parser.add_argument("title")
    add_parser.set_defaults(func=add_task)

    complete_parser = subparsers.add_parser("complete-task", help="Complete a task")
    complete_parser.add_argument("user")
    complete_parser.add_argument("title")
    complete_parser.set_defaults(func=complete_task)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()