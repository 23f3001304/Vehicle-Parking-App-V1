function setupFormValidation(config) {
  const form = document.getElementById(config.formId);

  if (!form) {
  console.error(`Form with ID ${config.formId} not found`);
  return;
  }

  const fieldConfigs = config.fields;

  form.addEventListener("submit", function (e) {
    for (const fieldName in fieldConfigs) {

      const fieldConfig = fieldConfigs[fieldName];
      const input = document.getElementById(fieldName);
      
      if (!input) continue;
      console.log(fieldName, fieldConfig);
      const value = input.value.trim();
      if(fieldConfig.spaces === false && /\s/.test(value)) {
        e.preventDefault();
        showError(`${fieldConfig.label || fieldName} should not contain spaces`);
        input.focus();
        return;
      }
      if (fieldConfig.required && !value) {
        e.preventDefault();
        showError(`${fieldConfig.label || fieldName} is required`);
        input.focus();
        return;
      }
      if (fieldConfig.length && value.length !== fieldConfig.length) {
        e.preventDefault();
        showError(`${fieldConfig.label || fieldName} must be exactly ${fieldConfig.length} characters`);
        input.focus();
        return;
      }
      if (fieldConfig.pattern && !fieldConfig.pattern.test(value)) {
        e.preventDefault();
        showError(`Please enter a valid ${fieldConfig.label || fieldName}`);
        input.focus();
        return;
      }
      if (fieldConfig.type === "number" && isNaN(value)) {
        e.preventDefault();
        showError(`${fieldConfig.label || fieldName} must be a number`);
        input.focus();
        return;
      }

      if (fieldConfig.min && parseFloat(value) < fieldConfig.min) {
        e.preventDefault();
        showError(`${fieldConfig.label || fieldName} must be at least ${fieldConfig.min}`);
        input.focus();
        return;
      }
      if (fieldConfig.max && parseFloat(value) > fieldConfig.max) {
        e.preventDefault();
        showError(`${fieldConfig.label || fieldName} must be at most ${fieldConfig.max}`);
        input.focus();
        return;
      }
      if (fieldConfig.maxLength && value.length > fieldConfig.maxLength) {
        e.preventDefault();
        showError(`${fieldConfig.label || fieldName} must be at most ${fieldConfig.maxLength} characters`);
        input.focus();
        return;
      }
      if (fieldConfig.minLength && value.length < fieldConfig.minLength) {
        e.preventDefault();
        showError(`${fieldConfig.label || fieldName} must be at least ${fieldConfig.minLength} characters`);
        input.focus();
        return;
      }
    }
    if (window.formSubmitted) {
      e.preventDefault();
      return;
    }
    window.formSubmitted = true;
    const submitButton = form.querySelector('button[type="submit"]');
    if (submitButton) {
      submitButton.disabled = true;
      submitButton.textContent = "Processing...";
    }
  });
}