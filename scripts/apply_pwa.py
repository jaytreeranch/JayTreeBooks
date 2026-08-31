#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
ICONS = ROOT / "icons"

PWA_HEAD_START = "<!-- JAYTREE_PWA_HEAD_START -->"
PWA_HEAD_END = "<!-- JAYTREE_PWA_HEAD_END -->"
PWA_SCRIPT_START = "<!-- JAYTREE_PWA_SCRIPT_START -->"
PWA_SCRIPT_END = "<!-- JAYTREE_PWA_SCRIPT_END -->"

PWA_HEAD = f"""{PWA_HEAD_START}
<link rel="manifest" href="/manifest.webmanifest">
<link rel="apple-touch-icon" sizes="180x180" href="/icons/apple-touch-icon.png">
<meta name="theme-color" content="#080d12">
<meta name="application-name" content="JayTree Books">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="JayTree Books">
<link rel="stylesheet" href="/pwa.css">
{PWA_HEAD_END}"""

PWA_SCRIPT = f"""{PWA_SCRIPT_START}
<script src="/pwa.js" defer></script>
{PWA_SCRIPT_END}"""

MANIFEST = {
    "id": "/",
    "name": "JayTree Books",
    "short_name": "JayTree",
    "description": "Mystery thrillers, audiobooks, trailers, and interactive Mystery Challenges from JayTree Books.",
    "start_url": "/",
    "scope": "/",
    "display": "standalone",
    "background_color": "#080d12",
    "theme_color": "#080d12",
    "lang": "en-US",
    "orientation": "any",
    "prefer_related_applications": False,
    "categories": ["books", "entertainment"],
    "icons": [
        {
            "src": "/icons/icon-192.png",
            "sizes": "192x192",
            "type": "image/png",
            "purpose": "any",
        },
        {
            "src": "/icons/icon-512.png",
            "sizes": "512x512",
            "type": "image/png",
            "purpose": "any",
        },
        {
            "src": "/icons/icon-512.png",
            "sizes": "512x512",
            "type": "image/png",
            "purpose": "maskable",
        },
    ],
    "shortcuts": [
        {"name": "Books", "short_name": "Books", "url": "/#books"},
        {"name": "Mystery Challenge", "short_name": "Challenge", "url": "/#challenge"},
        {"name": "Audiobooks", "short_name": "Audiobooks", "url": "/#audiobooks"},
    ],
}

PWA_CSS = r"""
.pwa-install-button{
  position:fixed;right:18px;bottom:18px;z-index:80;
  border:1px solid #c8a15a;background:#c8a15a;color:#080d12;
  padding:12px 16px;font:700 .72rem/1.1 Arial,sans-serif;
  letter-spacing:.11em;text-transform:uppercase;cursor:pointer;
  box-shadow:0 12px 34px rgba(0,0,0,.38)
}
.pwa-install-button:hover{filter:brightness(1.06)}
.pwa-install-help{
  position:fixed;right:18px;bottom:70px;z-index:81;width:min(340px,calc(100vw - 36px));
  background:#101920;color:#e8dfcc;border:1px solid rgba(200,161,90,.7);
  box-shadow:0 18px 48px rgba(0,0,0,.52);padding:18px
}
.pwa-install-help strong{display:block;color:#c8a15a;margin-bottom:8px}
.pwa-install-help p{margin:0 0 12px;color:#c9c4b8;font:400 .92rem/1.5 Arial,sans-serif}
.pwa-install-help button{
  border:1px solid #c8a15a;background:transparent;color:#e8dfcc;
  padding:8px 11px;cursor:pointer;text-transform:uppercase;letter-spacing:.08em;font-size:.68rem
}
@media(max-width:600px){
  .pwa-install-button{right:12px;bottom:12px}
  .pwa-install-help{right:12px;bottom:64px;width:calc(100vw - 24px)}
}
@media(display-mode:standalone){
  .pwa-install-button,.pwa-install-help{display:none!important}
}
""".strip() + "\n"

