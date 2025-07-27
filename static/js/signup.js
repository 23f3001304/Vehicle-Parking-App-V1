

document.addEventListener("DOMContentLoaded", function () {
  const config = {
  formId: "signupform",
  fields: {
    email: {
      label: "Email",
      required: true,
      pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
    },
    password: {
      label: "Password",
      required: true,
      length: 8,
      spaces: false
    },
    pincode: {
      label: "Pincode",
      required: true,
      length: 6,
      pattern: /^\d{6}$/,
    },
    fullname: {
      label: "Full Name",
      required: true,
      maxLength: 20,
      pattern: /^[a-zA-Z\s]+$/,
      minLength: 3,
    },
    address: {
      label: "Address",
      required: true,
    },
  },
};

  passwordUtility(true);
  pincodeUtility();
  setupFormValidation(config);
});
