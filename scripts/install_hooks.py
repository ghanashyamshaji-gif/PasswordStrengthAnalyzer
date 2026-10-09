"""Install the project's git hooks into .git/hooks."""
import os
import shutil
import stat

SOURCE = os.path.join("scripts", "pre-commit")
TARGET = os.path.join(".git", "hooks", "pre-commit")


def main():
    if not os.path.isdir(".git"):
        raise SystemExit("Run this from the project root (the folder that contains .git).")
    shutil.copyfile(SOURCE, TARGET)
    mode = os.stat(TARGET).st_mode
    os.chmod(TARGET, mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    print(f"Installed {TARGET}")


if __name__ == "__main__":
    main()
