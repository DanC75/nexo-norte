const menuButton = document.querySelector(".menu-toggle");
const navigation = document.querySelector(".site-nav");
const navigationShell = document.querySelector(".navigation-shell");
const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const regionConfig = {
  co: { locale: "es-CO", currency: "COP", country: "Colombia" },
  pe: { locale: "es-PE", currency: "PEN", country: "Perú" },
};

const readSavedRegion = () => {
  try {
    return localStorage.getItem("nexo-region");
  } catch {
    return null;
  }
};

const saveRegion = (region) => {
  try {
    localStorage.setItem("nexo-region", region);
  } catch {
    // The preference remains active for this page when storage is unavailable.
  }
};

const readRegionDecision = () => {
  try {
    return localStorage.getItem("nexo-region-confirmed");
  } catch {
    return null;
  }
};

const confirmRegion = (region) => {
  try {
    localStorage.setItem("nexo-region-confirmed", region);
  } catch {
    // The dialog can still close normally when storage is unavailable.
  }
};

const detectBrowserRegion = () => {
  const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
  const languages = navigator.languages?.length ? navigator.languages : [navigator.language];

  if (timezone === "America/Lima") return "pe";
  if (timezone === "America/Bogota") return "co";
  if (languages.some((language) => /^es-PE\b/i.test(language))) return "pe";
  if (languages.some((language) => /^es-CO\b/i.test(language))) return "co";
  return null;
};

const applyRegion = (requestedRegion, persist = true) => {
  const region = regionConfig[requestedRegion] ? requestedRegion : "co";
  document.documentElement.dataset.region = region;

  document.querySelectorAll("[data-region-selector]").forEach((selector) => {
    selector.value = region;
  });
  document.querySelectorAll("[data-region-text]").forEach((element) => {
    const localizedText = element.dataset[region];
    if (localizedText) element.textContent = localizedText;
  });

  const countryField = document.querySelector("[data-country-sync]");
  if (countryField) countryField.value = region;
  if (persist) saveRegion(region);

  window.NexoRegion.current = region;
  window.dispatchEvent(
    new CustomEvent("nexo:region-change", { detail: { region, ...regionConfig[region] } }),
  );
};

window.NexoRegion = {
  config: regionConfig,
  current: "co",
  apply: applyRegion,
  formatCurrency(value, region = window.NexoRegion.current) {
    const config = regionConfig[region] || regionConfig.co;
    return new Intl.NumberFormat(config.locale, {
      style: "currency",
      currency: config.currency,
      maximumFractionDigits: 0,
    }).format(value);
  },
};

const countryField = document.querySelector("[data-country-sync]");
const initialRegion = readSavedRegion() || countryField?.value || "co";
applyRegion(initialRegion, false);

document.querySelectorAll("[data-region-selector]").forEach((selector) => {
  selector.addEventListener("change", () => {
    applyRegion(selector.value);
    confirmRegion(selector.value);
  });
});

countryField?.addEventListener("change", () => applyRegion(countryField.value));

const submissionDialog = document.querySelector("[data-submission-dialog]");
const regionDialog = document.querySelector("[data-region-dialog]");
const detectedRegion = detectBrowserRegion();

const closeRegionDialog = () => {
  if (!regionDialog?.open) return;
  if (typeof regionDialog.close === "function") regionDialog.close();
  else regionDialog.removeAttribute("open");
};

if (
  regionDialog &&
  !submissionDialog &&
  detectedRegion &&
  detectedRegion !== window.NexoRegion.current &&
  !readRegionDecision()
) {
  const detectedCountry = regionConfig[detectedRegion].country;
  const currentCountry = regionConfig[window.NexoRegion.current].country;
  regionDialog.querySelectorAll("[data-detected-country]").forEach((element) => {
    element.textContent = detectedCountry;
  });
  regionDialog.querySelectorAll("[data-current-country]").forEach((element) => {
    element.textContent = currentCountry;
  });

  window.setTimeout(() => {
    if (detectedRegion === window.NexoRegion.current || readRegionDecision()) return;
    if (typeof regionDialog.showModal === "function") regionDialog.showModal();
    else regionDialog.setAttribute("open", "");
  }, prefersReducedMotion ? 0 : 450);

  regionDialog.querySelector("[data-region-accept]").addEventListener("click", () => {
    applyRegion(detectedRegion);
    confirmRegion(detectedRegion);
    closeRegionDialog();
  });
  regionDialog.querySelector("[data-region-stay]").addEventListener("click", () => {
    confirmRegion(window.NexoRegion.current);
    closeRegionDialog();
  });
}

