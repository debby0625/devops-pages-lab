"""Check source contracts and, when supplied, the actual Jekyll homepage."""

import argparse
from html.parser import HTMLParser
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
START = "<!--START_SECTION:activity-->"
END = "<!--END_SECTION:activity-->"


def require(condition, message):
    if not condition:
        raise ValueError(message)


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.links = []
        self.styles = []

    def handle_data(self, data):
        self.text.append(data)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a":
            self.links.append(attrs.get("href", ""))
        if tag == "link" and attrs.get("rel") == "stylesheet":
            self.styles.append(attrs.get("href", ""))


def validate(built=None, require_activity=False):
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    index = (ROOT / "index.md").read_text(encoding="utf-8")
    require(readme.count(START) == 1, "README needs exactly one start marker.")
    require(readme.count(END) == 1, "README needs exactly one end marker.")
    require(readme.index(START) < readme.index(END), "Activity markers are reversed.")
    require(index.startswith("---\n"), "index.md needs YAML front matter.")
    require("layout: default" in index, "index.md needs its default layout.")
    require("{% include_relative README.md %}" in index, "Missing README include.")
    require(not (ROOT / "index.html").exists(), "Remove index.html: index.md is the homepage.")
    activity = readme.split(START, 1)[1].split(END, 1)[0]
    if require_activity:
        require(bool(re.search(r"^\s*(?:\d+\.|[-*])\s+.+\[.+?\]\(https://github\.com/", activity, re.M)),
                "No generated GitHub activity item. Check TOKEN, username and events feed; rerun after events appear.")
    if built:
        path = ROOT / built
        require(path.is_file(), "Jekyll did not generate the homepage.")
        html = path.read_text(encoding="utf-8")
        require("{%" not in html and "{{" not in html, "Unprocessed Liquid in output.")
        page = Page()
        page.feed(html)
        text = " ".join(" ".join(page.text).split())
        for heading in ("DevOps Activity Journal", "Latest activity", "How publishing works"):
            require(heading in text, "README content missing from homepage: " + heading)
        for url in re.findall(r"\]\((https://github\.com/[^\s)]+)\)", activity):
            require(url in page.links, "Activity link missing from generated page: " + url)
        require(len(page.styles) == 1, "Expected the site's stylesheet.")
        css_path = path.parent / "assets/style.css"
        require(css_path.is_file(), "Built site is missing assets/style.css.")
        require(page.styles[0].endswith("/assets/style.css"), "Incorrect stylesheet URL.")
    print("PASS: source" + (", generated activity" if require_activity else "") + (", built homepage" if built else ""))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--built", help="Path to the actual Jekyll-generated homepage")
    parser.add_argument("--require-activity", action="store_true")
    args = parser.parse_args()
    try:
        validate(args.built, args.require_activity)
    except (ValueError, OSError) as error:
        print("FAIL:", error, file=sys.stderr)
        sys.exit(1)