PWA_JS = r"""(() => {
  const standalone = () =>
    window.matchMedia?.("(display-mode: standalone)")?.matches ||
    window.navigator.standalone === true;

  const isIOS = () =>
    /iphone|ipad|ipod/i.test(navigator.userAgent) ||
    (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1);

  const track = (eventName, params = {}) => {
    if (typeof window.gtag === "function") {
      window.gtag("event", eventName, params);
    }
  };

  if ("serviceWorker" in navigator) {
    window.addEventListener("load", () => {
      navigator.serviceWorker.register("/service-worker.js", { scope: "/" })
        .catch(error => console.warn("JayTree PWA service worker registration failed:", error));
    });
  }

  if (standalone()) return;

  let deferredPrompt = null;
  let installButton = null;
  let helpPanel = null;

  const removeHelp = () => {
    helpPanel?.remove();
    helpPanel = null;
  };

  const showHelp = (message) => {
    removeHelp();
    helpPanel = document.createElement("div");
    helpPanel.className = "pwa-install-help";
    helpPanel.setAttribute("role", "dialog");
    helpPanel.setAttribute("aria-label", "Install JayTree Books");
    helpPanel.innerHTML = `
      <strong>Install JayTree Books</strong>
      <p>${message}</p>
      <button type="button">Close</button>
    `;
    helpPanel.querySelector("button")?.addEventListener("click", removeHelp);
    document.body.appendChild(helpPanel);
  };

  const ensureButton = () => {
    if (installButton || standalone()) return;
    installButton = document.createElement("button");
    installButton.type = "button";
    installButton.className = "pwa-install-button";
    installButton.textContent = "Install App";
    installButton.setAttribute("aria-label", "Install JayTree Books app");

    installButton.addEventListener("click", async () => {
      if (deferredPrompt) {
        deferredPrompt.prompt();
        const choice = await deferredPrompt.userChoice;
        track("pwa_install_prompt", { outcome: choice.outcome });
        if (choice.outcome === "accepted") {
          installButton?.remove();
          installButton = null;
        }
        deferredPrompt = null;
        return;
      }

      if (isIOS()) {
        track("pwa_ios_install_help");
        showHelp("Tap the Share button in your browser, then choose “Add to Home Screen.”");
        return;
      }

      track("pwa_install_help");
      showHelp("Open your browser menu and choose Install app or Add to Home screen.");
    });

    document.body.appendChild(installButton);
  };

  window.addEventListener("beforeinstallprompt", event => {
    event.preventDefault();
    deferredPrompt = event;
    ensureButton();
    track("pwa_install_available");
  });

  window.addEventListener("appinstalled", () => {
    track("pwa_installed");
    installButton?.remove();
    installButton = null;
    removeHelp();
    deferredPrompt = null;
  });

  const ready = () => {
    if (isIOS() && !standalone()) ensureButton();
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", ready, { once: true });
  } else {
    ready();
  }
})();
"""

SERVICE_WORKER = r"""const CACHE_NAME = "jaytree-pwa-v1";
const CORE = [
  "/",
  "/manifest.webmanifest",
  "/pwa.css",
  "/pwa.js",
  "/icons/icon-192.png",
  "/icons/icon-512.png"
];

self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache =>
      Promise.allSettled(CORE.map(url => cache.add(url)))
    ).then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(key => key.startsWith("jaytree-pwa-") && key !== CACHE_NAME).map(key => caches.delete(key))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", event => {
  const request = event.request;
  if (request.method !== "GET") return;

  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return;

  event.respondWith(
    fetch(request)
      .then(response => {
        if (response && response.ok) {
          const copy = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(request, copy));
        }
        return response;
      })
      .catch(async () => {
        const cached = await caches.match(request);
        if (cached) return cached;
        if (request.mode === "navigate") {
          const home = await caches.match("/");
          if (home) return home;
        }
        return new Response("JayTree Books is temporarily offline.", {
          status: 503,
          headers: { "Content-Type": "text/plain; charset=utf-8" }
        });
      })
  );
});
"""


def replace_marker_block(text: str, start: str, end: str, block: str) -> str:
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    if pattern.search(text):
        return pattern.sub(lambda _: block, text)
    return text


