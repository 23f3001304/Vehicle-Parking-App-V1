      const errorToast = document.getElementById("errorToast");
      const errorMessage = document.getElementById("errorMessage");
      const closeToast = document.getElementById("closeToast");
      const progressBar = document.getElementById("progressBar");

      let toastTimer;

      window.showError = function (message , flag) {
        errorMessage.textContent = message;

        progressBar.style.transition = "none";
        progressBar.style.width = "100%";
        errorToast.classList.remove("hidden");
        errorToast.classList.add("visible");
         
        if (flag === "Success") {
           errorToast.classList.add("success-toast");
        }
        if (flag === "Error") {
           errorToast.classList.remove("success-toast");
        }
        if (flag === "Warning") {
           errorToast.classList.remove("success-toast");
           
        }
        if (toastTimer) {
          clearTimeout(toastTimer);
        }

        startProgressAnimation();
      };

      function startProgressAnimation() {
        setTimeout(() => {
          progressBar.style.transition = "width 5s linear";
          progressBar.style.width = "0";
        }, 10);

        toastTimer = setTimeout(() => {
          errorToast.classList.remove("visible");
          errorToast.classList.add("hidden");
        }, 5000);
      }

      closeToast.addEventListener("click", function () {
        errorToast.classList.remove("visible");
        errorToast.classList.add("hidden");
        if (toastTimer) {
          clearTimeout(toastTimer);
        }
      });

      if (errorToast.classList.contains("visible")) {
        startProgressAnimation();
      }