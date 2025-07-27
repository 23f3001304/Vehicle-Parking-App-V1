document.addEventListener("DOMContentLoaded", function () {
        const config = {
          formId: "loginForm",
          fields : {
            username: {
              type: "text",
              required: true,
              pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
            },
            password: {
              type: "password",
              required: true,
              length: 8,
              spaces: false
            },
          }
        }
        setupFormValidation(config);
        const usernameInput = document.getElementById("username");
        usernameInput.focus();
        passwordUtility("false");
      });