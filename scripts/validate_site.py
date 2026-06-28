#!/usr/bin/env python3
"""TechVizions site and GitHub Pages workflow validation harness.

Default mode performs local/static checks that do not require Ruby gems, npm, or
network access. Optional --live mode validates deployed URLs and asset links.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "_config.yml",
    "_data/default.yml",
    "_data/home.yml",
    "_layouts/default.html",
    "_layouts/home.html",
    ".github/workflows/pages.yml",
    "assets/files/TechVizions_Capabilities_Statement.pdf",
    "federal-buyers.md",
    "cloud-security-assessment.md",
    "fedramp-nist-gap-review.md",
    "devsecops-pipeline-review.md",
]

REQUIRED_PAGES = {
    "/federal-buyers/": ["Federal Buyers", "site.data.home.federal.naics", "site.data.home.federal.sam"],
    "/cloud-security-assessment/": ["Cloud Security Assessment", "Starting at $9,500"],
    "/fedramp-nist-gap-review/": ["NIST / FedRAMP Gap Review", "Starting at $12,500"],
    "/devsecops-pipeline-review/": ["DevSecOps Pipeline Review", "Starting at $8,500"],
}

REQUIRED_LIVE_PAGES = {
    "/federal-buyers/": ["Federal Buyers", "LCSTMPTTFVT5", "0BQG8", "541511"],
    "/cloud-security-assessment/": ["Cloud Security Assessment", "Starting at $9,500"],
    "/fedramp-nist-gap-review/": ["NIST / FedRAMP Gap Review", "Starting at $12,500"],
    "/devsecops-pipeline-review/": ["DevSecOps Pipeline Review", "Starting at $8,500"],
}

REQUIRED_LIVE_ASSETS = [
    "/assets/vendor/bootstrap/css/bootstrap.min.css",
    "/assets/css/agency.min.css",
    "/assets/js/agency.min.js",
    "/assets/img/logos/techvizions-horizontal-no-llc-allwhite-fixed.svg",
    "/assets/files/TechVizions_Capabilities_Statement.pdf",
]


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for key, value in attrs:
            if key in {"href", "src"} and value:
                self.links.append(value)


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def ok(message: str) -> None:
    print(f"OK: {message}")


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def run(cmd: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, check=check)


def http_get(url: str) -> tuple[int, bytes, str]:
    req = urllib.request.Request(url, headers={"User-Agent": "TechVizionsHarness/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, resp.read(), resp.headers.get("content-type", "")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read(), exc.headers.get("content-type", "")


def assert_contains(text: str, needles: Iterable[str], subject: str) -> None:
    for needle in needles:
        if needle not in text:
            fail(f"{subject} missing required text: {needle}")


def local_checks() -> None:
    for rel in REQUIRED_FILES:
        path = ROOT / rel
        if not path.exists():
            fail(f"required file missing: {rel}")
    ok("required files exist")

    diff = run(["git", "diff", "--check", "--", ".", ":!assets/files/TechVizions_Capabilities_Statement.pdf"], check=False)
    if diff.returncode != 0:
        print(diff.stdout)
        print(diff.stderr, file=sys.stderr)
        fail("git diff --check failed")
    ok("git diff --check passed for text files")

    config = read("_config.yml")
    assert_contains(config, ["assets_path: '/assets/'", "url: \"https://techvizions.com\""], "_config.yml")
    ok("asset path is absolute for child pages")

    default_layout = read("_layouts/default.html")
    assert_contains(
        default_layout,
        [
            "{{ page.title | default: site.title }}",
            "{{ page.description | default: site.description }}",
            "{{ page.keywords | default:",
            "{{ assets_path }}vendor/bootstrap/css/bootstrap.min.css",
            "{{ assets_path }}css/agency.min.css",
            "body.layout-default #mainNav",
            "class=\"layout-{{ page.layout | default: 'default' }}\"",
        ],
        "_layouts/default.html",
    )
    ok("default layout supports per-page SEO, asset path variable, and readable interior nav")

    home_layout = read("_layouts/home.html")
    assert_contains(home_layout, ["#federal-buyers", "View Federal Buyer Page", "Learn More", "<!-- Portfolio Grid -->"], "_layouts/home.html")
    ok("home layout includes federal buyer CTA and package links")

    home_data = read("_data/home.yml")
    assert_contains(
        home_data,
        [
            "LCSTMPTTFVT5",
            "0BQG8",
            "541511",
            "541512",
            "541519",
            "518210",
            "/cloud-security-assessment/",
            "/fedramp-nist-gap-review/",
            "/devsecops-pipeline-review/",
        ],
        "_data/home.yml",
    )
    ok("federal buyer data includes SAM, NAICS, and service URLs")

    workflow = read(".github/workflows/pages.yml")
    assert_contains(
        workflow,
        [
            "actions/checkout@v5",
            "actions/configure-pages@v6",
            "actions/jekyll-build-pages@v1",
            "actions/upload-pages-artifact@v5",
            "actions/deploy-pages@v5",
        ],
        ".github/workflows/pages.yml",
    )
    if "python3 scripts/validate_site.py --local" not in workflow:
        fail("workflow does not run the local validation harness")
    ok("GitHub Pages workflow uses expected actions and local harness")

    for page, needles in REQUIRED_PAGES.items():
        rel = page.strip("/") + ".md"
        if page == "/federal-buyers/":
            rel = "federal-buyers.md"
        text = read(rel)
        assert_contains(text, needles, rel)
        if f"permalink: {page}" not in text:
            fail(f"{rel} missing permalink {page}")
    ok("child page frontmatter/content checks passed")

    pdf = ROOT / "assets/files/TechVizions_Capabilities_Statement.pdf"
    data = pdf.read_bytes()
    if not data.startswith(b"%PDF") or len(data) < 3000:
        fail("capabilities statement PDF is missing, invalid, or unexpectedly small")
    ok("capabilities statement PDF exists and has a valid PDF header")


def live_checks(base_url: str) -> None:
    base_url = base_url.rstrip("/")
    for path, needles in REQUIRED_LIVE_PAGES.items():
        url = base_url + path
        status, body, ctype = http_get(url)
        if status != 200:
            fail(f"{url} returned HTTP {status}")
        text = body.decode("utf-8", errors="replace")
        assert_contains(text, needles, url)

        parser = LinkParser()
        parser.feed(text)
        broken_relative_assets = [
            link for link in parser.links
            if link.startswith(("vendor/", "css/", "js/", "img/"))
        ]
        if broken_relative_assets:
            fail(f"{url} contains child-page-breaking relative asset links: {broken_relative_assets}")
    ok("live child pages returned 200 and contain required text")

    for asset in REQUIRED_LIVE_ASSETS:
        url = base_url + asset
        status, body, ctype = http_get(url)
        if status != 200:
            fail(f"required asset {url} returned HTTP {status}")
        if asset.endswith(".pdf") and not body.startswith(b"%PDF"):
            fail(f"{url} did not return a PDF")
    ok("live required assets returned 200")


def gh_checks() -> None:
    gh_status = run(["gh", "auth", "status"], check=False)
    if gh_status.returncode != 0:
        fail("gh is not authenticated")

    pages = run(["gh", "api", "repos/tonyvinson/tonyvinson.github.io/pages", "--jq", "{build_type: .build_type, status: .status}"])
    payload = json.loads(pages.stdout)
    if payload.get("build_type") != "workflow":
        fail(f"GitHub Pages build_type is not workflow: {payload}")
    ok("GitHub Pages is configured for workflow builds")

    runs = run(["gh", "run", "list", "--repo", "tonyvinson/tonyvinson.github.io", "--workflow", "Deploy Jekyll site to GitHub Pages", "--limit", "1", "--json", "status,conclusion,databaseId"])
    latest = json.loads(runs.stdout)[0]
    if latest.get("status") != "completed" or latest.get("conclusion") != "success":
        fail(f"latest Pages workflow is not successful: {latest}")
    ok(f"latest Pages workflow succeeded: {latest['databaseId']}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate TechVizions website and GitHub Pages workflow")
    parser.add_argument("--local", action="store_true", help="run local/static checks")
    parser.add_argument("--live", action="store_true", help="run live deployed-site checks")
    parser.add_argument("--gh", action="store_true", help="run GitHub CLI workflow/account checks")
    parser.add_argument("--base-url", default="https://techvizions.com", help="base URL for --live checks")
    args = parser.parse_args()

    if not (args.local or args.live or args.gh):
        args.local = True

    if args.local:
        local_checks()
    if args.live:
        live_checks(args.base_url)
    if args.gh:
        gh_checks()

    print("All requested checks passed.")


if __name__ == "__main__":
    main()
