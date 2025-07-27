document.addEventListener("DOMContentLoaded", function () {
  const config = {
    formId: "add_lotform",
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
// const syncButtonHeights = () => {
//   const goBackBtn = document.getElementById('go_back');
//   const addLotBtn = document.getElementById('addlot-button');

//   const addLotRect = addLotBtn.getBoundingClientRect();
//   goBackBtn.style.position = 'absolute';
//   goBackBtn.style.top = addLotRect.top + 'px';
// };

// window.addEventListener('load', syncButtonHeights);
// let resizeRunning = false;

// function onResizeEnd() {
//   resizeRunning = false;
//   syncButtonHeights();
// }

// window.addEventListener('resize', () => {
//   if (!resizeRunning) {
//     resizeRunning = true;
//     requestAnimationFrame(onResizeEnd);
//   }
// });

  pincodeUtility();
  setupFormValidation(config);
});
