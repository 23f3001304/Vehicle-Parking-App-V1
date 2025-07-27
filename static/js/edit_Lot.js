document.addEventListener("DOMContentLoaded", function () {
  const config = {
    formId: "edit_lotform",
    fields: {
      'prime location': {
        label: "Prime Location/Name",
        required: true,
      },
      'address': {
        label: "Address",
        required: true,
      },
      'pincode': {
        label: "Pincode",
        required: true,
        length: 6,
        pattern: /^\d{6}$/,
      },
      'price_per_hour': {
        label: "Price Per Hour",
        required: true,
        type: "number",
        min: 1,
        max: 1000,
      },
      'maximum spots': {
        label: "Maximum Spots",
        required: true,
        type: "number",
        min: 1,
        max: 50,
      },
    },
  };
  pincodeUtility();
  setupFormValidation(config);
});
