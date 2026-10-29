"""Exercise source guards in disposable copies; never alter published sources."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def case(name, change=None, expected=None, require_activity=False):
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "site"
        shutil.copytree(ROOT, target, ignore=shutil.ignore_patterns(".git", "_site", "__pycache__"))
        if change:
            change(target)
        command = [sys.executable, str(target / "scripts/validate_site.py")]
        if require_activity:
            command.append("--require-activity")
        result = subprocess.run(command, text=True, capture_output=True)
        output = (result.stdout + result.stderr).strip()
        if expected:
            assert result.returncode != 0 and expected in output, (name, result.returncode, output)
            print(f"PASS expected rejection: {name}\n  {output}")
        else:
            assert result.returncode == 0, (name, output)
            print(f"PASS accepted: {name}\n  {output}")


def replace(path, before, after):
    path.write_text(path.read_text(encoding="utf-8").replace(before, after), encoding="utf-8")


case("valid source")
case("missing activity marker", lambda p: replace(p / "README.md", "<!--START_SECTION:activity-->", ""), "exactly one start marker")
case("duplicate marker", lambda p: replace(p / "README.md", "<!--START_SECTION:activity-->", "<!--START_SECTION:activity-->\n<!--START_SECTION:activity-->"), "exactly one start marker")
def reverse_markers(p):
    readme = p / "README.md"
    text = readme.read_text(encoding="utf-8")
    text = text.replace("<!--START_SECTION:activity-->", "TEMP_START")
    text = text.replace("<!--END_SECTION:activity-->", "<!--START_SECTION:activity-->")
    readme.write_text(text.replace("TEMP_START", "<!--END_SECTION:activity-->"), encoding="utf-8")


case("reversed markers", reverse_markers, "markers are reversed")
case("missing README include", lambda p: replace(p / "index.md", "{% include_relative README.md %}", ""), "Missing README include")
case("competing homepage", lambda p: (p / "index.html").write_text("competing entry"), "Remove index.html")


def empty_activity(p):
    readme = p / "README.md"
    text = readme.read_text(encoding="utf-8")
    start = "<!--START_SECTION:activity-->"
    end = "<!--END_SECTION:activity-->"
    readme.write_text(text.split(start)[0] + start + "\nPending\n" + end + text.split(end)[1], encoding="utf-8")


case("empty activity", empty_activity, "No generated GitHub activity item", require_activity=True)
print("PASS: all 7 validation scenarios; published sources untouched.")
