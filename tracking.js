(() => {
  "use strict";

  const STORAGE_KEY = "jt_campaign_attribution_v1";
  const UTM_KEYS = [
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_content",
    "utm_term",
    "utm_id"
  ];

  function safeRead() {
    try {
      const raw = sessionStorage.getItem(STORAGE_KEY);
      return raw ? JSON.parse(raw) : {};
    } catch (_) {
      return {};
    }
  }

  function safeWrite(value) {
    try {
      sessionStorage.setItem(STORAGE_KEY, JSON.stringify(value));
    } catch (_) {}
  }

  const params = new URLSearchParams(window.location.search);
  const incoming = {};
  UTM_KEYS.forEach(key => {
    const value = params.get(key);
    if (value) incoming[key] = value;
  });

  let attribution = safeRead();
  if (Object.keys(incoming).length) {
    attribution = {
      ...incoming,
      entry_path: window.location.pathname,
      entry_time: new Date().toISOString()
    };
    safeWrite(attribution);
  }

  function enrich(extra = {}) {
    const base = {};
    if (attribution.utm_source) base.campaign_source = attribution.utm_source;
    if (attribution.utm_medium) base.campaign_medium = attribution.utm_medium;
    if (attribution.utm_campaign) base.campaign_name = attribution.utm_campaign;
    if (attribution.utm_content) base.campaign_content = attribution.utm_content;
    if (attribution.utm_term) base.campaign_term = attribution.utm_term;
    if (attribution.utm_id) base.campaign_id = attribution.utm_id;
    if (attribution.entry_path) base.entry_path = attribution.entry_path;
    return Object.assign(base, extra || {});
  }

  window.JTTracking = {
    attribution,
    enrich
  };

  const rawGtag = window.gtag;
  if (typeof rawGtag !== "function" || rawGtag.__jaytreeWrapped) return;

  const readerStartEvents = new Set([
    "chapter",
    "featured_chapter"
  ]);

  const readIntentEvents = new Set([
    "kindle_unlimited",
    "chapter_kindle_unlimited",
    "featured_kindle_unlimited",
    "amazon",
    "ku_home_amazon",
    "ku_author_page"
  ]);

  const challengeEvents = new Set([
    "challenge_current_youtube",
    "challenge_reveal_youtube"
  ]);

  function sendDerived(name, sourceEvent, eventParams) {
    const derived = enrich(Object.assign({}, eventParams || {}, {
      source_event: sourceEvent,
      transport_type: "beacon"
    }));
    rawGtag("event", name, derived);
  }

  function wrappedGtag() {
    const args = Array.from(arguments);
    if (args[0] === "event") {
      const eventName = String(args[1] || "");
      const eventParams =
        args[2] && typeof args[2] === "object" && !Array.isArray(args[2])
          ? args[2]
          : {};

      args[2] = enrich(eventParams);
      rawGtag.apply(window, args);

      if (readerStartEvents.has(eventName)) {
        sendDerived("reader_start", eventName, eventParams);
      } else if (readIntentEvents.has(eventName)) {
        sendDerived("outbound_read_intent", eventName, eventParams);
      } else if (eventName === "case_files_signup_submit") {
        sendDerived("generate_lead", eventName, Object.assign({}, eventParams, {
          lead_type: "jaytree_case_files"
        }));
      } else if (eventName === "case_files_signup_complete") {
        sendDerived("sign_up", eventName, Object.assign({}, eventParams, {
          method: "kit",
          list_name: "jaytree_case_files"
        }));
      } else if (challengeEvents.has(eventName)) {
        sendDerived("mystery_challenge_action", eventName, eventParams);
      }
      return;
    }
    return rawGtag.apply(window, args);
  }

  wrappedGtag.__jaytreeWrapped = true;
  wrappedGtag.__jaytreeOriginal = rawGtag;
  window.gtag = wrappedGtag;

  if (Object.keys(incoming).length) {
    window.gtag("event", "campaign_landing", {
      landing_path: window.location.pathname,
      landing_title: document.title || "",
      transport_type: "beacon"
    });
  }
})();
