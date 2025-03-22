
const USER_TIER = "{{ selected_tier }}";  // Assuming USER_TIER is the selected tier

document.addEventListener("DOMContentLoaded", function () {
    // Pass the addon_config from Django to JavaScript
    const ADDON_CONFIG = JSON.parse('{{ addon_config|escapejs }}');
    console.log("Addon Config:", ADDON_CONFIG);


    console.log("DOM fully loaded ✅");

    let selectedOptions = {};

    function getElement(id) {
        const el = document.getElementById(id);
        if (!el) console.error(`❌ Missing element: #${id}`);
        return el;
    }

    // DOM Elements
    const dom = {
        guestCount: getElement("guest_count"),
        totalPrice: getElement("total_price"),
        csrfToken: document.querySelector("[name=csrfmiddlewaretoken]")?.value || "",
        summaryContainer: getElement("selectedSummary"),
        tierInput: getElement("tierInput"),
        venueSubtierInput: getElement("venueSubtierInput"),
        optionCards: document.querySelectorAll(".option-card"),
        overlay: getElement("overlay"),
        popup: getElement("optionPopup"),
        popupTitle: getElement("popupTitle"),
        popupImage: getElement("popupImage"),
        popupFields: getElement("optionSpecificFields"),
        selectDeselectBtn: getElement("selectDeselectBtn"),
        selectedOptionsInput: getElement("selectedOptionsInput"),
        closePopupBtn: document.querySelector(".close-btn"),
    };

    if (!dom.guestCount || !dom.totalPrice || !dom.popup) {
        console.error("❌ Critical DOM elements missing. Script will not run.");
        return;
    }

    console.log("✅ DOM elements initialized:", dom);

    function debounce(func, timeout = 300) {
        let timer;
        return (...args) => {
            clearTimeout(timer);
            timer = setTimeout(() => func(...args), timeout);
        };
    }

    function closePopup() {
        console.log("Closing popup...");
        dom.popup.classList.remove("show");
        dom.overlay.classList.remove("show");
    }

    function openPopup(option, imageUrl, label) {
        if (!dom.popupTitle || !dom.popupImage || !dom.popupFields) {
            console.error("❌ Popup elements missing. Cannot open popup.");
            return;
        }
        if (typeof ADDON_CONFIG === 'undefined' || !ADDON_CONFIG[option]) {
            console.error("❌ ADDON_CONFIG is undefined or option not found:", option);
            return;
        }

        console.log("Opening popup for:", option);

        dom.popupTitle.innerText = label || "Customization Options";

        if (imageUrl) {
            dom.popupImage.src = imageUrl;
            dom.popupImage.classList.remove("d-none");
        } else {
            dom.popupImage.classList.add("d-none");
        }

        dom.popupFields.innerHTML = "";

        const optionData = ADDON_CONFIG[option];

        if (optionData?.options?.length) {
            optionData.options.forEach(opt => {
                let label = document.createElement("label");
                let input = document.createElement("input");
                input.type = "checkbox";
                input.value = opt.id;
                input.checked = selectedOptions[option]?.includes(opt.id) || false;
                input.addEventListener("change", () => {
                    if (!selectedOptions[option]) selectedOptions[option] = [];
                    if (input.checked) {
                        selectedOptions[option].push(opt.id);
                    } else {
                        selectedOptions[option] = selectedOptions[option].filter(id => id !== opt.id);
                        if (selectedOptions[option].length === 0) delete selectedOptions[option];
                    }
                    updateState();
                });

                label.appendChild(input);
                label.appendChild(document.createTextNode(opt.name));
                dom.popupFields.appendChild(label);
            });
        } else {
            console.warn("⚠️ No additional options found for this add-on.");
        }

        dom.popup.classList.add("show");
        dom.overlay.classList.add("show");
    }

    function handleCardClick(e) {
        const card = e.currentTarget;
        const option = card.dataset.option;
        const imageUrl = card.dataset.imageUrl;
        const label = card.dataset.label;

        if (!option) {
            console.error("❌ Missing option in dataset:", card);
            return;
        }

        console.log("Clicked on:", option);

        // Check for tier restrictions
        if (!ADDON_CONFIG[option].tiers_allowed.includes(USER_TIER)) {
            console.warn(`⚠️ This add-on is not available for the selected tier: ${USER_TIER}`);
            return;
        }

        openPopup(option, imageUrl, label);

        dom.selectDeselectBtn.innerText = card.classList.contains("selected") ? "Deselect" : "Select";

        dom.selectDeselectBtn.onclick = function () {
            if (card.classList.contains("selected")) {
                delete selectedOptions[option];
                card.classList.remove("selected");
            } else {
                selectedOptions[option] = { selected: true, details: ADDON_CONFIG[option]?.details || {} };
                card.classList.add("selected");
            }

            console.log("Updated selected options:", selectedOptions);

            closePopup();
            updateState();
        };
    }

    function handleGuestCountChange() {
        updatePrice();
    }

    function updatePrice() {
        console.log("Updating price...");

        dom.totalPrice.innerHTML = `<div class="spinner-border spinner-border-sm text-primary"></div> Calculating...`;

        const requestData = {
            tier: dom.tierInput?.value || "Minimal",
            venue_subtier: dom.venueSubtierInput?.value || "",
            guest_count: parseInt(dom.guestCount?.value) || 0,
            selected_options: Object.keys(selectedOptions),
        };

        fetch(updatePriceUrl, {
            method: "POST",
            headers: { "X-CSRFToken": dom.csrfToken, "Content-Type": "application/json" },
            body: JSON.stringify(requestData),
        })
        .then(response => response.json())
        .then(data => {
            console.log("✅ Price update response:", data);
            dom.totalPrice.innerHTML = data.total_price ? `$${data.total_price}` : `<span class="text-danger">Error loading price</span>`;
        })
        .catch(error => {
            console.error("❌ Price update failed:", error);
            dom.totalPrice.innerHTML = `<span class="text-muted">Failed to load</span>`;
        });
    }

    function updateState() {
        console.log("Updating state...");
        dom.selectedOptionsInput.value = JSON.stringify(selectedOptions);
        updatePrice();
    }

    function initEventListeners() {
        console.log("Initializing event listeners...");

        dom.guestCount.addEventListener("input", debounce(handleGuestCountChange, 300));

        dom.optionCards.forEach(card => {
            card.addEventListener("click", handleCardClick);
        });

        dom.overlay.addEventListener("click", closePopup);
        dom.closePopupBtn?.addEventListener("click", closePopup);
    }

    initEventListeners();

    setTimeout(() => {
        console.log("Initializing state update...");
        updateState();
    }, 0);
});