const exhibitionList = document.querySelector("#exhibitions");
const slotSelect = document.querySelector("#slot");
const reserveForm = document.querySelector("#reserve-form");
const cancelForm = document.querySelector("#cancel-form");

async function request(url, options) {
  const response = await fetch(url, options);
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || "No se pudo completar la solicitud.");
  return data;
}

function showMessage(id, text, isError = false) {
  const element = document.querySelector(id);
  element.textContent = text;
  element.classList.toggle("error", isError);
}

async function loadContent() {
  const [exhibitions, slots] = await Promise.all([
    request("/api/exhibitions"),
    request("/api/slots"),
  ]);
  exhibitionList.replaceChildren();
  for (const exhibition of exhibitions) {
    const card = document.createElement("article");
    card.className = "card";
    const label = document.createElement("span");
    label.className = "card-label";
    label.textContent = `EXPOSICIÓN ${String(exhibition.id).padStart(2, "0")}`;
    const heading = document.createElement("h3");
    heading.textContent = exhibition.title;
    const description = document.createElement("p");
    description.textContent = exhibition.description;
    card.append(label, heading, description);
    exhibitionList.append(card);
  }
  if (!exhibitions.length) exhibitionList.textContent = "No hay exposiciones activas.";

  slotSelect.replaceChildren();
  const initial = document.createElement("option");
  initial.value = "";
  initial.textContent = "Selecciona un horario";
  slotSelect.append(initial);
  for (const slot of slots) {
    if (slot.available < 1) continue;
    const option = document.createElement("option");
    option.value = slot.id;
    option.textContent = `${slot.exhibition_title} · ${slot.visit_date} ${slot.start_time} · ${slot.available} cupos`;
    slotSelect.append(option);
  }
}

reserveForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const values = Object.fromEntries(new FormData(reserveForm));
  try {
    const result = await request("/api/reservations", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(values),
    });
    showMessage("#reserve-message", `Reserva confirmada. Guarda tu código: ${result.code}`);
    reserveForm.reset();
    await loadContent();
  } catch (error) {
    showMessage("#reserve-message", error.message, true);
  }
});

cancelForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const values = Object.fromEntries(new FormData(cancelForm));
  try {
    await request("/api/reservations/cancel", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(values),
    });
    showMessage("#cancel-message", "Reserva cancelada. El cupo quedó disponible de nuevo.");
    cancelForm.reset();
    await loadContent();
  } catch (error) {
    showMessage("#cancel-message", error.message, true);
  }
});

loadContent().catch((error) => {
  exhibitionList.textContent = "No se pudo cargar el contenido.";
  showMessage("#reserve-message", error.message, true);
});