if (submissionDialog) {
  const countdown = submissionDialog.querySelector("[data-redirect-countdown]");
  const stayButton = submissionDialog.querySelector("[data-stay-on-contact]");
  const homeUrl = submissionDialog.dataset.homeUrl;
  let remainingSeconds = 7;
  let redirectTimer = null;

  const stopRedirect = () => {
    if (redirectTimer) window.clearInterval(redirectTimer);
    redirectTimer = null;
  };

  const closeSubmissionDialog = () => {
    stopRedirect();
    if (submissionDialog.open && typeof submissionDialog.close === "function") {
      submissionDialog.close();
    } else {
      submissionDialog.removeAttribute("open");
    }
  };

  const returnHome = () => {
    closeSubmissionDialog();
    window.location.assign(homeUrl);
  };

  window.setTimeout(() => {
    if (typeof submissionDialog.showModal === "function") submissionDialog.showModal();
    else submissionDialog.setAttribute("open", "");
  }, prefersReducedMotion ? 0 : 180);

  redirectTimer = window.setInterval(() => {
    remainingSeconds -= 1;
    countdown.textContent = String(remainingSeconds);
    if (remainingSeconds <= 0) returnHome();
  }, 1000);

  stayButton.addEventListener("click", closeSubmissionDialog);
  submissionDialog.addEventListener("close", stopRedirect);
  window.addEventListener("pagehide", stopRedirect, { once: true });
}

const revealTargets = document.querySelectorAll(
  "main > section, .catalog-card, .case-card, .pricing-card, .principle-grid article, " +
    ".stack-grid article, .related-grid a",
);

revealTargets.forEach((target) => target.classList.add("reveal-item"));

if (prefersReducedMotion || !("IntersectionObserver" in window)) {
  revealTargets.forEach((target) => target.classList.add("is-visible"));
} else {
  const revealObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          revealObserver.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: "0px 0px -36px" },
  );

  revealTargets.forEach((target) => revealObserver.observe(target));
}

document.documentElement.classList.add("motion-ready");

window.addEventListener("pageshow", (event) => {
  if (!event.persisted || prefersReducedMotion) return;
  document.body.classList.remove("page-restored");
  requestAnimationFrame(() => document.body.classList.add("page-restored"));
});

const scrollProgress = document.querySelector("[data-scroll-progress]");
const heroGrid = document.querySelector(".hero-grid");
let scrollFrame = null;

const updateScrollEffects = () => {
  const scrollTop = window.scrollY;
  const scrollableHeight = document.documentElement.scrollHeight - window.innerHeight;
  const progress = scrollableHeight > 0 ? Math.min(1, scrollTop / scrollableHeight) : 0;
  navigationShell?.classList.toggle("is-scrolled", scrollTop > 12);
  scrollProgress?.style.setProperty("--scroll-progress", progress);
  if (heroGrid && !prefersReducedMotion) {
    heroGrid.style.setProperty("--hero-shift", `${Math.min(70, scrollTop * 0.08)}px`);
  }
  scrollFrame = null;
};

const requestScrollUpdate = () => {
  if (scrollFrame === null) scrollFrame = requestAnimationFrame(updateScrollEffects);
};

updateScrollEffects();
window.addEventListener("scroll", requestScrollUpdate, { passive: true });

if (!prefersReducedMotion && window.matchMedia("(pointer: fine)").matches) {
  document.querySelectorAll(".catalog-card, .pricing-card").forEach((surface) => {
    surface.classList.add("motion-surface");
    surface.addEventListener("pointermove", (event) => {
      const bounds = surface.getBoundingClientRect();
      surface.style.setProperty("--spot-x", `${event.clientX - bounds.left}px`);
      surface.style.setProperty("--spot-y", `${event.clientY - bounds.top}px`);
    });
    surface.addEventListener("pointerleave", () => {
      surface.style.removeProperty("--spot-x");
      surface.style.removeProperty("--spot-y");
    });
  });
}

if (menuButton && navigation) {
  menuButton.addEventListener("click", () => {
    const isOpen = menuButton.getAttribute("aria-expanded") === "true";
    menuButton.setAttribute("aria-expanded", String(!isOpen));
    menuButton.querySelector(".sr-only").textContent = isOpen ? "Abrir menú" : "Cerrar menú";
    navigation.classList.toggle("is-open", !isOpen);
  });

  navigation.addEventListener("click", (event) => {
    if (event.target.closest("a")) {
      menuButton.setAttribute("aria-expanded", "false");
      menuButton.querySelector(".sr-only").textContent = "Abrir menú";
      navigation.classList.remove("is-open");
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && navigation.classList.contains("is-open")) {
      menuButton.setAttribute("aria-expanded", "false");
      menuButton.querySelector(".sr-only").textContent = "Abrir menú";
      navigation.classList.remove("is-open");
      menuButton.focus();
    }
  });

  window.addEventListener("resize", () => {
    if (window.innerWidth > 900) {
      menuButton.setAttribute("aria-expanded", "false");
      menuButton.querySelector(".sr-only").textContent = "Abrir menú";
      navigation.classList.remove("is-open");
    }
  });
}
