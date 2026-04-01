(() => {
  const MESSAGE = "사람이 공간에 들어왔습니다";

  const notificationEl = document.getElementById("notification");
  const notifMessageEl = document.getElementById("notifMessage");
  const notifTimeEl = document.getElementById("notifTime");

  const currentMessageEl = document.getElementById("currentMessage");
  const currentTimestampEl = document.getElementById("currentTimestamp");

  const historyEl = document.getElementById("history");
  const triggerBtn = document.getElementById("triggerBtn");

  let hideTimer = null;

  function formatTimestamp(d) {
    // Keep it simple and human-friendly.
    return d.toLocaleString("ko-KR");
  }

  function showNotification(message, timestampText) {
    notifMessageEl.textContent = message;
    notifTimeEl.textContent = `발생 시간: ${timestampText}`;

    if (hideTimer) clearTimeout(hideTimer);
    notificationEl.classList.add("show");
    hideTimer = setTimeout(() => notificationEl.classList.remove("show"), 3000);
  }

  function addHistoryItem(message, timestampText) {
    const li = document.createElement("li");

    const timeSpan = document.createElement("span");
    timeSpan.className = "time";
    timeSpan.textContent = timestampText;

    const textSpan = document.createElement("span");
    textSpan.className = "text";
    textSpan.textContent = message;

    li.appendChild(timeSpan);
    li.appendChild(textSpan);

    // Newest first.
    historyEl.prepend(li);
  }

  function triggerAlarm() {
    const now = new Date();
    const timestampText = formatTimestamp(now);

    currentMessageEl.textContent = MESSAGE;
    currentTimestampEl.textContent = timestampText;

    showNotification(MESSAGE, timestampText);
    addHistoryItem(MESSAGE, timestampText);
  }

  triggerBtn.addEventListener("click", triggerAlarm);
})();

