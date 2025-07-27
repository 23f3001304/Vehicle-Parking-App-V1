function pincodeUtility() {
const pincodeInput = document.getElementById("pincode");
  const pincodeCount = document.getElementById("pincodeCount");
  if (pincodeInput && pincodeCount) {
    pincodeCount.textContent = pincodeInput.value.length;
    pincodeInput.removeEventListener("input", updatePincodeOnInput);

    function updatePincodeOnInput() {
      this.value = this.value.replace(/[^0-9]/g, "");
      pincodeCount.textContent = this.value.length;
      if (this.value.length > 0 && this.value.length !== 6) {
        this.classList.add("invalid-input");
      } else {
        this.classList.remove("invalid-input");
      }
    }
    pincodeInput.addEventListener("input", updatePincodeOnInput);

  }
}