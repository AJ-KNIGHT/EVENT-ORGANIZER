document.addEventListener("DOMContentLoaded", () => {
  // Highlight active link in navbar
  const navLinks = document.querySelectorAll(".nav-link");
  const currentPath = window.location.pathname;

  navLinks.forEach((link) => {
    if (link.getAttribute("href") === currentPath) {
      link.classList.add("active");
    }
  });

  // Smooth scroll for internal links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault();
      document.querySelector(this.getAttribute("href")).scrollIntoView({
        behavior: "smooth",
      });
    });
  });

  // Navbar scroll behavior
  const navbar = document.querySelector(".custom-navbar");
  window.addEventListener("scroll", () => {
    if (window.scrollY > 50) {
      navbar.classList.add("scrolled");
      navbar.style.backgroundColor = "rgba(255, 255, 255, 0.95)";
    } else {
      navbar.classList.remove("scrolled");
      navbar.style.backgroundColor = "rgba(255, 255, 255, 0.9)";
    }
  });
});

// Loader Script
window.onload = function () {
    const loader = document.getElementById("loader");
  
    // Add a delay before hiding the loader to allow for smoother transition
    setTimeout(() => {
      if (loader) {
        loader.classList.add("hidden");  // Hide the loader after 3 seconds
      }
    }, 600); // Adjust the duration (in ms) as needed
  
    // Get all toast elements
    const toasts = document.querySelectorAll(".toast");
  
    toasts.forEach((toast) => {
      // Set timeout to remove toast after 60 seconds (60000 milliseconds)
      setTimeout(() => {
        toast.style.animation = "fadeOut 0.5s ease";
        setTimeout(() => toast.remove(), 500); // Remove after fadeOut animation
      }, 60000);
    });
  };
