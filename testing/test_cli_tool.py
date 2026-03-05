import subprocess
import os
import textwrap

def run_cli_command(command):
    """Helper to run CLI command and capture output"""
    return subprocess.run(command, capture_output=True, text=True, encoding='utf-8')

def test_add_task():
    result = run_cli_command(["python", "-m", "lib.cli_tool", "add-task", "Alice", "Submit report"])
    assert "📌 Task 'Submit report' added to Alice." in result.stdout

import textwrap # Don't forget to import this at the top of your test file!

def test_complete_task_with_script(tmp_path):
    script_path = tmp_path / "script.py"
    
    # Using textwrap.dedent removes the leading spaces from the multi-line string
    script_content = textwrap.dedent(f"""
        import sys
        import io
        import os
        if sys.platform == "win32":
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        
        sys.path.insert(0, {repr(os.getcwd())})
        from lib.models import Task, User

        user = User("Bob")
        task = Task("Finish lab")
        user.add_task(task)
        task.complete()
        
        # FIX: Force the output to flush immediately
        print(f"✅ Task '{{task.title}}' completed.", flush=True)
    """).strip()

    script_path.write_text(script_content, encoding='utf-8')

    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"

    result = subprocess.run(
        ["python", str(script_path)],
        capture_output=True,
        text=True,
        env=env,
        encoding="utf-8" 
    )

    assert "✅ Task 'Finish lab' completed." in result.stdout