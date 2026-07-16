const filterButtons = document.querySelectorAll("[data-filter]");
const serviceCards = document.querySelectorAll("[data-category]");
const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

filterButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const selected = button.dataset.filter;
    filterButtons.forEach((item) => {
      const active = item === button;
      item.classList.toggle("is-active", active);
      item.setAttribute("aria-pressed", String(active));
    });
    serviceCards.forEach((card) => {
      const shouldShow = selected === "all" || card.dataset.category === selected;
      card.getAnimations?.().forEach((animation) => animation.cancel());
      if (shouldShow) {
        card.hidden = false;
        if (!reduceMotion && card.animate) {
          card.animate(
            [
              { opacity: 0, transform: "translateY(14px) scale(.98)" },
              { opacity: 1, transform: "translateY(0) scale(1)" },
            ],
            { duration: 320, easing: "cubic-bezier(.2, .7, .2, 1)" },
          );
        }
      } else {
        card.hidden = true;
      }
    });
  });
});

const calculator = document.querySelector("[data-impact-calculator]");

if (calculator) {
  let activeRegion = window.NexoRegion?.current || "co";

  const updateEstimate = () => {
    const data = new FormData(calculator);
    const weeklyHours = Math.max(0, Number(data.get("hours")) || 0);
    const hourlyCost = Math.max(0, Number(data.get("hourly_cost")) || 0);
    const monthlyErrors = Math.max(0, Number(data.get("error_cost")) || 0);
    const annualHours = weeklyHours * 52;
    const annualOpportunity = annualHours * hourlyCost + monthlyErrors * 12;
    const config = window.NexoRegion?.config[activeRegion] || {
      locale: "es-CO",
      currency: "COP",
    };
    const formattedValue = window.NexoRegion
      ? window.NexoRegion.formatCurrency(annualOpportunity, activeRegion)
      : new Intl.NumberFormat(config.locale, {
          style: "currency",
          currency: config.currency,
          maximumFractionDigits: 0,
        }).format(annualOpportunity);
    calculator.querySelector("[data-impact-value]").textContent = formattedValue;
    calculator.querySelector("[data-impact-hours]").textContent = `${annualHours.toLocaleString(config.locale)} horas al año para revisar`;
  };

  const applyCalculatorRegion = (region) => {
    activeRegion = region === "pe" ? "pe" : "co";
    calculator.querySelectorAll("[data-co-value]").forEach((input) => {
      input.value = input.dataset[`${activeRegion}Value`];
    });
    updateEstimate();
  };

  calculator.addEventListener("input", updateEstimate);
  calculator.addEventListener("submit", (event) => event.preventDefault());
  window.addEventListener("nexo:region-change", (event) => {
    applyCalculatorRegion(event.detail.region);
  });
  applyCalculatorRegion(activeRegion);
}
