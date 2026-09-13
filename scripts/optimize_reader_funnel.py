#!/usr/bin/env python3
from pathlib import Path
import re

PAGES = {
    "books/the-hollow-bell.html": {
        "hook": "Twenty years after Marnie Renner vanished, her remains surface beneath the ice—and her sister comes home to find out who put her there.",
        "meta": "Twenty years after Marnie Renner vanished, her remains surface beneath the ice in Millbrook Falls. Read Chapter One and continue with Kindle Unlimited.",
        "og": "Marnie Renner vanished twenty years ago. Now her remains have surfaced beneath the ice, reopening the cold case her sister never escaped.",
        "twitter": "A twenty-year disappearance becomes a murder investigation when Marnie Renner's remains surface beneath the ice.",
        "trailer_h2": "See the cold case surface beneath the ice.",
        "trailer_copy": "Watch Claire return to Millbrook Falls as a twenty-year disappearance becomes a murder investigation.",
        "read_next": "the-correction.html",
        "read_next_title": "If the buried history of Millbrook Falls pulled you in, enter the Averill Falls archive next.",
        "read_next_copy": "In <em>The Correction</em>, altered records do more than change the official story—they change what a town remembers.",
        "read_next_button": "Read The Correction",
    },
    "books/second-draft.html": {
        "hook": "Nora helps people rehearse impossible conversations. Then the rehearsals start changing reality.",
        "meta": "Nora helps people rehearse the hardest conversations of their lives—until the rehearsals start changing reality. Read Chapter One and continue with Kindle Unlimited.",
        "og": "A private rehearsal should be practice. In Nora's sunporch, getting the details right can make the rehearsal become real.",
        "twitter": "Nora helps people rehearse impossible conversations. Then the rehearsals start changing reality.",
        "trailer_h2": "See what happens when rehearsal becomes too real.",
        "trailer_copy": "Watch Nora's listening room turn precise rehearsals into something much harder to explain.",
        "read_next": "the-hollow-year.html",
        "read_next_title": "If memory becoming unreliable kept you reading, visit Amity Hollow next.",
        "read_next_copy": "In <em>The Hollow Year</em>, one person is erased from every living memory each October—and one woman still remembers.",
        "read_next_button": "Read The Hollow Year",
    },
    "books/the-hollow-year.html": {
        "hook": "In Amity Hollow, one person is erased from every living memory each October.",
        "meta": "In Amity Hollow, one person is erased from every living memory each October—and one woman still remembers. Read Chapter One and continue with Kindle Unlimited.",
        "og": "Every October, Amity Hollow loses one person from every living memory. This year, Enid Marsh remembers who is missing.",
        "twitter": "Every October, Amity Hollow forgets one person. This year, Enid remembers.",
        "trailer_h2": "See what Amity Hollow has forgotten.",
        "trailer_copy": "Watch Enid discover that a missing brother is only the newest name a whole town has forgotten.",
        "read_next": "the-absconding.html",
        "read_next_title": "If a small town hiding an impossible pattern kept you reading, go to Sorrel Falls next.",
        "read_next_copy": "In <em>The Absconding</em>, a mother dies beside the family beehives, the hives go silent, and an old family ritual says the story is wrong.",
        "read_next_button": "Read The Absconding",
    },
    "books/the-absconding.html": {
        "hook": "Del comes home after her mother dies beside the family beehives. Then the hives fall silent—and an old family ritual suggests the story she's been told is wrong.",
        "meta": "After Del's mother dies beside the family beehives, the hives fall silent—and an old family ritual suggests the story she's been told is wrong. Read Chapter One and continue with Kindle Unlimited.",
        "og": "Del comes home after her mother dies beside the family beehives. Then the hives fall silent, and an old family ritual points toward a buried truth.",
        "twitter": "Her mother dies beside the beehives. The hives fall silent. An old family ritual says the story is wrong.",
        "trailer_h2": "See why the hives have fallen silent.",
        "trailer_copy": "Watch Del return to Sorrel Falls and discover that the bees may know when the story being told is false.",
        "read_next": "the-hollow-bell.html",
        "read_next_title": "If buried family history and small-town silence kept you reading, return to Millbrook Falls next.",
        "read_next_copy": "In <em>The Hollow Bell</em>, a twenty-year disappearance becomes a murder investigation when Marnie Renner's remains surface beneath the ice.",
        "read_next_button": "Read The Hollow Bell",
    },
    "books/the-correction.html": {
        "hook": "A correction slip changes more than the official record. It changes what Averill Falls remembers.",
        "meta": "A correction slip changes more than the official record—it changes what Averill Falls remembers. Read Chapter One and continue with Kindle Unlimited.",
        "og": "In the Averill Falls archive, changing the official record can change what an entire town remembers.",
        "twitter": "A correction slip changes more than the official record. It changes what Averill Falls remembers.",
        "trailer_h2": "See what happens when the archive rewrites memory.",
        "trailer_copy": "Watch a routine correction reveal that the official record can change what an entire town remembers.",
        "read_next": "second-draft.html",
        "read_next_title": "If changing memory unsettled you, step into a room where rehearsal can change reality.",
        "read_next_copy": "<em>Second Draft</em> follows private rehearsals so precise that the line between what might happen and what did begins to disappear.",
        "read_next_button": "Read Second Draft",
    },
}


