(function () {
  const emotions = [
    { label: "Happy", icon: "😊", color: "#22c55e" },
    { label: "Sad", icon: "😔", color: "#38bdf8" },
    { label: "Angry", icon: "😠", color: "#fb7185" },
    { label: "Surprise", icon: "😲", color: "#f59e0b" },
  ];

  const defaultHistory = [
    { image: "lobby-customer-01.jpg", emotion: "Happy 😊", confidence: 94, date: "2026-05-29 09:24" },
    { image: "support-desk-clip.png", emotion: "Surprise 😲", confidence: 88, date: "2026-05-28 16:12" },
    { image: "checkout-feedback.webp", emotion: "Sad 😔", confidence: 79, date: "2026-05-28 11:47" },
    { image: "vip-counter.jpg", emotion: "Happy 😊", confidence: 91, date: "2026-05-27 14:35" },
  ];

  const input = document.querySelector("#imageInput");
  const dropZone = document.querySelector("#dropZone");
  const previewWrap = document.querySelector("#previewWrap");
  const previewImage = document.querySelector("#previewImage");
  const fileName = document.querySelector("#fileName");
  const detectButton = document.querySelector("#detectButton");
  const resultEmpty = document.querySelector("#resultEmpty");
  const resultContent = document.querySelector("#resultContent");
  const emotionResult = document.querySelector("#emotionResult");
  const confidenceRing = document.querySelector("#confidenceRing");
  const confidenceValue = document.querySelector("#confidenceValue");
  const confidenceBar = document.querySelector("#confidenceBar");
  const resultCopy = document.querySelector("#resultCopy");
  let selectedFile = null;

  function getHistory() {
    const saved = localStorage.getItem("ferHistory");
    if (saved) return JSON.parse(saved);
    localStorage.setItem("ferHistory", JSON.stringify(defaultHistory));
    return defaultHistory;
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

  function saveHistory(item) {
    const history = getHistory();
    localStorage.setItem("ferHistory", JSON.stringify([item, ...history].slice(0, 20)));
  }

  function setFile(file) {
    if (!file || !file.type.startsWith("image/")) return;
    selectedFile = file;
    previewImage.src = URL.createObjectURL(file);
    fileName.textContent = file.name;
    previewWrap.classList.remove("d-none");
    detectButton.disabled = false;
  }

  input?.addEventListener("change", (event) => setFile(event.target.files[0]));

  ["dragenter", "dragover"].forEach((name) => {
    dropZone?.addEventListener(name, (event) => {
      event.preventDefault();
      dropZone.classList.add("is-dragging");
    });
  });

  ["dragleave", "drop"].forEach((name) => {
    dropZone?.addEventListener(name, (event) => {
      event.preventDefault();
      dropZone.classList.remove("is-dragging");
    });
  });

  dropZone?.addEventListener("drop", (event) => setFile(event.dataTransfer.files[0]));

  detectButton?.addEventListener("click", () => {
    if (!selectedFile) return;
    const spinner = detectButton.querySelector(".spinner-border");
    const label = detectButton.querySelector("span:first-child");
    detectButton.disabled = true;
    spinner.classList.remove("d-none");
    label.classList.add("opacity-50");

    window.setTimeout(() => {
      const emotion = emotions[Math.floor(Math.random() * emotions.length)];
      const confidence = Math.floor(78 + Math.random() * 20);
      emotionResult.textContent = `${emotion.label} ${emotion.icon}`;
      confidenceRing.style.setProperty("--value", confidence);
      confidenceRing.style.setProperty("--ring-color", emotion.color);
      confidenceValue.textContent = `${confidence}%`;
      confidenceBar.style.width = `${confidence}%`;
      confidenceBar.style.backgroundColor = emotion.color;
      resultCopy.textContent = `${emotion.label} was detected with ${confidence}% confidence.`;
      resultEmpty.classList.add("d-none");
      resultContent.classList.remove("d-none");
      detectButton.disabled = false;
      spinner.classList.add("d-none");
      label.classList.remove("opacity-50");

      const now = new Date();
      saveHistory({
        image: selectedFile.name,
        emotion: `${emotion.label} ${emotion.icon}`,
        confidence,
        date: now.toLocaleString([], { year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit" }),
      });
      renderActivity();
      updateMetrics();
    }, 950);
  });

  function renderActivity() {
    const activityList = document.querySelector("#activityList");
    if (!activityList) return;
    activityList.innerHTML = getHistory().slice(0, 5).map((item) => `
      <li>
        <span class="activity-icon"><i class="fa-solid fa-face-smile"></i></span>
        <div>
          <strong>${item.emotion}</strong>
          <p>${escapeHtml(item.image)} • ${item.confidence}% • ${escapeHtml(item.date)}</p>
        </div>
      </li>
    `).join("");
  }

  function updateMetrics() {
    const history = getHistory();
    const average = Math.round(history.reduce((sum, item) => sum + item.confidence, 0) / history.length);
    document.querySelector("#totalScans").textContent = history.length.toLocaleString();
    document.querySelector("#avgConfidence").textContent = `${average}%`;
  }

  function renderChart() {
    const canvas = document.querySelector("#emotionChart");
    if (!canvas || !window.Chart) return;
    new Chart(canvas, {
      type: "doughnut",
      data: {
        labels: ["Happy", "Sad", "Angry", "Surprise"],
        datasets: [{
          data: [48, 19, 12, 21],
          backgroundColor: ["#22c55e", "#38bdf8", "#fb7185", "#f59e0b"],
          borderWidth: 0,
        }],
      },
      options: {
        plugins: {
          legend: { position: "bottom", labels: { color: "#475569", font: { family: "Poppins" } } },
        },
        cutout: "68%",
      },
    });
  }

  renderActivity();
  updateMetrics();
  renderChart();
})();
