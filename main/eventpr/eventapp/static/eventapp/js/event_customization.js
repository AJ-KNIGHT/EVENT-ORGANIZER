document.addEventListener('DOMContentLoaded', function() {
    // Read selected options JSON and tier from the body data attributes
    const bodyEl = document.querySelector('body');
    const selectedOptionsJSON = bodyEl.dataset.selectedOptions || "{}";
    let tier = bodyEl.dataset.tier || "minimal"; // default if not provided
    tier = tier.toLowerCase();  // normalize

    let selectedOptions = {};
    try {
        selectedOptions = JSON.parse(selectedOptionsJSON);
    } catch (err) {
        console.error("Failed to parse selected options:", err);
    }
    console.log("Loaded Selected Options:", selectedOptions);
    console.log("Detected Tier:", tier);

    // Assume maximum guests based on tier (can be refined later)
    const maxGuestsMap = { minimal: 50, medium: 100, premium: 200 };
    const maxGuests = maxGuestsMap[tier] || 50;

    // Grab elements for guest count and total price
    const guestCountInput = document.getElementById('guest_count');
    const totalPriceEl = document.getElementById('total_price');
    const guestErrorEl = document.getElementById('guest_error');

    // Set up click handlers for each option card
    const optionCards = document.querySelectorAll('.option-card');
    optionCards.forEach(card => {
        const cardTier = (card.dataset.tier || "").toLowerCase();
        const optionName = card.dataset.option;
        // Enforce tier restriction: disable card if tier doesn't match
        if (cardTier && cardTier !== tier) {
            card.classList.add("disabled");
            card.style.cursor = "not-allowed";
        } else {
            card.addEventListener('click', () => openPopup(optionName));
        }
    });

    // Guest count change: update price
    guestCountInput.addEventListener('change', updatePrice);

    // Popup functions
    function openPopup(optionName) {
        // Get option details; you can extend this with more options as needed
        const details = getOptionDetails(optionName);
        document.getElementById('popupTitle').textContent = details.displayName || optionName;
        document.getElementById('popupImage').src = details.image || '';
        document.getElementById('popupDescription').textContent = details.description || '';

        // Render extra fields dynamically if any (for now, basic example)
        renderOptionFields(optionName);

        // Set toggle button text based on selection state
        const toggleBtn = document.getElementById('selectDeselectBtn');
        toggleBtn.dataset.option = optionName;
        if (selectedOptions[optionName]) {
            toggleBtn.textContent = "Deselect";
            toggleBtn.classList.add('deselect');
        } else {
            toggleBtn.textContent = "Select";
            toggleBtn.classList.remove('deselect');
        }

        // Show popup and overlay
        document.getElementById('overlay').classList.add('active');
        document.getElementById('optionPopup').classList.add('active');
    }

    window.closePopup = function() {
        document.getElementById('overlay').classList.remove('active');
        document.getElementById('optionPopup').classList.remove('active');
    };

    window.toggleSelection = function() {
        const toggleBtn = document.getElementById('selectDeselectBtn');
        const optionName = toggleBtn.dataset.option;
        if (!optionName) return;

        // Toggle selection status
        if (selectedOptions[optionName]) {
            delete selectedOptions[optionName];
        } else {
            selectedOptions[optionName] = true;
        }
        // Update button text accordingly
        toggleBtn.textContent = selectedOptions[optionName] ? "Deselect" : "Select";
        toggleBtn.classList.toggle('deselect', !!selectedOptions[optionName]);

        // Update price after toggling
        updatePrice();
    };

    // Provide details for each option (extend as needed)
    function getOptionDetails(optionName) {
        const detailsMap = {
            catering: {
                displayName: "Catering",
                image: "{% static 'eventapp/images/catering.png' %}",
                description: "Select your catering preferences."
            },
            entertainment: {
                displayName: "Entertainment",
                image: "{% static 'eventapp/images/entertainment.png' %}",
                description: "Select your entertainment options."
            },
            // Add more options if necessary.
        };
        return detailsMap[optionName] || { displayName: optionName, image: "", description: "" };
    }

    // Render extra fields for specific options; currently supports catering and entertainment
    function renderOptionFields(optionName) {
        const container = document.getElementById('optionSpecificFields');
        let html = "";
        if (optionName === "catering") {
            html = `
                <label class="form-label">Catering Options:</label>
                <div class="form-check">
                    <input class="form-check-input" type="checkbox" id="catering_veg">
                    <label class="form-check-label" for="catering_veg">Vegetarian</label>
                </div>
                <div class="form-check">
                    <input class="form-check-input" type="checkbox" id="catering_nonveg">
                    <label class="form-check-label" for="catering_nonveg">Non-Vegetarian</label>
                </div>
                <div class="form-check">
                    <input class="form-check-input" type="checkbox" id="catering_beverages">
                    <label class="form-check-label" for="catering_beverages">Beverages</label>
                </div>
            `;
        } else if (optionName === "entertainment") {
            html = `
                <label class="form-label">Entertainment Options:</label>
                <div class="form-check">
                    <input class="form-check-input" type="checkbox" id="entertainment_dj">
                    <label class="form-check-label" for="entertainment_dj">DJ</label>
                </div>
                <div class="form-check">
                    <input class="form-check-input" type="checkbox" id="entertainment_band">
                    <label class="form-check-label" for="entertainment_band">Live Band</label>
                </div>
                <div class="form-check">
                    <input class="form-check-input" type="checkbox" id="entertainment_projector">
                    <label class="form-check-label" for="entertainment_projector">Projector</label>
                </div>
            `;
        }
        // Clear previous fields and add new ones
        container.innerHTML = html;
    }

    // Function to update price via AJAX call to update_price endpoint
    window.updatePrice = function() {
        const guestCount = parseInt(guestCountInput.value) || 0;
        if (guestCount > maxGuests) {
            guestErrorEl.classList.remove('d-none');
            totalPriceEl.textContent = "$0";
            return;
        } else {
            guestErrorEl.classList.add('d-none');
        }
        // Prepare selected options list (keys of selectedOptions)
        const selectedOptionsList = Object.keys(selectedOptions);

        // Get CSRF token from hidden input in the form (assumed to be present)
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        // AJAX call using jQuery
        $.ajax({
            url: "{% url 'eventapp:update_price' %}",
            type: "POST",
            data: {
                'tier': tier,
                'guest_count': guestCount,
                'selected_options': selectedOptionsList,
                'csrfmiddlewaretoken': csrfToken
            },
            success: function(response) {
                if (response.total_price) {
                    totalPriceEl.textContent = `$${response.total_price}`;
                } else if (response.error) {
                    alert(response.error);
                }
            },
            error: function(err) {
                console.error("Error updating price:", err);
            }
        });
    };

    // Optionally, update price on load
    updatePrice();
});