def replace_meta(text: str, prop: str, value: str) -> str:
    if prop == "description":
        pattern = r'<meta name="description" content="[^"]*">'
        repl = f'<meta name="description" content="{value}">'
    elif prop == "og:description":
        pattern = r'<meta property="og:description" content="[^"]*">'
        repl = f'<meta property="og:description" content="{value}">'
    else:
        pattern = r'<meta name="twitter:description" content="[^"]*">'
        repl = f'<meta name="twitter:description" content="{value}">'
    return re.sub(pattern, repl, text, count=1)


def optimize(path: Path, cfg: dict) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text

    text = replace_meta(text, "description", cfg["meta"])
    text = replace_meta(text, "og:description", cfg["og"])
    text = replace_meta(text, "twitter:description", cfg["twitter"])
    text = re.sub(r'<p class="book-hook">.*?</p>', f'<p class="book-hook">{cfg["hook"]}</p>', text, count=1, flags=re.S)

    trailer_pattern = (
        r'(<section class="book-section"><div class="eyebrow">Official Book Trailer</div>)'
        r'<h2>.*?</h2><p class="section-copy">.*?</p>'
    )
    trailer_repl = (
        r'\1'
        + f'<h2>{cfg["trailer_h2"]}</h2>'
        + f'<p class="section-copy">{cfg["trailer_copy"]}</p>'
    )
    text = re.sub(trailer_pattern, trailer_repl, text, count=1, flags=re.S)

    if 'id="read-next"' not in text:
        read_next = (
            '<section class="book-section" id="read-next">'
            '<div class="eyebrow">Read Next</div>'
            f'<h2>{cfg["read_next_title"]}</h2>'
            f'<p class="section-copy">{cfg["read_next_copy"]}</p>'
            f'<p><a class="cta solid" href="{cfg["read_next"]}" data-track="read_next">{cfg["read_next_button"]}</a></p>'
            '</section>\n'
        )
        marker = '<section class="book-section"><div class="eyebrow">More JayTree Mysteries</div>'
        if marker not in text:
            raise RuntimeError(f"Related-books marker not found in {path}")
        text = text.replace(marker, read_next + marker, 1)

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = []
    for filename, cfg in PAGES.items():
        path = Path(filename)
        if not path.exists():
            raise FileNotFoundError(filename)
        if optimize(path, cfg):
            changed.append(filename)
    print("Reader funnel optimization complete.")
    for item in changed:
        print(f"UPDATED {item}")
    if not changed:
        print("No changes needed; pages are already optimized.")


if __name__ == "__main__":
    main()
