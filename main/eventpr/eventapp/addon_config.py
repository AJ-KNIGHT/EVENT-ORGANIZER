ADDON_CONFIG = {
    "catering": {
        "label": "Catering",
        "tiers_allowed": ["Minimal", "Medium", "Premium"],
        "description": "Includes buffet setup, serving staff, and standard menu options.",
        "price": 50,  # Base price for catering
        "per_guest": True,  # This addon is priced per guest
        "image_url": "/static/eventapp/images/catering.jpeg"
    },
    "decorations": {
        "label": "Decorations",
        "tiers_allowed": ["Minimal", "Medium", "Premium"],
        "description": "Standard venue decorations including tables, chairs, and floral arrangements.",
        "price": 5000,  # Base price for decorations
        "per_guest": False,  # This addon is not priced per guest
        "image_url": "/static/eventapp/images/decorations.jpeg"
    },
    "entertainment": {
        "label": "Entertainment",
        "tiers_allowed": ["Medium", "Premium"],
        "description": "Basic live music or DJ services for your event.",
        "price": 15000,  # Base price for entertainment
        "per_guest": False,  # This addon is not priced per guest
        "image_url": "/static/eventapp/images/entertainment.jpeg"
    },
    "photography": {
        "label": "Photography",
        "tiers_allowed": ["Medium", "Premium"],
        "description": "Professional photography with digital copies of all images.",
        "price": 12000,  # Base price for photography
        "per_guest": False,  # This addon is not priced per guest
        "image_url": "/static/eventapp/images/photography.jpeg"
    },
    "lighting_effects": {
        "label": "Lighting Effects",
        "tiers_allowed": ["Minimal", "Medium", "Premium"],
        "description": "Standard ambient lighting and decorative effects.",
        "price": 8000,  # Base price for lighting effects
        "per_guest": False,  # This addon is not priced per guest
        "image_url": "/static/eventapp/images/lighting_effects.jpeg"
    },
    "table_arrangements": {
        "label": "Table Arrangements",
        "tiers_allowed": ["Minimal", "Medium", "Premium"],
        "description": "Includes table covers, centerpieces, and guest seating plans.",
        "price": 30,  # Base price for table arrangements
        "per_guest": True,  # This addon is not priced per guest
        "image_url": "/static/eventapp/images/table_arrangements.jpeg"
    },
    # Boolean add-ons (Fixed Pricing)
    "audio_visual": {
        "label": "Audio Visual",
        "tiers_allowed": ["Minimal", "Medium", "Premium"],
        "description": "Includes microphones, speakers, and projectors if needed.",
        "price": 5000,  # Base price for audio visual
        "per_guest": False,  # This addon is not priced per guest
        "image_url": "/static/eventapp/images/audio_visual.jpeg"
    },
    "security_staff": {
        "label": "Security Staff",
        "tiers_allowed": ["Minimal", "Medium", "Premium"],
        "description": "Trained security personnel to ensure event safety.",
        "price": 50,  # Base price for security staff
        "per_guest": True,  # This addon is priced per guest
        "image_url": "/static/eventapp/images/security_staff.jpeg"
    },
    "medical_support": {
        "label": "Medical Support",
        "tiers_allowed": ["Minimal", "Medium", "Premium"],
        "description": "On-site medical team with first aid and emergency response.",
        "price": 50,  # Base price for medical support
        "per_guest": True,  # This addon is priced per guest
        "image_url": "/static/eventapp/images/medical_support.jpeg"
    },
    "event_manager": {
        "label": "Event Manager",
        "tiers_allowed": ["Minimal", "Medium", "Premium"],
        "description": "A dedicated event manager to coordinate logistics and execution.",
        "price": 10000,  # Base price for event manager
        "per_guest": False,  # This addon is not priced per guest
        "image_url": "/static/eventapp/images/event_manager.jpeg"
    },
    "cleanup_service": {
        "label": "Cleanup Service",
        "tiers_allowed": ["Minimal", "Medium", "Premium"],
        "description": "Post-event cleanup including waste disposal and venue reset.",
        "price": 4000,  # Base price for cleanup service
        "per_guest": False,  # This addon is not priced per guest
        "image_url": "/static/eventapp/images/cleanup_service.jpeg"
    },
}
