
# addon_config.py

ADDON_CONFIG = {
    "catering": {
         "label": "Catering",
         "tiers_allowed": ["Minimal", "Medium", "Premium"],
         "choices": ["None","Standard", "Buffet", "Multi-Course", "Custom"],
         "sub_options": {
             "veg": {"type": "boolean", "label": "Vegetarian Option"},
             "beverages": {"type": "boolean", "label": "Include Beverages"},
             "cuisine": {
                  "type": "choice",
                  "label": "Cuisine Type",
                  "choices": {
                      "Minimal": ["None","Indian"],
                      "Medium": ["None","Indian", "Chinese", "Mexican"],
                      "Premium": ["None","Indian", "Chinese", "Mexican", "Italian"]
                  }
             },
             "chef_special": {
                  "type": "choice",
                  "label": "Chef Special Menu",
                  "choices": {
                      "Minimal": ["None"],
                      "Medium": ["None", "Seasonal"],
                      "Premium": ["None", "Seasonal", "Gourmet"]
                  }
             }
         },
         "image_url": "/static/eventapp/images/catering.png"
    },
    "decorations": {
         "label": "Decorations",
         "tiers_allowed": ["Minimal", "Medium", "Premium"],
         "choices": ["None","Basic", "Themed", "Luxury"],
         "sub_options": {},
         "image_url": "/static/eventapp/images/decorations.png"
    },
    "entertainment": {
         "label": "Entertainment",
         "tiers_allowed": ["Medium", "Premium"],
         "choices": ["None", "DJ", "Live Band", "Projector"],
         "sub_options": {},
         "image_url": "/static/eventapp/images/entertainment.png"
    },
    "photography": {
         "label": "Photography",
         "tiers_allowed": ["Medium", "Premium"],
         "choices": ["None", "Basic", "Professional"],
         "sub_options": {},
         "image_url": "/static/eventapp/images/photography.png"
    },
    "lighting_effects": {
         "label": "Lighting Effects",
         "tiers_allowed": ["Minimal", "Medium", "Premium"],
         "choices": ["None","Basic", "Themed", "Premium"],
         "sub_options": {},
         "image_url": "/static/eventapp/images/lighting_effects.png"
    },
    "table_arrangements": {
          "label": "Table Arrangements",
          "tiers_allowed": ["Minimal", "Medium", "Premium"],
          "choices": ["None","Basic", "Themed", "Premium"],
          "sub_options": {},
          "image_url": "/static/eventapp/images/table_arrangements.png"
     },
    # Boolean add-ons (with no sub-options):
    "audio_visual": {
         "type": "boolean",
         "label": "Audio Visual",
         "tiers_allowed": ["Minimal", "Medium", "Premium"],
         "image_url": "/static/eventapp/images/audio_visual.png"
    },
    "security_staff": {
         "type": "boolean",
         "label": "Security Staff",
         "tiers_allowed": ["Minimal", "Medium", "Premium"],
         "image_url": "/static/eventapp/images/security_staff.png"
    },
    "medical_support": {
         "type": "boolean",
         "label": "Medical Support",
         "tiers_allowed": ["Minimal", "Medium", "Premium"],
         "image_url": "/static/eventapp/images/medical_support.png"
    },
    "event_manager": {
         "type": "boolean",
         "label": "Event Manager",
         "tiers_allowed": ["Minimal", "Medium", "Premium"],
         "image_url": "/static/eventapp/images/event_manager.png"
    },
    
    "cleanup_service": {
         "type": "boolean",
         "label": "Cleanup Service",
         "tiers_allowed": ["Minimal", "Medium", "Premium"],
         "image_url": "/static/eventapp/images/cleanup_service.png"
    }
}
