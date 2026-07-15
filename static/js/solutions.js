const filterButtons = document.querySelectorAll("[data-filter]");
const serviceCards = document.querySelectorAll("[data-category]");

filterButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const selected = button.dataset.filter;
    filterButtons.forEach((item) => {
      const active = item === button;
      item.classList.toggle("is-active", active);
      item.setAttribute("aria-pressed", String(active));
    });
    serviceCards.forEach((card) => {
      card.hidden = selected !== "all" && card.dataset.category !== selected;
    });
  });
});

const calculator = document.querySelector("[data-impact-calculator]");

if (calculator) {
  const currency = new Intl.NumberFormat("es-CO", {
    style: "currency",
    currency: "COP",
    maximumFractionDigits: 0,
  });

  const updateEstimate = () => {
    const data = new FormData(calculator);
    const weeklyHours = Math.max(0, Number(data.get("hours")) || 0);
    const hourlyCost = Math.max(0, Number(data.get("hourly_cost")) || 0);
    const monthlyErrors = Math.max(0, Number(data.get("error_cost")) || 0);
    const annualHours = weeklyHours * 52;
    const annualOpportunity = annualHours * hourlyCost + monthlyErrors * 12;
    calculator.querySelector("[data-impact-value]").textContent = currency.format(annualOpportunity);
    calculator.querySelector("[data-impact-hours]").textContent = `${annualHours.toLocaleString("es-CO")} horas al año para revisar`;
  };

  calculator.addEventListener("input", updateEstimate);
  calculator.addEventListenen("submit", (event) => event.preventDefault());
  updateEstimate();
}
