import streamlit as st
import matplotlib.pyplot as plt
from visitor_counter import display_visitor_counter

# Set page configuration
st.set_page_config(
    page_title="Redevelopment Financial Calculator",
    page_icon="🏢",
    layout="wide"
)

# Calling visitor counter at beginning of code 
display_visitor_counter()

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
            
            # Add a download button for the report
            report_text = f"""
REDEVELOPMENT PROJECT ANALYSIS
==================================================

PROJECT BASICS:
--------------
Region: {results['region']}
Project Type: {results['project_type']}
Redevelopment Type: {'Self-Redevelopment' if results['is_self_redevelopment'] else 'Builder Redevelopment'}

LAND & AREA DETAILS:
------------------
Land Area: {format_area(results['land_area'], 'Guntha' if REGION_CONFIG[region]['uses_guntha'] else 'sqm')} 
          ({format_area(results['land_area_sqm'], 'sqm')})
{"Road Width: " + str(results['road_width']) + " meters" if results['road_width'] is not None else ""}
Base FSI: {results['base_fsi']}
TDR Percentage: {results['tdr_percentage']:.1f}%
TDR Bonus to FSI: {results['effective_fsi'] - results['base_fsi']:.2f}
Effective FSI with TDR: {results['effective_fsi']:.2f}

{"Fungible FSI: " + str(results['fungible_fsi'] * 100) + "%" if REGION_CONFIG[region]['has_fungible'] else "Ancillary FSI: " + str(results['ancillary_fsi'] * 100) + "%"}
{"Fungible FSI Area Factor: " + str(results['fungible_area_factor']) if REGION_CONFIG[region]['has_fungible'] else "Ancillary FSI Area Factor: " + str(results['ancillary_area_factor'])}
Total Effective FSI: {results['total_effective_fsi']:.2f}

Current Carpet Area: {format_area(results['total_current_carpet_area'])}
Offered Carpet Area: {format_area(results['total_offered_carpet_area'])}
Total Buildable Area: {format_area(results['total_buildable_area_sqft'])}
Green Building Bonus: {format_area(results['green_bonus'])}
Self-Redevelopment Bonus: {format_area(results['self_redev_bonus'])}
Total Area with Bonuses: {format_area(results['total_final_area'])}


PREMIUM & TDR CALCULATION:
-----------------
Ready Reckoner Rate: {format_currency(results['ready_reckoner_rate'])}/sqm
{"Fungible FSI Factor: " + str(results['fungible_fsi']) if REGION_CONFIG[region]['has_fungible'] else "Ancillary FSI Factor: " + str(results['ancillary_fsi'])}
Premium Cost: {format_currency(results['premium_cost'])}
TDR Cost: {format_currency(results['tdr_cost'])}

COST ANALYSIS:
------------
Premium Cost: {format_currency(results['premium_cost'])}
TDR Cost: {format_currency(results['tdr_cost'])}
Construction Cost: {format_currency(results['construction_cost'])} ({format_currency(results['construction_cost_per_sqft'])}/sqft)
GST Cost (5% on construction): {format_currency(results['gst_cost'])}
Stamp Duty Cost: {format_currency(results['stamp_duty_cost'])}
Rent Cost: {format_currency(results['rent_cost'])}
Relocation Cost: {format_currency(results['relocation_cost'])}
Bank Interest: {format_currency(results['bank_interest'])}
TOTAL PROJECT COST: {format_currency(results['total_cost'])}

REVENUE & {"PROFIT" if is_profitable else "LOSS"}:
--------------
Market Rate: {format_currency(results['market_rate_per_sqft'])}/sqft
Project Value: {format_currency(results['project_value'])}
TOTAL {"PROFIT" if is_profitable else "LOSS"}: {format_currency(abs(results['total_profit']))}

{"PROFIT" if is_profitable else "LOSS"} DISTRIBUTION:
-----------------
{"Society's " + ("Profit" if results['society_profit'] >= 0 else "Loss") + ": " + format_currency(abs(results['society_profit']))}
{"Developer's " + ("Profit" if results['developer_profit'] >= 0 else "Loss") + " (100%): " + format_currency(abs(results['developer_profit'])) if not results['is_self_redevelopment'] else ""}
{"Profit" if results['per_member_profit'] >= 0 else "Loss"} per Member: {format_currency(abs(results['per_member_profit']))}

SALABLE FLATS:
-----------
Number of Potential Salable Flats: {results['num_salable_flats']:.1f}
            """
            
            st.download_button(
                label="Download Report as Text",
                data=report_text,
                file_name="redevelopment_report.txt",
                mime="text/plain",


# Scenario comparison tab
with scenario_tab:
    st.header("Scenario Comparison")
    st.markdown("""
    Coming soon! This feature will allow you to compare multiple redevelopment scenarios side by side.
    """)
            with viz_tab3:
                # FSI composition visualization
                fig3, ax3 = plt.subplots(figsize=(10, 6))
                
                # Create FSI breakdown
                fsi_labels = ['Base FSI']
                fsi_values = [results['base_fsi']]
                fsi_colors = ['#3498db']  # Blue
                
                # Add TDR if present
                tdr_value = results['effective_fsi'] - results['base_fsi']
                if tdr_value > 0:
                    fsi_labels.append('TDR Bonus')
                    fsi_values.append(tdr_value)
                    fsi_colors.append('#2ecc71')  # Green
                
                # Add Fungible/Ancillary if present
                if REGION_CONFIG[region]["has_fungible"] and results['fungible_area_factor'] > 0:
                    fsi_labels.append('Fungible FSI')
                    fsi_values.append(results['fungible_area_factor'])
                    fsi_colors.append('#e74c3c')  # Red
                elif not REGION_CONFIG[region]["has_fungible"] and results['ancillary_area_factor'] > 0:
                    fsi_labels.append('Ancillary FSI')
                    fsi_values.append(results['ancillary_area_factor'])
                    fsi_colors.append('#f39c12')  # Orange
                
                ax3.bar(fsi_labels, fsi_values, color=fsi_colors)
                ax3.set_ylabel('FSI Value')
                ax3.set_title('FSI Composition')
                
                # Add a line for total effective FSI
                ax3.axhline(y=results['total_effective_fsi'], color='r', linestyle='-', label=f'Total Effective FSI: {results["total_effective_fsi"]:.2f}')
                ax3.legend()
                
                plt.tight_layout()
                st.pyplot(fig3)
            with viz_tab2:
                # Profit and area allocation
                fig2, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
                
                # Area allocation
                area_labels = ['Society Area', 'Sellable Area']
                area_values = [
                    results['total_offered_carpet_area'],
                    results['builder_sellable_area']
                ]
                ax1.bar(area_labels, area_values, color=['#3498db', '#2ecc71'])
                ax1.set_ylabel('Square Feet')
                ax1.set_title('Area Allocation')
                
                # Check if project is profitable or in loss
                is_profitable = results['total_profit'] >= 0
                
                # For profit/loss distribution visualization
                if is_profitable:
                    if not results['is_self_redevelopment']:
                        profit_labels = ['Developer Profit', 'Society Profit']
                        profit_values = [
                            max(0, results['developer_profit']),
                            max(0, results['society_profit'])
                        ]
                        if all(v > 0 for v in profit_values):
                            ax2.pie(profit_values, labels=profit_labels, autopct='%1.1f%%', startangle=90, colors=['#e74c3c', '#3498db'])
                            ax2.axis('equal')
                            ax2.set_title('Profit Distribution')
                        else:
                            ax2.bar(profit_labels, profit_values, color=['#e74c3c', '#3498db'])
                            ax2.set_ylabel('Profit Amount (₹)')
                            ax2.set_title('Profit Distribution')
                    else:
                        ax2.bar(['Total Cost', 'Project Value'], 
                               [results['total_cost'], results['project_value']], 
                               color=['#e74c3c', '#3498db'])
                        ax2.set_ylabel('Amount (₹)')
                        ax2.set_title('Cost vs. Project Value')
                else:
                    if not results['is_self_redevelopment']:
                        loss_labels = ['Developer Loss', 'Society Loss']
                        loss_values = [
                            abs(results['developer_profit']),
                            abs(results['society_profit'])
                        ]
                        ax2.bar(loss_labels, loss_values, color=['#e74c3c', '#3498db'])
                        ax2.set_ylabel('Loss Amount (₹)')
                        ax2.set_title('Loss Distribution')
                    else:
                        ax2.bar(['Total Cost', 'Project Value'], 
                               [results['total_cost'], results['project_value']], 
                               color=['#e74c3c', '#3498db'])
                        ax2.set_ylabel('Amount (₹)')
                        ax2.set_title('Cost vs. Project Value (Loss Scenario)')
                
                plt.tight_layout()
                st.pyplot(fig2)"fsi_multiplier": 1.0,
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
        "max_rate": 6000,
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


# ======================
# Helper Functions
# ======================
def get_ready_reckoner_rate(region, year):
    """Get ready reckoner rate for region and year."""
    ready_reckoner_rates = {
        "Mumbai": {2022: 150000, 2023: 160000, 2024: 170000},
        "Navi Mumbai": {2022: 120000, 2023: 130000, 2024: 140000},
        "Thane": {2022: 100000, 2023: 110000, 2024: 120000},
        "Pune": {2022: 80000, 2023: 85000, 2024: 90000},
        "Nagpur": {2022: 60000, 2023: 65000, 2024: 70000},
        "Nashik": {2022: 70000, 2023: 75000, 2024: 80000}
    }
    return ready_reckoner_rates.get(region, {}).get(year, 0)


def get_fsi_based_on_road_width(region, project_type, road_width):
    """
    Returns FSI based on road width for the given region and project type.
    """
    if region == "Mumbai" and road_width is not None:
        for (min_width, max_width), fsi in ROAD_WIDTH_FSI_RULES[region][project_type].items():
            if min_width <= road_width < max_width:
                return fsi
    return REGION_CONFIG[region]["fsi_rules"][project_type]


def format_currency(amount):
    """Format amount in Indian Rupees with commas."""
    if amount >= 10000000:  # Convert to crores
        return f"₹{amount/10000000:.2f} Cr (₹{amount:,.2f})"
    elif amount >= 100000:  # Convert to lakhs
        return f"₹{amount/100000:.2f} Lakh (₹{amount:,.2f})"
    else:
        return f"₹{amount:,.2f}"


def format_area(area, unit="sqft"):
    """Format area with commas and unit."""
    return f"{area:,.2f} {unit}"


def get_land_area_input(region):
    """Conditional land area input based on region"""
    if REGION_CONFIG[region]["uses_guntha"]:
        return st.number_input("Land Area (Guntha)", min_value=0.1, value=10.0)
    else:
        return st.number_input("Land Area (Sq.m)", min_value=1.0, value=1000.0)


def get_fungible_input(region):
    """Show fungible FSI input only for Mumbai"""
    if REGION_CONFIG[region]["has_fungible"]:
        default = REGION_CONFIG[region]["premium_rates"]["fungible_fsi"] * 100
        return st.number_input("Fungible FSI (%)", 
                              min_value=0.0, max_value=40.0, 
                              value=default,
                              help="In Mumbai, this adds to the buildable area and incurs premium cost") / 100
    return 0.0


def get_ancillary_input(region):
    """Ancillary FSI input for non-Mumbai regions"""
    if not REGION_CONFIG[region]["has_fungible"]:
        return st.number_input("Ancillary FSI (%)", 
                              min_value=0.0, max_value=30.0,
                              help="Percentage of FSI to purchase as ancillary, which adds to buildable area") / 100
    return 0.0


def calculate_profit(
        region,
        ready_reckoner_year,
        land_area,
        current_carpet_area_per_member,
        total_members,
        extra_carpet_percentage,
        fsi,
        fungible_fsi,
        construction_cost_per_sqft,
        market_rate_per_sqft,
        avg_new_flat_size,
        rent_per_month,
        rent_duration_months,
        relocation_cost_per_member,
        bank_interest,
        project_type,
        is_self_redevelopment,
        profit_sharing_with_developer,
        tdr_percentage=0.0,
        tdr_type=None,
        tdr_market_rate=None,
        road_width=None,
        ancillary_fsi=0.0
    ):
    """Calculate profit/loss from redevelopment project."""
    
    # Land area conversion
    land_area_sqm = land_area * 101.17 if REGION_CONFIG[region]["uses_guntha"] else land_area
    
    # Get FSI based on road width for Mumbai
    base_fsi = get_fsi_based_on_road_width(region, project_type, road_width) if region == "Mumbai" and road_width else fsi
        
    # Get ready reckoner rate
    ready_reckoner_rate = get_ready_reckoner_rate(region, ready_reckoner_year)
    
    # Calculate areas
    total_current_carpet_area = current_carpet_area_per_member * total_members
    total_offered_carpet_area = total_current_carpet_area * (1 + extra_carpet_percentage/100)
    land_area_sqft = land_area_sqm * 10.764
    
    # TDR Calculation
    tdr_cost = 0
    tdr_bonus = 0
    if tdr_percentage > 0:
        if region == "Mumbai" and tdr_type:
            # Mumbai-specific TDR calculation with different types
            tdr_settings = TDR_CONFIG.get(region, {}).get("types", {}).get(tdr_type, {})
            if tdr_settings:
                base_tdr_area = land_area_sqm * (tdr_percentage/100)
                tdr_bonus = base_tdr_area * tdr_settings["fsi_multiplier"]
                
                if tdr_market_rate is not None:
                    tdr_rate = tdr_market_rate * tdr_settings["cost_factor"]
                    tdr_cost = base_tdr_area * 10.764 * tdr_rate
                else:
                    tdr_cost = base_tdr_area * ready_reckoner_rate * tdr_settings["cost_factor"]
        else:
            # Standard TDR calculation for other regions
            tdr_settings = TDR_CONFIG["default"]["types"]["Standard TDR"]
            base_tdr_area = land_area_sqm * (tdr_percentage/100)
            
            # Use region-specific TDR multiplier
            tdr_multiplier = REGION_CONFIG[region]["fsi_rules"]["tdr_multiplier"]
            tdr_bonus = base_tdr_area * tdr_settings["fsi_multiplier"] * tdr_multiplier
            
            # Calculate TDR cost based on ready reckoner rate and cost factor
            tdr_cost_factor = tdr_settings["cost_factor"]
            tdr_rate = ready_reckoner_rate * REGION_CONFIG[region]["tdr_rates"][project_type]
            tdr_cost = base_tdr_area * tdr_rate * tdr_cost_factor
    
    # Calculate effective FSI (base FSI + TDR)
    if tdr_percentage > 0:
        effective_fsi = base_fsi + (tdr_bonus / land_area_sqm if land_area_sqm > 0 else 0)
    else:
        effective_fsi = base_fsi
    
    # Calculate FSI components
    fungible_area_factor = base_fsi * fungible_fsi if REGION_CONFIG[region]["has_fungible"] and fungible_fsi > 0 else 0
    ancillary_area_factor = base_fsi * ancillary_fsi if not REGION_CONFIG[region]["has_fungible"] and ancillary_fsi > 0 else 0
    total_effective_fsi = effective_fsi + fungible_area_factor + ancillary_area_factor
    
    # Calculate buildable area
    total_buildable_area_sqft = land_area_sqft * total_effective_fsi
    green_bonus = total_buildable_area_sqft * REGION_CONFIG[region]["bonuses"]["green_building"]
    self_redev_bonus = total_buildable_area_sqft * REGION_CONFIG[region]["bonuses"]["self_redev"] if is_self_redevelopment else 0
    total_final_area = total_buildable_area_sqft + green_bonus + self_redev_bonus
    builder_sellable_area = total_final_area - total_offered_carpet_area
    
    # Calculate costs
    premium_cost = 0
    if REGION_CONFIG[region]["has_fungible"]:
        premium_cost = land_area_sqm * ready_reckoner_rate * fungible_fsi
    elif ancillary_fsi > 0:
        premium_cost = land_area_sqm * ready_reckoner_rate * ancillary_fsi * REGION_CONFIG[region]["fsi_rules"]["ancillary_cost"]
    
    construction_cost = total_final_area * construction_cost_per_sqft
    rent_cost = total_members * rent_per_month * rent_duration_months
    relocation_cost = total_members * relocation_cost_per_member
    
    # Taxes
    gst_cost = construction_cost * REGION_CONFIG[region]["gst"]["builder"] if not is_self_redevelopment else 0
    if is_self_redevelopment:
        stamp_duty_cost = REGION_CONFIG[region]["stamp_duty"]["self"] * total_members
    else:
        stamp_duty_cost = total_offered_carpet_area * market_rate_per_sqft * REGION_CONFIG[region]["stamp_duty"]["builder"]
    
    total_cost = premium_cost + tdr_cost + construction_cost + rent_cost + relocation_cost + bank_interest + gst_cost + stamp_duty_cost
    
    # Profit calculation
    project_value = builder_sellable_area * market_rate_per_sqft
    total_profit = project_value - total_cost
    
    if not is_self_redevelopment:
        developer_profit = total_profit
        society_profit = 0
    else:
        developer_profit = 0
        society_profit = total_profit
    
    per_member_profit = society_profit / total_members if total_members > 0 else 0
    num_salable_flats = builder_sellable_area / avg_new_flat_size if avg_new_flat_size > 0 else 0
    
    return {
        "region": region,
        "project_type": project_type,
        "is_self_redevelopment": is_self_redevelopment,
        "land_area": land_area,
        "land_area_sqm": land_area_sqm,
        "ready_reckoner_rate": ready_reckoner_rate,
        "base_fsi": base_fsi,
        "effective_fsi": effective_fsi,
        "total_effective_fsi": total_effective_fsi,
        "tdr_percentage": tdr_percentage,
        "tdr_type": tdr_type,
        "tdr_cost": tdr_cost,
        "tdr_bonus_area": tdr_bonus,
        "fungible_fsi": fungible_fsi,
        "fungible_area_factor": fungible_area_factor,
        "ancillary_fsi": ancillary_fsi,
        "ancillary_area_factor": ancillary_area_factor,
        "total_current_carpet_area": total_current_carpet_area,
        "total_offered_carpet_area": total_offered_carpet_area,
        "total_buildable_area_sqft": total_buildable_area_sqft,
        "green_bonus": green_bonus,
        "self_redev_bonus": self_redev_bonus,
        "total_final_area": total_final_area,
        "builder_sellable_area": builder_sellable_area,
        "premium_cost": premium_cost,
        "construction_cost_per_sqft": construction_cost_per_sqft,
        "construction_cost": construction_cost,
        "rent_cost": rent_cost,
        "relocation_cost": relocation_cost,
        "bank_interest": bank_interest,
        "gst_cost": gst_cost,
        "stamp_duty_cost": stamp_duty_cost,
        "total_cost": total_cost,
        "market_rate_per_sqft": market_rate_per_sqft,
        "project_value": project_value,
        "total_profit": total_profit,
        "developer_profit": developer_profit,
        "society_profit": society_profit,
        "per_member_profit": per_member_profit,
        "num_salable_flats": num_salable_flats,
        "road_width": road_width if region == "Mumbai" and road_width else None
    }


# ======================
# Main Application UI
# ======================
st.title("Redevelopment Financial Calculator")
st.markdown("""
    This calculator helps housing societies evaluate the financial aspects of redevelopment projects.
    It provides transparent calculations for profit/loss estimation, surplus corpus, and salable flats.
    Now includes Maharashtra region-specific rules, GST and stamp duty costs for more accurate financial assessment.
    Includes Fungible FSI (Mumbai) and Ancillary FSI (other regions) in buildable area calculations.
""")

# Create top-level tabs
main_tab, scenario_tab = st.tabs(["Single Project Analysis", "Scenario Comparison"])

# Main single project analysis tab
with main_tab:
    # Create two columns - one for inputs, one for results
    col1, col2 = st.columns([1, 2])

    # Input form in the first column
    with col1:
        st.header("Enter Project Details")
        
        # Location Parameters
        st.subheader("Location")
        region = st.selectbox("Region", list(REGION_CONFIG.keys()))
        ready_reckoner_year = st.selectbox("Ready Reckoner Year", [2022, 2023, 2024])
        project_type = st.selectbox("Project Type", ["residential", "commercial"])
        is_self_redevelopment = st.radio(
            "Redevelopment Type", 
            ["Self-Redevelopment", "Builder Redevelopment"]
        ) == "Self-Redevelopment"
        
        # Land Parameters
        st.subheader("Land Parameters")
        land_area = get_land_area_input(region)
        
        # Show road width input only for Mumbai
        road_width = None
        if region == "Mumbai":
            road_width = st.number_input(
                "Road Width Abutting Property (meters)", 
                min_value=6.0, 
                max_value=30.0, 
                value=12.0,
                help="FSI varies based on road width in Mumbai"
            )
        
        total_members = st.number_input("Number of Members/Flats", value=40, min_value=1, step=1)
        carpet_area = st.number_input("Current Carpet Area per Member (sqft)", value=500.0, min_value=100.0)
        extra_percentage = st.number_input("Extra Carpet Percentage", value=30.0, min_value=0.0)
        
        # Construction Parameters
        st.subheader("Construction Parameters")
        
        # Base FSI - dynamic based on road width for Mumbai
        if region == "Mumbai" and road_width is not None:
            default_fsi = get_fsi_based_on_road_width(region, project_type, road_width)
            fsi_text = f"Base FSI Value (Road width based: {default_fsi})"
        else:
            default_fsi = REGION_CONFIG[region]["fsi_rules"][project_type]
            fsi_text = "Base FSI Value"
            
        fsi = st.number_input(fsi_text, value=float(default_fsi), min_value=0.1)
        
        # TDR Input
        tdr_percentage = st.number_input(
            "TDR Percentage (0-100%)", 
            min_value=0.0, 
            max_value=100.0, 
            value=0.0,
            help="Percentage of Transfer of Development Rights to apply"
        )
        
        tdr_type = None
        tdr_market_rate = None
        if tdr_percentage > 0:
            if region == "Mumbai":
                tdr_type = st.selectbox(
                    "TDR Type",
                    options=REGION_CONFIG[region]["tdr_types_available"],
                    format_func=lambda x: f"{x} ({TDR_CONFIG['Mumbai']['types'][x]['description']})",
                    help="Select the type of TDR being utilized"
                )
                
                tdr_market_rate = st.slider(
                    "Current TDR Market Rate (₹/sqft)",
                    min_value=TDR_CONFIG["Mumbai"]["min_rate"],
                    max_value=TDR_CONFIG["Mumbai"]["max_rate"],
                    value=TDR_CONFIG["Mumbai"]["market_rate"],
                    help="Adjust based on current market conditions"
                )
            else:
                tdr_type = "Standard TDR"
                st.info(f"Using standard TDR with region-specific multiplier of {REGION_CONFIG[region]['fsi_rules']['tdr_multiplier']}x for {region}")
        
        # Conditional inputs for fungible vs ancillary FSI
        fungible_fsi = get_fungible_input(region)
        ancillary_fsi = get_ancillary_input(region)
        
        # Cost parameters
        default_construction = REGION_CONFIG[region]["premium_rates"]["construction"]
        construction_cost = st.number_input(
            "Construction Cost per sqft (₹)", 
            value=float(default_construction),
            min_value=1000.0
        )
        
        market_rate = st.number_input("Market Rate per sqft (₹)", value=17500.0, min_value=5000.0)
        avg_flat_size = st.number_input("Average Size of New Salable Flats (sqft)", value=750.0, min_value=200.0)
        
        # Financial Parameters
        st.subheader("Financial Parameters")
        rent = st.number_input("Monthly Rent per Flat (₹)", value=15000.0, min_value=0.0)
        rent_months = st.number_input("Rent Duration (months)", value=36, min_value=0, step=1)
        relocation = st.number_input("Relocation Cost per Member (₹)", value=20000.0, min_value=0.0)
        bank_interest = st.number_input("Bank Interest (₹)", value=50000000.0, min_value=0.0)
        
        # Profit Sharing (if builder redevelopment)
        profit_sharing = 100  # Default to 100% for builder as requested
        if not is_self_redevelopment:
            st.info("For builder redevelopment, the builder typically takes 100% of the profit/loss.")
            profit_sharing = 100  # Fixed at 100% for builder redevelopment
        
        # Calculate button
        calculate_button = st.button("Calculate Result", type="primary")

    # Results in the second column
    with col2:
        if calculate_button:
            results = calculate_profit(
                region=region,
                ready_reckoner_year=ready_reckoner_year,
                land_area=land_area,
                current_carpet_area_per_member=carpet_area,
                total_members=total_members,
                extra_carpet_percentage=extra_percentage,
                fsi=fsi,
                fungible_fsi=fungible_fsi,
                construction_cost_per_sqft=construction_cost,
                market_rate_per_sqft=market_rate,
                avg_new_flat_size=avg_flat_size,
                rent_per_month=rent,
                rent_duration_months=rent_months,
                relocation_cost_per_member=relocation,
                bank_interest=bank_interest,
                project_type=project_type,
                is_self_redevelopment=is_self_redevelopment,
                profit_sharing_with_developer=profit_sharing,
                tdr_percentage=tdr_percentage,
                tdr_type=tdr_type,
                tdr_market_rate=tdr_market_rate,
                road_width=road_width,
                ancillary_fsi=ancillary_fsi
            )
            
            # Display results in sections
            st.header("REDEVELOPMENT PROJECT ANALYSIS")
            
            # Project basics
            st.subheader("PROJECT BASICS")
            st.markdown(f"""
            - **Region**: {results['region']}
            - **Project Type**: {results['project_type']}
            - **Redevelopment Type**: {'Self-Redevelopment' if results['is_self_redevelopment'] else 'Builder Redevelopment'}
            if REGION_CONFIG[region]["has_fungible"]:
                st.markdown(f"""
                - **Fungible FSI**: {results['fungible_fsi'] * 100:.1f}%
                - **Fungible FSI Area Factor**: {results['fungible_area_factor']:.2f}
                if REGION_CONFIG[region]["has_fungible"]:
                premium_text = f"""
                - **Fungible FSI Factor**: {results['fungible_fsi']:.2f} ({results['fungible_fsi'] * 100:.1f}%)
                - **Premium Cost Formula**: Land Area × Ready Reckoner Rate × Fungible FSI Factor
                - **Premium Cost Calculation**: {format_area(results['land_area_sqm'], 'sqm')} × {format_currency(results['ready_reckoner_rate'])}/sqm × {results['fungible_fsi']:.2f}
                - **Total Premium Cost**: {format_currency(results['premium_cost'])}"""
            else:
                premium_text = f"""
                - **Ancillary FSI Factor**: {results['ancillary_fsi']:.2f} ({results['ancillary_fsi'] * 100:.1f}%)
                - **Ancillary Cost Formula**: Land Area × Ready Reckoner Rate × Ancillary FSI × Cost Factor
                - **Ancillary Cost Factor**: {REGION_CONFIG[region]["fsi_rules"]["ancillary_cost"]:.2f} (of Ready Reckoner)
                - **Total Ancillary Cost**: {format_currency(results['premium_cost'])}"""
                
            # Show TDR information
            if results.get('tdr_percentage', 0) > 0:
                if region == "Mumbai":
                    tdr_info = TDR_CONFIG.get(results['region'], {}).get('types', {}).get(results.get('tdr_type', ''), {})
                    if tdr_info:
                        st.markdown(f"""
                        ### TDR Analysis
                        - **Type**: {results.get('tdr_type', 'N/A')}
                        - **Source**: {tdr_info.get('source', 'N/A')}
                        - **Applicable Zones**: {", ".join(tdr_info.get('usage_restrictions', ['All zones']))}
                        - **FSI Multiplier**: {tdr_info.get('fsi_multiplier', 1.0)}x
                        - **Cost Factor**: {tdr_info.get('cost_factor', 1.0)}x
                        - **Total Bonus FSI Area**: {results.get('tdr_bonus_area', 0):.2f} sqm
                        - **Total TDR Cost**: {format_currency(results.get('tdr_cost', 0))}
                
            st.markdown(premium_text)
            
            # Cost analysis
            st.subheader("COST ANALYSIS")
            st.markdown(f"""
            - **Premium Cost**: {format_currency(results['premium_cost'])}
            - **TDR Cost**: {format_currency(results['tdr_cost'])}
            - **Construction Cost**: {format_currency(results['construction_cost'])} ({format_currency(results['construction_cost_per_sqft'])}/sqft)
            - **GST Cost (5% on construction)**: {format_currency(results['gst_cost'])}
            - **Stamp Duty Cost**: {format_currency(results['stamp_duty_cost'])}
            - **Rent Cost**: {format_currency(results['rent_cost'])}
            - **Relocation Cost**: {format_currency(results['relocation_cost'])}
            - **Bank Interest**: {format_currency(results['bank_interest'])}
            - **TOTAL PROJECT COST**: {format_currency(results['total_cost'])}
            
            # Profit/Loss distribution
            st.subheader(f"{profit_loss_word} DISTRIBUTION")
            
            if is_self_redevelopment:
                society_status = "Profit" if results['society_profit'] >= 0 else "Loss"
                member_status = "Profit" if results['per_member_profit'] >= 0 else "Loss"
                
                st.markdown(f"""
                - **Society's {society_status}**: {format_currency(abs(results['society_profit']))}
                - **{member_status} per Member**: {format_currency(abs(results['per_member_profit']))}
                
            # Visualization section
            st.subheader("Project Financial Visualization")
            
            # Create tabs for different visualizations
            viz_tab1, viz_tab2, viz_tab3 = st.tabs(["Cost Breakdown", "Profit Analysis", "FSI Composition"])
            
            with viz_tab1:
                # Cost breakdown pie chart
                cost_labels = ['Premium Cost', 'TDR Cost', 'Construction Cost', 'GST', 
                              'Stamp Duty', 'Rent Cost', 'Relocation Cost', 'Bank Interest']
                cost_values = [
                    results['premium_cost'],
                    results['tdr_cost'],
                    results['construction_cost'],
                    results['gst_cost'],
                    results['stamp_duty_cost'],
                    results['rent_cost'],
                    results['relocation_cost'],
                    results['bank_interest']
                ]
                
                # Filter out zero values for better visualization
                filtered_labels = [label for label, value in zip(cost_labels, cost_values) if value > 0]
                filtered_values = [value for value in cost_values if value > 0]
                
                fig1, ax1 = plt.subplots(figsize=(10, 6))
                ax1.pie(filtered_values, labels=filtered_labels, autopct='%1.1f%%', startangle=90)
                ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
                plt.title('Project Cost Breakdown')
                st.pyplot(fig1)
            else:
                developer_status = "Profit" if results['developer_profit'] >= 0 else "Loss"
                society_status = "Profit" if results['society_profit'] >= 0 else "Loss"
                member_status = "Profit" if results['per_member_profit'] >= 0 else "Loss"
                
                st.markdown(f"""
                - **Developer's {developer_status} (100%)**: {format_currency(abs(results['developer_profit']))}
                - **Society's {society_status} (0%)**: {format_currency(abs(results['society_profit']))}
                - **{member_status} per Member**: {format_currency(abs(results['per_member_profit']))}
                """)
                
            # Salable flats
            st.subheader("SALABLE FLATS")
            st.markdown(f"""
            - **Number of Potential Salable Flats**: {results['num_salable_flats']:.1f}
            """)
            
            # Revenue and profit/loss
            is_profitable = results['total_profit'] >= 0
            profit_loss_word = "PROFIT" if is_profitable else "LOSS"
            
            st.subheader(f"REVENUE & {profit_loss_word}")
            st.markdown(f"""
            - **Market Rate**: {format_currency(results['market_rate_per_sqft'])}/sqft
            - **Project Value**: {format_currency(results['project_value'])}
            - **TOTAL {profit_loss_word}**: {format_currency(abs(results['total_profit']))}
            """)
                    else:
                        st.warning("No TDR configuration found for the selected type")
                else:
                    # For non-Mumbai regions, show standard TDR analysis
                    tdr_multiplier = REGION_CONFIG[region]["fsi_rules"]["tdr_multiplier"]
                    tdr_cost_factor = TDR_CONFIG["default"]["types"]["Standard TDR"]["cost_factor"]
                    tdr_rate = results["ready_reckoner_rate"] * REGION_CONFIG[region]["tdr_rates"][project_type]
                    
                    st.markdown(f"""
                    ### TDR Analysis
                    - **Type**: Standard TDR
                    - **Region Multiplier**: {tdr_multiplier}x
                    - **Cost Factor**: {tdr_cost_factor}x
                    - **TDR Rate**: {format_currency(tdr_rate)}/sqm
                    - **Total Bonus FSI Area**: {results.get('tdr_bonus_area', 0):.2f} sqm
                    - **Total TDR Cost**: {format_currency(results.get('tdr_cost', 0))}
                    """)
            else:
                st.markdown(f"""
                - **Ancillary FSI**: {results['ancillary_fsi'] * 100:.1f}%
                - **Ancillary FSI Area Factor**: {results['ancillary_area_factor']:.2f}
                """)
            
            st.markdown(f"""
            - **Total Effective FSI (Base + TDR + Fungible/Ancillary)**: {results['total_effective_fsi']:.2f}
            - **Current Carpet Area**: {format_area(results['total_current_carpet_area'])}
            - **Offered Carpet Area**: {format_area(results['total_offered_carpet_area'])}
            - **Total Buildable Area**: {format_area(results['total_buildable_area_sqft'])}
            - **Green Building Bonus**: {format_area(results['green_bonus'])}
            - **Self-Redevelopment Bonus**: {format_area(results['self_redev_bonus'])}
            - **Total Area with Bonuses**: {format_area(results['total_final_area'])}
            - **Builder Sellable Area**: {format_area(results['builder_sellable_area'])}
            """)
            
            # Premium calculation
            st.subheader("PREMIUM & TDR CALCULATION")
            
            st.markdown(f"""
            - **Ready Reckoner Rate**: {format_currency(results['ready_reckoner_rate'])}/sqm
            - **Land Area**: {format_area(results['land_area_sqm'], 'sqm')}
            """)
            
            # Land and area details
            st.subheader("LAND & AREA DETAILS")
            
            # Show different details based on region
            if REGION_CONFIG[region]["uses_guntha"]:
                land_area_text = f"**Land Area**: {format_area(results['land_area'], 'Guntha')} ({format_area(results['land_area_sqm'], 'sqm')})"
            else:
                land_area_text = f"**Land Area**: {format_area(results['land_area'], 'sqm')} ({format_area(results['land_area_sqm'], 'sqm')})"
            
            # Show road width for Mumbai
            road_width_text = ""
            if region == "Mumbai" and results['road_width'] is not None:
                road_width_text = f"**Road Width**: {results['road_width']} meters"
            
            st.markdown(f"""
            {land_area_text}
            {road_width_text}
            - **Base FSI**: {results['base_fsi']}
            - **TDR Percentage**: {results['tdr_percentage']:.1f}%
            - **TDR Bonus to FSI**: {results['effective_fsi'] - results['base_fsi']:.2f}
            - **Effective FSI with TDR**: {results['effective_fsi']:.2f}
            """)
