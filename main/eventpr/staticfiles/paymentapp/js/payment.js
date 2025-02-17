document.addEventListener("DOMContentLoaded", function () {
  console.log("✅ payment.js is loaded!");
  alert("✅ payment.js is working!");
  const paymentMethods = document.querySelectorAll(".payment-method");
  const codMethod = document.querySelector(".cod");
  const confirmButton = document.querySelector(".confirm-btn");

  // Ensure only Cash on Delivery is selected
  paymentMethods.forEach((method) => {
    method.addEventListener("click", function () {
      if (method.classList.contains("unavailable")) {
        alert("This payment method is not available right now.");
      } else {
        // Remove 'selected' class from all and add it only to COD
        paymentMethods.forEach((m) => m.classList.remove("selected"));
        codMethod.classList.add("selected");
      }
    });
  });

  // Disable confirm button if COD is not selected (for safety)
  confirmButton.addEventListener("click", function (event) {
    if (!codMethod.classList.contains("selected")) {
      event.preventDefault();
      alert("Only Cash on Delivery is available at the moment.");
    }
  });
});
