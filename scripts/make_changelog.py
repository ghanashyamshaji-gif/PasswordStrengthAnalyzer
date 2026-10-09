"""Print a changelog section made from commit messages since the last tag.

Usage: python scripts/make_changelog.py v0.2.0 > CHANGELOG.md
"""
import subprocess
import sys


def git(*args):
    result = subprocess.run(
        ["git", *args], capture_output=True, text=True, encoding="utf-8", check=True
    )
    return result.stdout.strip()


def main():
    version = sys.argv[1] if len(sys.argv) > 1 else "Unreleased"
    try:
        commit_range = f"{git('describe', '--tags', '--abbrev=0')}..HEAD"
    except subprocess.CalledProcessError:
        commit_range = "HEAD"  # no tags yet: use the whole history
    subjects = git("log", commit_range, "--no-merges", "--pretty=format:%s").splitlines()
    print(f"# Changelog\n\n## {version}\n")
    for subject in subjects:
        print(f"- {subject}")


if __name__ == "__main__":
    main()
