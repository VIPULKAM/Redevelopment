# File: config.py
# Contains all configuration data for the application

# ======================
# Road Width Based FSI Rules for Mumbai
# ======================
ROAD_WIDTH_FSI_RULES = {
    "Mumbai": {
        "residential": {
            (0, 9): 1.0,      # Roads <9m width
            (9, 12): 1.33,    # Roads 9-12m
            (12, 18): 2.5,    # Roads 12-18m
            (18, float('inf')): 3.0  # Roads >18m
        },
        "commercial": {
            (0, 9): 1.5,
            (9, 12): 2.0,
            (12, 18): 3.0,
            (18, float('inf')): 5.0
        }
    }
}

# ======================
# Enhanced TDR Configuration Rules for Mumbai 
# ======================
TDR_CONFIG = {
    "Mumbai": {
        "types": {
            "Road TDR": {
                "fsi_multiplier": 1.0,
                "cost_factor": 0.7,
                "description": "Generated from road-widening projects",
                "source": "MCGM",
                "usage_restrictions": ["all zones"]
            },
            "Reservation TDR": {
                "fsi_multiplier": 1.0,
                "cost_factor": 0.8,
                "description": "From surrendering land for public amenities",
                "source": "DP Reservations",
                "usage_restrictions": ["all zones"]
            },
            "Slum TDR": {
                "fsi_multiplier": 1.5,
                "cost_factor": 1.2,
                "description": "From slum rehabilitation projects",
                "source": "SRA",
                "usage_restrictions": ["suburbs", "extended suburbs"]
            },
            "Heritage TDR": {
                "fsi_multiplier": 2.0,
                "cost_factor": 1.5,
                "description": "From heritage property conservation",
                "source": "Heritage Committee",
                "usage_restrictions": ["island city", "townsite"]
            }
        },
        "market_rate": 4500,
        "min_rate": 3000,
        "max_rate": 9000,
        "calculation_method": "market_driven"
    },
    "default": {
        "types": {
            "Standard TDR": {
                "fsi_multiplier": 1.0,
                "cost_factor": 1.0,
                "description": "Standard TDR for non-Mumbai regions",
                "calculation_method": "ready_reckoner"
            }
        }
    }
}

