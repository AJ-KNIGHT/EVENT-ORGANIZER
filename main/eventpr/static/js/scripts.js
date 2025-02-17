document.addEventListener("DOMContentLoaded", () => {
    // Highlight active link in navbar
    const navLinks = document.querySelectorAll(".nav-link");
    const currentPath = window.location.pathname;

    navLinks.forEach(link => {
        if (link.getAttribute("href") === currentPath) {
            link.classList.add("active");
        }
    });

    // Smooth scroll for internal links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener("click", function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute("href")).scrollIntoView({
                behavior: "smooth"
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

function showAlert(message, type) {
    // Create alert div
    const alertDiv = document.createElement("div");
    alertDiv.classList.add("alert-message", type); // Add type (success/error)
    alertDiv.textContent = message;

    // Append the alert to the container
    const container = document.getElementById("alert-container");
    container.appendChild(alertDiv);

    // Show the alert
    setTimeout(() => {
        alertDiv.style.display = 'block';
    }, 100);

    // Hide the alert after 5 seconds
    setTimeout(() => {
        alertDiv.style.opacity = '0';
        setTimeout(() => {
            alertDiv.remove(); // Remove from DOM after animation
        }, 500);
    }, 5000);
}
