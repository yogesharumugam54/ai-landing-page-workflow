"""Quality checker for generated landing pages (standard library only).

Usage:
    python checks/check_page.py output/index.html brief/example-brief.md
"""
import re
import sys
from html.parser import HTMLParser

PLACEHOLDERS = ["lorem ipsum", "{{", "}}", "todo", "your text here", "xxx"]


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.viewport = False
        self.description = False
        self.title = ""
        self.in_title = False
        self.h1_count = 0
        self.in_h1 = False
        self.h1_text = ""
        self.section_ids = set()
        self.images_without_alt = 0
        self.empty_links = 0
        self.links = []
        self.external_requests = []
        self.text = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("style", "script"):
            self.skip += 1
        if tag == "meta":
            if a.get("name") == "viewport":
                self.viewport = True
            if a.get("name") == "description" and a.get("content"):
                self.description = True
        if tag == "title":
            self.in_title = True
        if tag == "h1":
            self.h1_count += 1
            self.in_h1 = True
        if tag == "section" and a.get("id"):
            self.section_ids.add(a["id"])
        if tag == "img" and not a.get("alt"):
            self.images_without_alt += 1
        if tag == "a":
            href = a.get("href", "")
            if href in ("", "#"):
                self.empty_links += 1
            self.links.append(href)
        if tag in ("script", "img", "link", "iframe"):
            src = a.get("src") or a.get("href") or ""
            if src.startswith("http"):
                self.external_requests.append(src)

    def handle_endtag(self, tag):
        if tag in ("style", "script") and self.skip:
            self.skip -= 1
        if tag == "title":
            self.in_title = False
        if tag == "h1":
            self.in_h1 = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if self.in_h1:
            self.h1_text += data
        if not self.skip:
            self.text.append(data)


def read_brief(path):
    brief = open(path, encoding="utf-8").read()
    sections = re.search(r"## Required sections.*?\n(.*?)\n##", brief, re.S)
    required = re.findall(r"^- (\S+)", sections.group(1), re.M) if sections else []
    banned = re.search(r"Words to avoid:\s*(.*)", brief)
    banned = [w.strip().lower() for w in banned.group(1).split(",") if w.strip()] if banned else []
    limit = re.search(r"Headline max words:\s*(\d+)", brief)
    limit = int(limit.group(1)) if limit else 10
    cta = re.search(r"CTA button text:\s*(.*)", brief)
    cta = cta.group(1).strip() if cta else ""
    return required, banned, limit, cta


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    page_path, brief_path = sys.argv[1], sys.argv[2]
    html = open(page_path, encoding="utf-8").read()
    required, banned, limit, cta = read_brief(brief_path)

    p = PageParser()
    p.feed(html)
    text = " ".join(p.text).lower()

    results = []

    def check(name, ok, detail=""):
        results.append((ok, name, detail))

    check("viewport meta tag (mobile)", p.viewport)
    check("title present", bool(p.title.strip()))
    check("meta description present", p.description)
    check("exactly one h1", p.h1_count == 1, f"found {p.h1_count}")
    words = len(p.h1_text.split())
    check(f"headline within {limit} words", 0 < words <= limit, f"{words} words")
    for sid in required:
        check(f"section #{sid} exists", sid in p.section_ids)
    check("all images have alt text", p.images_without_alt == 0, f"{p.images_without_alt} missing")
    check("no empty links", p.empty_links == 0, f"{p.empty_links} empty")
    check("no placeholder text", not any(x in text for x in PLACEHOLDERS))
    hits = [w for w in banned if w in text]
    check("no banned words", not hits, ", ".join(hits))
    check("CTA text appears at least twice", bool(cta) and text.count(cta.lower()) >= 2,
          f"'{cta}' x{text.count(cta.lower()) if cta else 0}")
    check("no external requests (self contained)", not p.external_requests,
          f"{len(p.external_requests)} found")
    check("no horizontal overflow rule (overflow-x hidden or max-width used)", "max-width" in html)

    failed = 0
    for ok, name, detail in results:
        if not ok:
            failed += 1
        print(("PASS  " if ok else "FAIL  ") + name + (f"  [{detail}]" if detail else ""))
    print(f"\n{len(results) - failed}/{len(results)} checks passed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
