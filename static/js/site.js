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
  selector.addEventListener("change", () => applyRegion(selector.value));
});

countryField?.addEventListener("change", () => applyRegion(countryField.value));

const revealTargets = document.querySelectorAll(
  "main > section:not(.signal-bar), .service-tile, .sector-grid article, .method-steps li, " +
    ".catalog-card, .case-card, .pricing-card, .principle-grid article, .stack-grid article, .related-grid a",
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
  document.querySelectorAll(".service-tile, .catalog-card, .pricing-card").forEach((surface) => {
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