def patch_html(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text

    text = re.sub(r'\s*<link\b[^>]*rel=["\']apple-touch-icon["\'][^>]*>\s*', "\n", text, flags=re.IGNORECASE)

    if PWA_HEAD_START in text:
        text = replace_marker_block(text, PWA_HEAD_START, PWA_HEAD_END, PWA_HEAD)
    elif "</head>" in text:
        text = text.replace("</head>", PWA_HEAD + "\n</head>", 1)

    if PWA_SCRIPT_START in text:
        text = replace_marker_block(text, PWA_SCRIPT_START, PWA_SCRIPT_END, PWA_SCRIPT)
    elif "</body>" in text:
        text = text.replace("</body>", PWA_SCRIPT + "\n</body>", 1)

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def html_targets() -> list[Path]:
    paths = set(ROOT.glob("*.html"))
    for folder in ("books", "chapters", "audio"):
        directory = ROOT / folder
        if directory.exists():
            paths.update(directory.glob("*.html"))
    return sorted(paths)


def make_icon(size: int) -> Image.Image:
    bg = (8, 13, 18)
    gold = (200, 161, 90)
    cream = (232, 223, 204)

    image = Image.new("RGB", (size, size), bg)
    draw = ImageDraw.Draw(image)
    scale = size / 512
    cx = size / 2

    margin = int(62 * scale)
    radius = int(78 * scale)
    stroke = max(3, int(10 * scale))
    draw.rounded_rectangle(
        [margin, margin, size - margin, size - margin],
        radius=radius,
        outline=gold,
        width=stroke,
    )

    y_mid = 332 * scale
    y_top = 282 * scale
    y_bottom = 380 * scale
    left = [
        (cx - 14 * scale, y_mid),
        (cx - 72 * scale, y_top),
        (cx - 154 * scale, y_top + 22 * scale),
        (cx - 134 * scale, y_bottom),
        (cx - 52 * scale, y_bottom - 18 * scale),
        (cx, y_mid + 24 * scale),
    ]
    right = [
        (cx + 14 * scale, y_mid),
        (cx + 72 * scale, y_top),
        (cx + 154 * scale, y_top + 22 * scale),
        (cx + 134 * scale, y_bottom),
        (cx + 52 * scale, y_bottom - 18 * scale),
        (cx, y_mid + 24 * scale),
    ]
    draw.line(left, fill=cream, width=max(4, int(12 * scale)), joint="curve")
    draw.line(right, fill=cream, width=max(4, int(12 * scale)), joint="curve")
    draw.line([(cx, y_mid + 20 * scale), (cx, y_bottom - 18 * scale)], fill=gold, width=max(3, int(8 * scale)))

    draw.line([(cx, y_mid + 8 * scale), (cx, 158 * scale)], fill=gold, width=max(6, int(18 * scale)))
    for start, end in [
        ((cx, 205 * scale), (cx - 78 * scale, 162 * scale)),
        ((cx, 220 * scale), (cx + 84 * scale, 171 * scale)),
        ((cx, 183 * scale), (cx - 46 * scale, 133 * scale)),
        ((cx, 188 * scale), (cx + 54 * scale, 130 * scale)),
        ((cx, 245 * scale), (cx - 96 * scale, 216 * scale)),
        ((cx, 248 * scale), (cx + 98 * scale, 220 * scale)),
    ]:
        draw.line([start, end], fill=gold, width=max(4, int(12 * scale)))

    for dx, dy, radius_leaf in [
        (-92, 150, 33), (-55, 124, 28), (-10, 115, 31), (38, 122, 28), (82, 152, 34),
        (-105, 205, 27), (-62, 188, 31), (-18, 172, 26), (25, 176, 28), (70, 190, 31), (106, 211, 26),
    ]:
        x = cx + dx * scale
        y = dy * scale
        r = radius_leaf * scale
        draw.ellipse([x - r, y - r, x + r, y + r], fill=gold)

    draw.ellipse([cx - 10 * scale, 145 * scale, cx + 10 * scale, 165 * scale], fill=cream)
    return image


def write_icons() -> None:
    ICONS.mkdir(parents=True, exist_ok=True)
    icon512 = make_icon(512)
    icon512.save(ICONS / "icon-512.png", "PNG", optimize=True)
    icon512.resize((192, 192), Image.Resampling.LANCZOS).save(ICONS / "icon-192.png", "PNG", optimize=True)
    icon512.resize((180, 180), Image.Resampling.LANCZOS).save(ICONS / "apple-touch-icon.png", "PNG", optimize=True)


def write_assets() -> None:
    (ROOT / "manifest.webmanifest").write_text(
        json.dumps(MANIFEST, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (ROOT / "pwa.css").write_text(PWA_CSS, encoding="utf-8")
    (ROOT / "pwa.js").write_text(PWA_JS, encoding="utf-8")
    (ROOT / "service-worker.js").write_text(SERVICE_WORKER, encoding="utf-8")
    write_icons()


def main() -> None:
    write_assets()
    changed = 0
    for path in html_targets():
        if patch_html(path):
            changed += 1
            print(f"PWA enabled: {path.relative_to(ROOT)}")
    print(f"JayTree Books PWA assets written; {changed} HTML file(s) updated.")


if __name__ == "__main__":
    main()
