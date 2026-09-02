(() => {
  const standalone = () =>
    window.matchMedia?.("(display-mode: standalone)")?.matches ||
    window.navigator.standalone === true;

  const isIOS = () =>
    /iphone|ipad|ipod/i.test(navigator.userAgent) ||
    (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1);

  const track = (eventName, params = {}) => {
    if (typeof window.gtag === "function") window.gtag("event", eventName, params);
  };

  const chicagoNowKey = () => {
    const parts = new Intl.DateTimeFormat("en-US", {
      timeZone: "America/Chicago",
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
      hour: "2-digit",
      hour12: false
    }).formatToParts(new Date());
    const values = Object.fromEntries(parts.map(part => [part.type, part.value]));
    return `${values.year}-${values.month}-${values.day}T${values.hour}`;
  };

  const updateMysteryCaseLaunch = () => {
    const challenge = document.getElementById("challenge");
    if (!challenge) return;
    const launchLabel = challenge.querySelector(".coming-soon");
    const heading = challenge.querySelector(".challenge-copy h2");
    const note = challenge.querySelector(".challenge-note");
    const primary = challenge.querySelector(".challenge-copy .hero-actions .cta.solid");
    const launched = chicagoNowKey() >= "2026-09-06T19";

    if (launched) {
      if (launchLabel) launchLabel.textContent = "Case #001 Is Now Open";
      if (heading) heading.textContent = "Can you solve Mystery Case #001 before the reveal?";
      if (note) note.textContent = "The full Case File #001 is now live. Study the evidence, choose your suspect, and lock in your theory before the reveal.";
      if (primary) {
        primary.textContent = "Watch Case #001";
        primary.href = "https://www.youtube.com/@JayTreeBooks";
        primary.target = "_blank";
        primary.rel = "noopener";
        primary.dataset.event = "challenge_case_001_youtube";
      }
    } else {
      if (launchLabel) launchLabel.textContent = "Case #001 Premieres Sunday, September 6 • 7 PM CT";
      if (heading) heading.textContent = "Mystery Case #001 opens this Sunday.";
      if (note) note.textContent = "The full Case File #001 challenge premieres Sunday, September 6 at 7 PM CT. Watch Teaser #3 now and be ready to lock in your theory before the reveal.";
    }
  };

  if ("serviceWorker" in navigator) {
    window.addEventListener("load", () => {
      navigator.serviceWorker.register("/service-worker.js", { scope: "/" })
        .catch(error => console.warn("JayTree PWA service worker registration failed:", error));
    });
  }

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
    updateMysteryCaseLaunch();
    if (isIOS() && !standalone()) ensureButton();
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", ready, { once: true });
  } else {
    ready();
  }
})();
