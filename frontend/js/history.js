(function () {
  const defaultHistory = [
    { image: "lobby-customer-01.jpg", emotion: "Happy 😊", confidence: 94, date: "2026-05-29 09:24" },
    { image: "support-desk-clip.png", emotion: "Surprise 😲", confidence: 88, date: "2026-05-28 16:12" },
    { image: "checkout-feedback.webp", emotion: "Sad 😔", confidence: 79, date: "2026-05-28 11:47" },
    { image: "vip-counter.jpg", emotion: "Happy 😊", confidence: 91, date: "2026-05-27 14:35" },
    { image: "service-delay.png", emotion: "Angry 😠", confidence: 83, date: "2026-05-26 18:03" },
  ];

  const body = document.querySelector("#historyBody");
  const search = document.querySelector("#historySearch");
  const recordCount = document.querySelector("#recordCount");

  function getHistory() {
    const saved = localStorage.getItem("ferHistory");
    if (saved) return JSON.parse(saved);
    localStorage.setItem("ferHistory", JSON.stringify(defaultHistory));
    return defaultHistory;
  }

  function setHistory(items) {
    localStorage.setItem("ferHistory", JSON.stringify(items));
  }

  function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, (char) => ({
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      "\"": "&quot;",
      "'": "&#039;",
    }[char]));
  }

  function badgeClass(emotion) {
    if (emotion.includes("Happy")) return "emotion-happy";
    if (emotion.includes("Sad")) return "emotion-sad";
    if (emotion.includes("Angry")) return "emotion-angry";
    return "emotion-surprise";
  }

  function render() {
    const query = search.value.trim().toLowerCase();
    const rows = getHistory().filter((item) => {
      return `${item.image} ${item.emotion} ${item.date}`.toLowerCase().includes(query);
    });

    recordCount.textContent = `${rows.length} ${rows.length === 1 ? "record" : "records"}`;
    body.innerHTML = rows.map((item, index) => `
      <tr>
        <td><span class="file-chip"><i class="fa-regular fa-image"></i>${escapeHtml(item.image)}</span></td>
        <td><span class="emotion-badge ${badgeClass(item.emotion)}">${escapeHtml(item.emotion)}</span></td>
        <td>
          <div class="confidence-cell">
            <span>${item.confidence}%</span>
            <div class="progress"><div class="progress-bar" style="width:${item.confidence}%"></div></div>
          </div>
        </td>
        <td>${escapeHtml(item.date)}</td>
        <td class="text-end">
          <button class="btn btn-sm btn-delete" type="button" data-delete="${index}" aria-label="Delete ${escapeHtml(item.image)}">
            <i class="fa-solid fa-trash-can"></i>
          </button>
        </td>
      </tr>
    `).join("");

    if (!rows.length) {
      body.innerHTML = `<tr><td colspan="5" class="empty-table">No scan records match your search.</td></tr>`;
    }
  }

  search?.addEventListener("input", render);
  body?.addEventListener("click", (event) => {
    const button = event.target.closest("[data-delete]");
    if (!button) return;
    const visibleRows = Array.from(body.querySelectorAll("[data-delete]"));
    const visibleIndex = visibleRows.indexOf(button);
    const query = search.value.trim().toLowerCase();
    const history = getHistory();
    const filtered = history.filter((item) => `${item.image} ${item.emotion} ${item.date}`.toLowerCase().includes(query));
    const target = filtered[visibleIndex];
    setHistory(history.filter((item) => item !== target));
    render();
  });

  render();
})();
