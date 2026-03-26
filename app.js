const catalog = window.initialCatalog || [];
const select = document.getElementById("tool-select");
const quickTools = document.getElementById("quick-tools");

const bindings = {
  code: document.getElementById("tool-code"),
  name: document.getElementById("tool-name"),
  product: document.getElementById("product-line"),
  cycle: document.getElementById("cycle-time"),
  weight: document.getElementById("piece-weight"),
  scrap: document.getElementById("scrap"),
  pieceTime: document.getElementById("piece-time"),
  temperature: document.getElementById("temperature"),
  pressure: document.getElementById("pressure"),
  speed: document.getElementById("speed"),
  notes: document.getElementById("notes"),
};

function findTool(code) {
  return catalog.find((tool) => tool.code === code);
}

function updateQuickButtons(code) {
  document.querySelectorAll(".quick-tool").forEach((button) => {
    button.classList.toggle("active", button.dataset.code === code);
  });
}

function renderTool(code) {
  const tool = findTool(code);
  if (!tool) return;

  bindings.code.textContent = tool.code;
  bindings.name.textContent = tool.name;
  bindings.product.textContent = tool.product;
  bindings.cycle.textContent = `${tool.cycle_time_seconds} s`;
  bindings.weight.textContent = `${tool.piece_weight_grams} g`;
  bindings.scrap.textContent = `${tool.expected_scrap_percent}%`;
  bindings.pieceTime.textContent = `${tool.time_per_piece_seconds} s`;
  bindings.temperature.textContent = tool.machine_parameters.temperature;
  bindings.pressure.textContent = tool.machine_parameters.pressure;
  bindings.speed.textContent = tool.machine_parameters.speed;
  bindings.notes.textContent = tool.operational_notes;
  select.value = tool.code;
  updateQuickButtons(tool.code);
}

select?.addEventListener("change", (event) => {
  renderTool(event.target.value);
});

quickTools?.addEventListener("click", (event) => {
  const button = event.target.closest(".quick-tool");
  if (!button) return;
  renderTool(button.dataset.code);
});
