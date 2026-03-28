(function () {
  const offsetMinutes = new Date().getTimezoneOffset();
  document.cookie = `timezone_offset=${offsetMinutes}; path=/; samesite=lax`;
  
  const footerYear = document.getElementById("footer-year");
  if (!footerYear) {
    return;
  }

  const serverYear = footerYear.dataset.serverYear;
  const serverTimestamp = Number(footerYear.dataset.serverTs);

  if (!Number.isFinite(serverTimestamp)) {
    return;
  }

  const clientTimestamp = Math.floor(Date.now() / 1000);
  const maxDiffSeconds = 24 * 60 * 60;

  if (Math.abs(clientTimestamp - serverTimestamp) <= maxDiffSeconds) {
    footerYear.textContent = String(new Date().getFullYear());
    return;
  }

  footerYear.textContent = serverYear;
})();
