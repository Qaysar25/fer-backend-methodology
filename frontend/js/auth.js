(function () {
  const TOKEN_KEY = "ferSystemsToken";
  const loginForm = document.querySelector("#loginForm");
  const protectedPage = document.body.classList.contains("app-page");

  function hasToken() {
    return Boolean(localStorage.getItem(TOKEN_KEY));
  }

  function validateIdentity(value) {
    const trimmed = value.trim();
    const emailLike = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(trimmed);
    const usernameLike = /^[a-zA-Z0-9._-]{3,}$/.test(trimmed);
    return emailLike || usernameLike;
  }

  function setError(id, message) {
    const element = document.querySelector(id);
    if (element) element.textContent = message;
  }

  if (protectedPage && !hasToken()) {
    window.location.replace("login.html");
    return;
  }

  document.querySelectorAll("[data-logout]").forEach((button) => {
    button.addEventListener("click", () => {
      localStorage.removeItem(TOKEN_KEY);
      window.location.href = "login.html";
    });
  });

  if (!loginForm) return;

  if (hasToken()) {
    window.location.replace("index.html");
    return;
  }

  loginForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const email = document.querySelector("#email").value;
    const password = document.querySelector("#password").value;
    const loginButton = document.querySelector("#loginButton");
    const spinner = loginButton.querySelector(".spinner-border");
    const buttonText = loginButton.querySelector(".btn-text");

    setError("#emailError", "");
    setError("#passwordError", "");

    let isValid = true;
    if (!validateIdentity(email)) {
      setError("#emailError", "Use a valid email address or username.");
      isValid = false;
    }
    if (!password.trim()) {
      setError("#passwordError", "Password is required.");
      isValid = false;
    }
    if (!isValid) return;

    loginButton.disabled = true;
    spinner.classList.remove("d-none");
    buttonText.classList.add("opacity-50");

    window.setTimeout(() => {
      const mockAllowed = email.toLowerCase().includes("user") && password.length > 3;
      if (!mockAllowed) {
        setError("#passwordError", "Mock login failed. Use an identity containing 'user' and a password longer than 3 characters.");
        loginButton.disabled = false;
        spinner.classList.add("d-none");
        buttonText.classList.remove("opacity-50");
        return;
      }

      const id = crypto.randomUUID ? crypto.randomUUID() : `${Date.now()}-${Math.random().toString(16).slice(2)}`;
      localStorage.setItem(TOKEN_KEY, `mock-jwt-${id}`);
      window.location.href = "index.html";
    }, 850);
  });
})();