# ======================
# Enhanced Configuration with Region-Specific Settings
# ======================
REGION_CONFIG = {
    "Mumbai": {
        "uses_guntha": False,
        "has_fungible": True,
        "fsi_rules": {
            "residential": 2.5, 
            "commercial": 5.0, 
            "tdr_multiplier": 2.5,
            "ancillary_cost": 0
        },
        "tdr_types_available": ["Road TDR", "Reservation TDR", "Slum TDR", "Heritage TDR"],
        "premium_rates": {
            "construction": 3000, 
            "fungible_fsi": 0.35
        },
        "bonuses": {
            "green_building": 0.07, 
            "self_redev": 0.10, 
            "ancillary": 0.60
        },
        "parking": {
            "redev_reduction": 0.20, 
            "car_lift_threshold": 2000
        },
        "tdr_rates": {
            "residential": 0.4, 
            "commercial": 0.3
        },
        "stamp_duty": {
            "builder": 0.06,
            "self": 1000
        },
        "gst": {
            "builder": 0.05,
            "self": 0.0
        }
    },
    "Navi Mumbai": {
        "uses_guntha": True,
        "has_fungible": False,
        "fsi_rules": {
            "residential": 2.0, 
            "commercial": 4.0, 
            "tdr_multiplier": 2.0,
            "ancillary_cost": 0.4
        },
        "tdr_types_available": ["Standard TDR"],
        "premium_rates": {
            "construction": 2800, 
            "fungible_fsi": 0.33
        },
        "bonuses": {
            "green_building": 0.06, 
            "self_redev": 0.12, 
            "ancillary": 0.50
        },
        "parking": {
            "redev_reduction": 0.25, 
            "car_lift_threshold": 1800
        },
        "tdr_rates": {
            "residential": 0.38, 
            "commercial": 0.28
        },
        "stamp_duty": {
            "builder": 0.06,
            "self": 1000
        },
        "gst": {
            "builder": 0.05,
            "self": 0.0
        }
    },
    "Thane": {
        "uses_guntha": True,
        "has_fungible": False,
        "fsi_rules": {
            "residential": 3.0, 
            "commercial": 4.0, 
            "tdr_multiplier": 2.0,
            "ancillary_cost": 0.4
        },
        "tdr_types_available": ["Standard TDR"],
        "premium_rates": {
            "construction": 2500,
            "fungible_fsi": 0.30
        },
        "bonuses": {
            "green_building": 0.05,
            "self_redev": 0.15,
            "ancillary": 0.50
        },
        "parking": {
            "redev_reduction": 0.30,
            "car_lift_threshold": 1500
        },
        "tdr_rates": {
            "residential": 0.35, 
            "commercial": 0.25
        },
        "stamp_duty": {
            "builder": 0.06,
            "self": 1000
        },
        "gst": {
            "builder": 0.05,
            "self": 0.0
        }
    },
    "Pune": {
        "uses_guntha": True,
        "has_fungible": False,
        "fsi_rules": {
            "residential": 1.75, 
            "commercial": 3.0, 
            "tdr_multiplier": 1.8,
            "ancillary_cost": 0.4
        },
        "tdr_types_available": ["Standard TDR"],
        "premium_rates": {
            "construction": 2700, 
            "fungible_fsi": 0.28
        },
        "bonuses": {
            "green_building": 0.05,
            "self_redev": 0.12,
            "ancillary": 0.45
        },
        "parking": {
            "redev_reduction": 0.25,
            "car_lift_threshold": 1800
        },
        "tdr_rates": {
            "residential": 0.35, 
            "commercial": 0.25
        },
        "stamp_duty": {
            "builder": 0.06,
            "self": 1000
        },
        "gst": {
            "builder": 0.05,
            "self": 0.0
        }
    },
    "Nagpur": {
        "uses_guntha": True,
        "has_fungible": False,
        "fsi_rules": {
            "residential": 1.5, 
            "commercial": 2.5, 
            "tdr_multiplier": 1.5,
            "ancillary_cost": 0.4
        },
        "tdr_types_available": ["Standard TDR"],
        "premium_rates": {
            "construction": 2200, 
            "fungible_fsi": 0.25
        },
        "bonuses": {
            "green_building": 0.05,
            "self_redev": 0.10,
            "ancillary": 0.40
        },
        "parking": {
            "redev_reduction": 0.20,
            "car_lift_threshold": 1500
        },
        "tdr_rates": {
            "residential": 0.30, 
            "commercial": 0.20
        },
        "stamp_duty": {
            "builder": 0.06,
            "self": 1000
        },
        "gst": {
            "builder": 0.05,
            "self": 0.0
        }
    },
    "Nashik": {
        "uses_guntha": True,
        "has_fungible": False,
        "fsi_rules": {
            "residential": 1.6, 
            "commercial": 2.8, 
            "tdr_multiplier": 1.6,
            "ancillary_cost": 0.4
        },
        "tdr_types_available": ["Standard TDR"],
        "premium_rates": {
            "construction": 2300, 
            "fungible_fsi": 0.26
        },
        "bonuses": {
            "green_building": 0.05,
            "self_redev": 0.10,
            "ancillary": 0.40
        },
        "parking": {
            "redev_reduction": 0.20,
            "car_lift_threshold": 1600
        },
        "tdr_rates": {
            "residential": 0.32, 
            "commercial": 0.22
        },
        "stamp_duty": {
            "builder": 0.06,
            "self": 1000
        },
        "gst": {
            "builder": 0.05,
            "self": 0.0
        }
    }
}

# Ready Reckoner rates by region and year
READY_RECKONER_RATES = {
    "Mumbai": {2022: 150000, 2023: 160000, 2024: 170000},
    "Navi Mumbai": {2022: 120000, 2023: 130000, 2024: 140000},
    "Thane": {2022: 100000, 2023: 110000, 2024: 120000},
    "Pune": {2022: 80000, 2023: 85000, 2024: 90000},
    "Nagpur": {2022: 60000, 2023: 65000, 2024: 70000},
    "Nashik": {2022: 70000, 2023: 75000, 2024: 80000}
}