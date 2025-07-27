function passwordUtility(flag) {
  var passwordInput = document.getElementById("password");
  const charCount = document.getElementById("charCount");
  if (flag === true) {
    const passwordStrengthIndicator = document.getElementById(
      "passwordStrengthIndicator"
    );
    const strengthText = document.getElementById("strengthText");
    function updateStrengthUI(strength) {
      if (strengthText) {
        if (strength < 30) {
          strengthText.textContent = "Weak";
          strengthText.className = "password-strength-text weak";
          passwordStrengthIndicator.style.backgroundColor = "#FF3B30";
        } else if (strength < 60) {
          strengthText.textContent = "Fair";
          strengthText.className = "password-strength-text fair";
          passwordStrengthIndicator.style.backgroundColor = "#FF9500";
        } else if (strength < 100) {
          strengthText.textContent = "Good";
          strengthText.className = "password-strength-text good";
          passwordStrengthIndicator.style.backgroundColor = "#FFCC00";
        } else {
          strengthText.textContent = "Strong";
          strengthText.className = "password-strength-text strong";
          passwordStrengthIndicator.style.backgroundColor = "#34C759";
        }
      }
    }

    function calculatePasswordStrength(password) {
      let strength = 0;

      if (password.length >= 4) strength += 25;
      if (password.length >= 6) strength += 10;
      if (password.length >= 8) strength += 15;

      if (/\d/.test(password)) strength += 10;

      if (/[a-z]/.test(password)) strength += 10;

      if (/[A-Z]/.test(password)) strength += 15;

      if (/[^a-zA-Z0-9]/.test(password)) strength += 15;

      return Math.min(strength, 100);
    }
  }
  const togglePassword = document.getElementById("togglePassword");
  if (togglePassword && passwordInput) {
    togglePassword.addEventListener("click", function () {
      const type = passwordInput.getAttribute("type") === "password" ? "text" : "password";
      passwordInput.setAttribute("type", type);
      this.setAttribute(
        "aria-label",
        type === "password" ? "Show password" : "Hide password"
      );
      const icon = this.querySelector(".toggle-icon");
      if (type === "password") {
        icon.innerHTML = `<path d="M12 5C7 5 2.73 8.11 1 12.5C2.73 16.89 7 20 12 20C17 20 21.27 16.89 23 12.5C21.27 8.11 17 5 12 5ZM12 17.5C9.24 17.5 7 15.26 7 12.5C7 9.74 9.24 7.5 12 7.5C14.76 7.5 17 9.74 17 12.5C17 15.26 14.76 17.5 12 17.5ZM12 9.5C10.34 9.5 9 10.84 9 12.5C9 14.16 10.34 15.5 12 15.5C13.66 15.5 15 14.16 15 12.5C15 10.84 13.66 9.5 12 9.5Z" fill="#1D1B20"/>`;
      } else {
        icon.innerHTML = `<path d="M12 9.5C10.34 9.5 9 10.84 9 12.5C9 14.16 10.34 15.5 12 15.5C13.66 15.5 15 14.16 15 12.5C15 10.84 13.66 9.5 12 9.5ZM12 7.5C9.24 7.5 7 9.74 7 12.5C7 15.26 9.24 17.5 12 17.5C14.76 17.5 17 15.26 17 12.5C17 9.74 14.76 7.5 12 7.5ZM12 4.5C17 4.5 21.27 7.61 23 12C21.27 16.39 17 19.5 12 19.5C7 19.5 2.73 16.39 1 12C2.73 7.61 7 4.5 12 4.5Z" fill="#1D1B20"/><path d="M3.71 3.56L20.44 20.29" stroke="#1D1B20" stroke-width="2" stroke-linecap="round"/>`;
      }
    });
  }

  if (passwordInput && charCount) {
    charCount.textContent = passwordInput.value.length;

    passwordInput.addEventListener("input", function () {
      const value = this.value;
      charCount.textContent = value.length;

      if (passwordStrengthIndicator && strengthText) {
        let strength = calculatePasswordStrength(value);
        passwordStrengthIndicator.style.cssText = `width: ${strength}% !important; display: block !important;`;
        updateStrengthUI(strength);
      }
    });
  }
}
function isNumberKey(event) {
      const key = event.key;
      return (
        (key >= "0" && key <= "9") ||
        key === "Backspace" ||
        key === "Delete" ||
        key === "ArrowLeft" ||
        key === "ArrowRight"
      );
    }