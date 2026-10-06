import os

structure = {
    "analyzer": ["__init__.py", "strength.py", "patterns.py", "crack_time.py", "feedback.py"],
    "tests": ["__init__.py"],
}

for folder, files in structure.items():
    os.makedirs(folder, exist_ok=True)
    for f in files:
        path = os.path.join(folder, f)
        if not os.path.exists(path):
            open(path, "w").close()
            print(f"Created {path}")

if not os.path.exists("main.py"):
    open("main.py", "w").close()
    print("Created main.py")
