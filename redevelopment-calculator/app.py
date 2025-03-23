import streamlit as st
import matplotlib.pyplot as plt

# ======================
# Enhanced Configuration
# ======================
REGION_CONFIG = {
    "Mumbai": {
        "fsi_rules": {
            "residential": 2.5, 
            "commercial": 5.0, 
            "tdr_multiplier": 2.5
        },
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
            "builder": 0.06,  # 6% for builder redevelopment
            "self": 1000      # Flat Rs.1000 per unit for self-redevelopment
        },
        "gst": {
            "builder": 0.05,  # 5% for builder redevelopment
            "self": 0.0       # 0% for self-redevelopment
        }
    },
    "Navi Mumbai": {
        "fsi_rules": {
            "residential": 2.0, 
            "commercial": 4.0, 
            "tdr_multiplier": 2.0
        },
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
        "fsi_rules": {
            "residential": 3.0, 
            "commercial": 4.0, 
            "tdr_multiplier": 2.0
        },
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
        "fsi_rules": {
            "residential": 1.75, 
            "commercial": 3.0, 
            "tdr_multiplier": 1.8
        },
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
        "fsi_rules": {
            "residential": 1.5, 
            "commercial": 2.5, 
            "tdr_multiplier": 1.5
        },
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
        "fsi_rules": {
            "residential": 1.6, 
            "commercial": 2.8, 
            "tdr_multiplier": 1.6
        },
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

def calculate_profit(
        region,
        ready_reckoner_year,
        land_area_guntha,
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
        tdr_percentage=0.0
    ):
    """Calculate profit from redevelopment project with TDR support and tax considerations."""
    # Convert guntha to square meters (1 guntha = 101.17 sqm)
    land_area_sqm = land_area_guntha * 101.17
    
    # Get ready reckoner rate for the region and year
    ready_reckoner_rate = get_ready_reckoner_rate(region, ready_reckoner_year)
    
    # Calculate current carpet area
    total_current_carpet_area = current_carpet_area_per_member * total_members
    
    # Calculate offered carpet area (with extra percentage)
    total_offered_carpet_area = total_current_carpet_area * (1 + extra_carpet_percentage/100)
    
    # Convert to sqft (1 sqm = 10.764 sqft)
    land_area_sqft = land_area_sqm * 10.764
    
    # TDR Calculation
    tdr_factor = REGION_CONFIG[region]["tdr_rates"][project_type]
    tdr_multiplier = REGION_CONFIG[region]["fsi_rules"]["tdr_multiplier"]
    tdr_bonus = (tdr_percentage/100) * tdr_factor * fsi
    effective_fsi = fsi + tdr_bonus
    
    # Calculate buildable area with effective FSI
    total_buildable_area_sqft = land_area_sqft * effective_fsi
    
    # Calculate green building bonus
    green_bonus = total_buildable_area_sqft * REGION_CONFIG[region]["bonuses"]["green_building"]
    
    # Calculate self-redevelopment bonus if applicable
    self_redev_bonus = 0
    if is_self_redevelopment:
        self_redev_bonus = total_buildable_area_sqft * REGION_CONFIG[region]["bonuses"]["self_redev"]
    
    # Calculate total area with bonuses
    total_final_area = total_buildable_area_sqft + green_bonus + self_redev_bonus
    
    # Calculate builder sellable area
    builder_sellable_area = total_final_area - total_offered_carpet_area
    
    # Calculate premium cost
    premium_cost_per_sqm = ready_reckoner_rate * fungible_fsi
    premium_cost = land_area_sqm * premium_cost_per_sqm
    
    # Calculate TDR cost
    tdr_cost = 0
    if tdr_percentage > 0:
        tdr_cost = land_area_sqm * ready_reckoner_rate * (tdr_percentage/100) * tdr_factor
    
    # Calculate construction cost
    construction_cost = total_final_area * construction_cost_per_sqft
    
    # Calculate rent cost
    rent_cost = total_members * rent_per_month * rent_duration_months
    
    # Calculate relocation cost
    relocation_cost = total_members * relocation_cost_per_member
    
    # Calculate GST (only for builder redevelopment)
    gst_cost = 0
    if not is_self_redevelopment:
        gst_rate = REGION_CONFIG[region]["gst"]["builder"]
        gst_cost = construction_cost * gst_rate
    
    # Calculate stamp duty
    stamp_duty_cost = 0
    if is_self_redevelopment:
        # Flat rate per unit for self-redevelopment
        stamp_duty_cost = REGION_CONFIG[region]["stamp_duty"]["self"] * total_members
    else:
        # Percentage of project value for builder redevelopment
        stamp_duty_rate = REGION_CONFIG[region]["stamp_duty"]["builder"]
        # Apply stamp duty to the offered carpet area value (for members' agreements)
        member_area_value = total_offered_carpet_area * market_rate_per_sqft
        stamp_duty_cost = member_area_value * stamp_duty_rate
    
    # Calculate total cost (now with GST and stamp duty)
    total_cost = premium_cost + tdr_cost + construction_cost + rent_cost + relocation_cost + bank_interest + gst_cost + stamp_duty_cost
    
    # Calculate project value
    project_value = builder_sellable_area * market_rate_per_sqft
    
    # Calculate total profit
    total_profit = project_value - total_cost
    
    # Calculate profit distribution
    profit_sharing_percentage = profit_sharing_with_developer
    developer_profit = 0
    society_profit = total_profit
    
    # Handle loss scenario differently
    if total_profit < 0:
        # In case of loss, society bears all loss in self-redevelopment
        if not is_self_redevelopment:
            # In builder redevelopment with loss, the loss sharing would depend on the agreement
            # For simplicity, we're assuming the loss is shared according to the profit sharing ratio
            developer_profit = total_profit * (profit_sharing_percentage / 100)
            society_profit = total_profit - developer_profit
    else:
        # Normal profit distribution for profitable projects
        if not is_self_redevelopment:
            developer_profit = total_profit * (profit_sharing_percentage / 100)
            society_profit = total_profit - developer_profit
    
    # Calculate per member profit
    per_member_profit = society_profit / total_members
    
    # Calculate number of salable flats
    num_salable_flats = builder_sellable_area / avg_new_flat_size
    
    # Return results
    return {
        "region": region,
        "project_type": project_type,
        "is_self_redevelopment": is_self_redevelopment,
        "land_area_guntha": land_area_guntha,
        "land_area_sqm": land_area_sqm,
        "ready_reckoner_rate": ready_reckoner_rate,
        "fsi": fsi,
        "effective_fsi": effective_fsi,
        "tdr_percentage": tdr_percentage,
        "tdr_cost": tdr_cost,
        "fungible_fsi": fungible_fsi,
        "total_current_carpet_area": total_current_carpet_area,
        "total_offered_carpet_area": total_offered_carpet_area,
        "total_buildable_area_sqft": total_buildable_area_sqft,
        "green_bonus": green_bonus,
        "self_redev_bonus": self_redev_bonus,
        "total_final_area": total_final_area,
        "builder_sellable_area": builder_sellable_area,
        "premium_cost_per_sqm": premium_cost_per_sqm,
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
        "profit_sharing_percentage": profit_sharing_percentage,
        "developer_profit": developer_profit,
        "society_profit": society_profit,
        "per_member_profit": per_member_profit,
        "num_salable_flats": num_salable_flats
    }
    
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

# Streamlit App
# ----------------------------------------------------

# Set page configuration
st.set_page_config(
    page_title="Redevelopment Profit Calculator",
    page_icon="🏢",
    layout="wide"
)

# Add title and description
st.title("Redevelopment Profit Calculator")
st.markdown("""
    This calculator helps housing societies evaluate the financial aspects of redevelopment projects.
    It provides transparent calculations for profit, surplus corpus, and salable flats.
    Now includes GST and stamp duty costs for more accurate financial assessment.
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
    land_area_guntha = st.number_input("Land Area (Guntha)", value=10.0, min_value=0.1)
    total_members = st.number_input("Number of Members/Flats", value=40, min_value=1, step=1)
    carpet_area = st.number_input("Current Carpet Area per Member (sqft)", value=500.0, min_value=100.0)
    extra_percentage = st.number_input("Extra Carpet Percentage", value=30.0, min_value=0.0)
    
    # Construction Parameters
    st.subheader("Construction Parameters")
    
    # Base FSI
    default_fsi = REGION_CONFIG[region]["fsi_rules"][project_type]
    fsi = st.number_input(f"Base FSI Value", value=float(default_fsi), min_value=0.1)
    
    # TDR Input
    tdr_percentage = st.number_input(
        "TDR Percentage (0-100%)", 
        min_value=0.0, 
        max_value=100.0, 
        value=0.0,
        help="Percentage of Transfer of Development Rights to apply"
    )
    
    # Fungible FSI
    default_fungible = REGION_CONFIG[region]["premium_rates"]["fungible_fsi"]
    default_fungible_pct = default_fungible * 100
    fungible_input = st.number_input(
        "Fungible FSI Percentage (25-40%)", 
        value=float(default_fungible_pct),
        min_value=0.0,
        max_value=100.0,
        help="Used to calculate premium cost based on Ready Reckoner rates"
    )
    fungible_fsi = fungible_input / 100  # Convert to decimal
    
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
    profit_sharing = 0
    if not is_self_redevelopment:
        profit_sharing = st.number_input(
            "Profit Sharing with Developer (%)", 
            value=30.0,
            min_value=0.0,
            max_value=100.0
        )
    
    # Calculate button
    calculate_button = st.button("Calculate Profit", type="primary")

# Results in the second column
with col2:
    if calculate_button:
        results = calculate_profit(
            # Location parameters
            region=region,
            ready_reckoner_year=ready_reckoner_year,
            
            # Land parameters
            land_area_guntha=land_area_guntha,
            current_carpet_area_per_member=carpet_area,
            total_members=total_members,
            extra_carpet_percentage=extra_percentage,
            
            # Construction parameters
            fsi=fsi,
            fungible_fsi=fungible_fsi,
            construction_cost_per_sqft=construction_cost,
            market_rate_per_sqft=market_rate,
            avg_new_flat_size=avg_flat_size,
            
            # Financial parameters
            rent_per_month=rent,
            rent_duration_months=rent_months,
            relocation_cost_per_member=relocation,
            bank_interest=bank_interest,
            
            # Project type
            project_type=project_type,
            is_self_redevelopment=is_self_redevelopment,
            profit_sharing_with_developer=profit_sharing,
            
            # TDR parameter
            tdr_percentage=tdr_percentage
        )
        
        # Display results in sections
        st.header("REDEVELOPMENT PROJECT ANALYSIS")
        
        # Project basics
        st.subheader("PROJECT BASICS")
        st.markdown(f"""
        - **Region**: {results['region']}
        - **Project Type**: {results['project_type']}
        - **Redevelopment Type**: {'Self-Redevelopment' if results['is_self_redevelopment'] else 'Builder Redevelopment'}
        """)
        
        # Land and area details
        st.subheader("LAND & AREA DETAILS")
        st.markdown(f"""
        - **Land Area**: {format_area(results['land_area_guntha'], 'Guntha')} ({format_area(results['land_area_sqm'], 'sqm')})
        - **Base FSI**: {results['fsi']}
        - **TDR Percentage**: {results['tdr_percentage']:.1f}%
        - **Effective FSI (with TDR)**: {results['effective_fsi']:.2f}
        - **Fungible FSI**: {results['fungible_fsi'] * 100:.1f}%
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
        - **Fungible FSI Factor**: {results['fungible_fsi']:.2f} ({results['fungible_fsi'] * 100:.1f}%)
        - **Land Area**: {format_area(results['land_area_sqm'], 'sqm')}
        - **Premium Cost Formula**: Land Area × Ready Reckoner Rate × Fungible FSI Factor
        - **Premium Cost Calculation**: {format_area(results['land_area_sqm'], 'sqm')} × {format_currency(results['ready_reckoner_rate'])}/sqm × {results['fungible_fsi']:.2f}
        - **Premium Cost per sqm**: {format_currency(results['premium_cost_per_sqm'])}/sqm
        - **Total Premium Cost**: {format_currency(results['premium_cost'])}
        - **TDR Cost**: {format_currency(results['tdr_cost'])}
        """)
        
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
        """)
        
        # Revenue and profit/loss
        st.subheader("REVENUE & PROFIT/LOSS")
        st.markdown(f"""
        - **Market Rate**: {format_currency(results['market_rate_per_sqft'])}/sqft
        - **Project Value**: {format_currency(results['project_value'])}
        - **TOTAL {'PROFIT' if results['total_profit'] >= 0 else 'LOSS'}**: {format_currency(abs(results['total_profit']))}
        """)
        
        # Profit/Loss distribution
        st.subheader("PROFIT/LOSS DISTRIBUTION")
        if results['total_profit'] >= 0:
            # Profit scenario
            if results['is_self_redevelopment']:
                st.markdown(f"""
                - **Society's Profit**: {format_currency(results['society_profit'])}
                - **Profit per Member**: {format_currency(results['per_member_profit'])}
                """)
            else:
                st.markdown(f"""
                - **Developer's Profit ({results['profit_sharing_percentage']}%)**: {format_currency(results['developer_profit'])}
                - **Society's Profit**: {format_currency(results['society_profit'])}
                - **Profit per Member**: {format_currency(results['per_member_profit'])}
                """)
        else:
            # Loss scenario
            if results['is_self_redevelopment']:
                st.markdown(f"""
                - **Society's Loss**: {format_currency(abs(results['society_profit']))}
                - **Loss per Member**: {format_currency(abs(results['per_member_profit']))}
                """)
            else:
                st.markdown(f"""
                - **Developer's Loss ({results['profit_sharing_percentage']}%)**: {format_currency(abs(results['developer_profit']))}
                - **Society's Loss**: {format_currency(abs(results['society_profit']))}
                - **Loss per Member**: {format_currency(abs(results['per_member_profit']))}
                """)
        
        # Salable flats
        st.subheader("SALABLE FLATS")
        st.markdown(f"""
        - **Number of Potential Salable Flats**: {results['num_salable_flats']:.1f}
        """)
        
        # Add a download button for the report
        st.download_button(
            label="Download Report as Text",
            data=f"""
REDEVELOPMENT PROJECT ANALYSIS
==================================================

PROJECT BASICS:
--------------
Region: {results['region']}
Project Type: {results['project_type']}
Redevelopment Type: {'Self-Redevelopment' if results['is_self_redevelopment'] else 'Builder Redevelopment'}

LAND & AREA DETAILS:
------------------
Land Area: {format_area(results['land_area_guntha'], 'Guntha')} ({format_area(results['land_area_sqm'], 'sqm')})
Base FSI: {results['fsi']}
TDR Percentage: {results['tdr_percentage']:.1f}%
Effective FSI (with TDR): {results['effective_fsi']:.2f}
Fungible FSI: {results['fungible_fsi'] * 100:.1f}%
Current Carpet Area: {format_area(results['total_current_carpet_area'])}
Offered Carpet Area: {format_area(results['total_offered_carpet_area'])}
Total Buildable Area: {format_area(results['total_buildable_area_sqft'])}
Green Building Bonus: {format_area(results['green_bonus'])}
Self-Redevelopment Bonus: {format_area(results['self_redev_bonus'])}
Total Area with Bonuses: {format_area(results['total_final_area'])}
Builder Sellable Area: {format_area(results['builder_sellable_area'])}

PREMIUM & TDR CALCULATION:
-----------------
Ready Reckoner Rate: {format_currency(results['ready_reckoner_rate'])}/sqm
Fungible FSI Factor: {results['fungible_fsi']:.2f} ({results['fungible_fsi'] * 100:.1f}%)
Land Area: {format_area(results['land_area_sqm'], 'sqm')}
Premium Cost Formula: Land Area × Ready Reckoner Rate × Fungible FSI Factor
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

REVENUE & {'PROFIT' if results['total_profit'] >= 0 else 'LOSS'}:
--------------
Market Rate: {format_currency(results['market_rate_per_sqft'])}/sqft
Project Value: {format_currency(results['project_value'])}
TOTAL {'PROFIT' if results['total_profit'] >= 0 else 'LOSS'}: {format_currency(abs(results['total_profit']))}

{'PROFIT' if results['total_profit'] >= 0 else 'LOSS'} DISTRIBUTION:
-----------------
{("Society's " + ('Profit' if results['society_profit'] >= 0 else 'Loss') + ": " + format_currency(abs(results['society_profit'])))}
{("Developer's " + ('Profit' if results['developer_profit'] >= 0 else 'Loss') + " (" + str(results['profit_sharing_percentage']) + "%): " + format_currency(abs(results['developer_profit']))) if not results['is_self_redevelopment'] else ""}
{('Profit' if results['per_member_profit'] >= 0 else 'Loss')} per Member: {format_currency(abs(results['per_member_profit']))}

SALABLE FLATS:
-----------
Number of Potential Salable Flats: {results['num_salable_flats']:.1f}
            """,
            file_name="redevelopment_report.txt",
            mime="text/plain",
        )
        
        # NEW CODE: Add visualization section
        st.subheader("Project Financial Visualization")
        
        # Create tabs for different visualizations
        viz_tab1, viz_tab2 = st.tabs(["Cost Breakdown", "Profit Analysis"])
        
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
                # Handle profit scenario
                if not results['is_self_redevelopment']:
                    # Builder redevelopment with profit
                    profit_labels = ['Developer Profit', 'Society Profit']
                    profit_values = [
                        max(0, results['developer_profit']),  # Ensure positive values
                        max(0, results['society_profit'])     # Ensure positive values
                    ]
                    # Only create pie chart if we have positive values
                    if all(v > 0 for v in profit_values):
                        ax2.pie(profit_values, labels=profit_labels, autopct='%1.1f%%', startangle=90, colors=['#e74c3c', '#3498db'])
                        ax2.axis('equal')
                        ax2.set_title('Profit Distribution')
                    else:
                        # Fallback to bar chart if any value is not positive
                        ax2.bar(profit_labels, profit_values, color=['#e74c3c', '#3498db'])
                        ax2.set_ylabel('Profit Amount (₹)')
                        ax2.set_title('Profit Distribution')
                else:
                    # Self-redevelopment with profit - compare cost vs profit
                    # For pie charts, both values must be positive
                    ax2.bar(['Total Cost', 'Project Value'], 
                           [results['total_cost'], results['project_value']], 
                           color=['#e74c3c', '#3498db'])
                    ax2.set_ylabel('Amount (₹)')
                    ax2.set_title('Cost vs. Project Value')
            else:
                # Handle loss scenario with a bar chart
                if not results['is_self_redevelopment']:
                    # Builder redevelopment with loss
                    loss_labels = ['Developer Loss', 'Society Loss']
                    loss_values = [
                        abs(results['developer_profit']),
                        abs(results['society_profit'])
                    ]
                    ax2.bar(loss_labels, loss_values, color=['#e74c3c', '#3498db'])
                    ax2.set_ylabel('Loss Amount (₹)')
                    ax2.set_title('Loss Distribution')
                else:
                    # Self-redevelopment with loss - show cost vs value comparison
                    ax2.bar(['Total Cost', 'Project Value'], 
                           [results['total_cost'], results['project_value']], 
                           color=['#e74c3c', '#3498db'])
                    ax2.set_ylabel('Amount (₹)')
                    ax2.set_title('Cost vs. Project Value (Loss Scenario)')
            
            plt.tight_layout()
            st.pyplot(fig2)

# Add detailed documentation sections
st.markdown("---")

# Premium & TDR calculation documentation
with st.expander("About Premium & TDR Calculation in Maharashtra"):
    st.markdown("""
    ## UNDERSTANDING PREMIUM & TDR CALCULATION FOR REDEVELOPMENT

    1. **REGULATORY BASIS**
       The premium and TDR calculation for redevelopment projects in Maharashtra is based on
       the Maharashtra Regional and Town Planning Act and subsequent government resolutions.
       
    2. **PREMIUM FORMULA COMPONENTS**
       Premium Cost = Land Area (sqm) × Ready Reckoner Rate (₹/sqm) × Fungible FSI Factor
       
       Where:
       - Land Area: Total plot area in square meters
       - Ready Reckoner Rate: Government-published property valuation rates (updated annually)
       - Fungible FSI Factor: Additional construction rights multiplier (typically 0.25-0.40)
    
    3. **TDR (TRANSFER OF DEVELOPMENT RIGHTS)**
       TDR allows for the transfer of development potential from one plot to another.
       
       - Increases effective FSI based on regional multiplier
       - TDR cost calculated as percentage of ready reckoner rate
       - Different regions have different TDR multipliers and rates
       - TDR can significantly increase buildable area while often being more cost-effective than premium FSI
       
    4. **GST & STAMP DUTY CONSIDERATIONS**
       - **For Builder Redevelopment**: 
         - GST: 5% on construction cost
         - Stamp Duty: 5-6% of the agreement value (varies by region)
       - **For Self-Redevelopment**:
         - GST: 0% (no service provider involved)
         - Stamp Duty: Flat ₹1,000 per unit
    
    5. **READY RECKONER RATES**
       - Published annually by the Inspector General of Registration and Controller of Stamps
       - Varies by locality and street
       - Represents the minimum value for property transactions
       
    6. **FUNGIBLE FSI FACTOR**
       - Mumbai: 0.35 (35% of Ready Reckoner rate)
       - Navi Mumbai: 0.33 (33% of Ready Reckoner rate)
       - Thane: 0.30 (30% of Ready Reckoner rate)
       - Pune: 0.28 (28% of Ready Reckoner rate)
       - Nagpur: 0.25 (25% of Ready Reckoner rate)
       - Nashik: 0.26 (26% of Ready Reckoner rate)
    """)

# Scenario Comparison Tab
with scenario_tab:
    st.header("Compare Different Scenarios")
    st.markdown("""
    This feature allows you to compare the base scenario with alternative scenarios by varying key parameters.
    See how changes in market rates, construction costs, or FSI affect your project's profitability.
    """)
    
    # Create three columns for the three scenarios
    base_col, alt1_col, alt2_col = st.columns(3)
    
    with base_col:
        st.subheader("Base Scenario")
        base_region = st.selectbox("Region", list(REGION_CONFIG.keys()), key="base_region")
        base_project_type = st.selectbox("Project Type", ["residential", "commercial"], key="base_project_type")
        base_is_self_redevelopment = st.radio(
            "Redevelopment Type", 
            ["Self-Redevelopment", "Builder Redevelopment"],
            key="base_redev_type"
        ) == "Self-Redevelopment"
        
        # Land Parameters
        base_land_area = st.number_input("Land Area (Guntha)", value=10.0, min_value=0.1, key="base_land")
        base_members = st.number_input("Number of Members/Flats", value=40, min_value=1, step=1, key="base_members")
        base_carpet_area = st.number_input("Current Carpet Area per Member (sqft)", value=500.0, min_value=100.0, key="base_carpet")
        base_extra_percentage = st.number_input("Extra Carpet Percentage", value=30.0, min_value=0.0, key="base_extra")
        
        # FSI Parameters
        default_fsi = REGION_CONFIG[base_region]["fsi_rules"][base_project_type]
        base_fsi = st.number_input(f"Base FSI Value", value=float(default_fsi), min_value=0.1, key="base_fsi")
        
        # Cost Parameters
        default_construction = REGION_CONFIG[base_region]["premium_rates"]["construction"]
        base_construction_cost = st.number_input(
            "Construction Cost per sqft (₹)", 
            value=float(default_construction),
            min_value=1000.0,
            key="base_construction"
        )
        
        base_market_rate = st.number_input("Market Rate per sqft (₹)", value=17500.0, min_value=5000.0, key="base_market")
    
    with alt1_col:
        st.subheader("Alternative Scenario 1")
        st.markdown("**What parameter would you like to vary?**")
        
        alt1_param = st.selectbox(
            "Parameter to change",
            ["Construction Cost", "Market Rate", "FSI", "Extra Carpet %"],
            key="alt1_param"
        )
        
        # How much to vary the parameter
        alt1_change = st.slider(
            "Change (%)", 
            min_value=-30, 
            max_value=30, 
            value=10,
            key="alt1_change"
        )
        
        # Show what the new value will be
        if alt1_param == "Construction Cost":
            new_value = base_construction_cost * (1 + alt1_change/100)
            st.write(f"New Construction Cost: ₹{new_value:,.2f}/sqft")
        elif alt1_param == "Market Rate":
            new_value = base_market_rate * (1 + alt1_change/100)
            st.write(f"New Market Rate: ₹{new_value:,.2f}/sqft")
        elif alt1_param == "FSI":
            new_value = base_fsi * (1 + alt1_change/100)
            st.write(f"New FSI: {new_value:.2f}")
        elif alt1_param == "Extra Carpet %":
            new_value = base_extra_percentage + alt1_change
            st.write(f"New Extra Carpet: {new_value:.1f}%")
    
    with alt2_col:
        st.subheader("Alternative Scenario 2")
        st.markdown("**What parameter would you like to vary?**")
        
        alt2_param = st.selectbox(
            "Parameter to change",
            ["Construction Cost", "Market Rate", "FSI", "Extra Carpet %"],
            key="alt2_param"
        )
        
        # How much to vary the parameter
        alt2_change = st.slider(
            "Change (%)", 
            min_value=-30, 
            max_value=30, 
            value=-10,
            key="alt2_change"
        )
        
        # Show what the new value will be
        if alt2_param == "Construction Cost":
            new_value = base_construction_cost * (1 + alt2_change/100)
            st.write(f"New Construction Cost: ₹{new_value:,.2f}/sqft")
        elif alt2_param == "Market Rate":
            new_value = base_market_rate * (1 + alt2_change/100)
            st.write(f"New Market Rate: ₹{new_value:,.2f}/sqft")
        elif alt2_param == "FSI":
            new_value = base_fsi * (1 + alt2_change/100)
            st.write(f"New FSI: {new_value:.2f}")
        elif alt2_param == "Extra Carpet %":
            new_value = base_extra_percentage + alt2_change
            st.write(f"New Extra Carpet: {new_value:.1f}%")
    
    # Common parameters (hidden in expandable section)
    with st.expander("Additional Parameters (applied to all scenarios)"):
        common_rr_year = st.selectbox("Ready Reckoner Year", [2022, 2023, 2024], key="common_rr_year")
        
        # TDR Input
        common_tdr_percentage = st.number_input(
            "TDR Percentage (0-100%)", 
            min_value=0.0, 
            max_value=100.0, 
            value=0.0,
            key="common_tdr"
        )
        
        # Fungible FSI
        default_fungible = REGION_CONFIG[base_region]["premium_rates"]["fungible_fsi"]
        default_fungible_pct = default_fungible * 100
        common_fungible_input = st.number_input(
            "Fungible FSI Percentage (25-40%)", 
            value=float(default_fungible_pct),
            min_value=0.0,
            max_value=100.0,
            key="common_fungible"
        )
        common_fungible_fsi = common_fungible_input / 100
        
        common_avg_flat_size = st.number_input("Average Size of New Salable Flats (sqft)", value=750.0, min_value=200.0, key="common_flat_size")
        
        # Financial Parameters
        common_rent = st.number_input("Monthly Rent per Flat (₹)", value=15000.0, min_value=0.0, key="common_rent")
        common_rent_months = st.number_input("Rent Duration (months)", value=36, min_value=0, step=1, key="common_rent_months")
        common_relocation = st.number_input("Relocation Cost per Member (₹)", value=20000.0, min_value=0.0, key="common_reloc")
        common_bank_interest = st.number_input("Bank Interest (₹)", value=50000000.0, min_value=0.0, key="common_bank")
        
        # Profit Sharing (if builder redevelopment)
        common_profit_sharing = 0
        if not base_is_self_redevelopment:
            common_profit_sharing = st.number_input(
                "Profit Sharing with Developer (%)", 
                value=30.0,
                min_value=0.0,
                max_value=100.0,
                key="common_profit_sharing"
            )
    
    # Calculate button for comparison
    compare_button = st.button("Compare Scenarios", type="primary")
    
    if compare_button:
        # Calculate base scenario
        base_results = calculate_profit(
            region=base_region,
            ready_reckoner_year=common_rr_year,
            land_area_guntha=base_land_area,
            current_carpet_area_per_member=base_carpet_area,
            total_members=base_members,
            extra_carpet_percentage=base_extra_percentage,
            fsi=base_fsi,
            fungible_fsi=common_fungible_fsi,
            construction_cost_per_sqft=base_construction_cost,
            market_rate_per_sqft=base_market_rate,
            avg_new_flat_size=common_avg_flat_size,
            rent_per_month=common_rent,
            rent_duration_months=common_rent_months,
            relocation_cost_per_member=common_relocation,
            bank_interest=common_bank_interest,
            project_type=base_project_type,
            is_self_redevelopment=base_is_self_redevelopment,
            profit_sharing_with_developer=common_profit_sharing,
            tdr_percentage=common_tdr_percentage
        )
        
        # Calculate scenario 1
        alt1_construction_cost = base_construction_cost
        alt1_market_rate = base_market_rate
        alt1_fsi = base_fsi
        alt1_extra_percentage = base_extra_percentage
        
        # Update the varied parameter
        if alt1_param == "Construction Cost":
            alt1_construction_cost = base_construction_cost * (1 + alt1_change/100)
        elif alt1_param == "Market Rate":
            alt1_market_rate = base_market_rate * (1 + alt1_change/100)
        elif alt1_param == "FSI":
            alt1_fsi = base_fsi * (1 + alt1_change/100)
        elif alt1_param == "Extra Carpet %":
            alt1_extra_percentage = base_extra_percentage + alt1_change
        
        # Calculate alt1 results
        alt1_results = calculate_profit(
            region=base_region,
            ready_reckoner_year=common_rr_year,
            land_area_guntha=base_land_area,
            current_carpet_area_per_member=base_carpet_area,
            total_members=base_members,
            extra_carpet_percentage=alt1_extra_percentage,
            fsi=alt1_fsi,
            fungible_fsi=common_fungible_fsi,
            construction_cost_per_sqft=alt1_construction_cost,
            market_rate_per_sqft=alt1_market_rate,
            avg_new_flat_size=common_avg_flat_size,
            rent_per_month=common_rent,
            rent_duration_months=common_rent_months,
            relocation_cost_per_member=common_relocation,
            bank_interest=common_bank_interest,
            project_type=base_project_type,
            is_self_redevelopment=base_is_self_redevelopment,
            profit_sharing_with_developer=common_profit_sharing,
            tdr_percentage=common_tdr_percentage
        )
        
        # Calculate scenario 2
        alt2_construction_cost = base_construction_cost
        alt2_market_rate = base_market_rate
        alt2_fsi = base_fsi
        alt2_extra_percentage = base_extra_percentage
        
        # Update the varied parameter
        if alt2_param == "Construction Cost":
            alt2_construction_cost = base_construction_cost * (1 + alt2_change/100)
        elif alt2_param == "Market Rate":
            alt2_market_rate = base_market_rate * (1 + alt2_change/100)
        elif alt2_param == "FSI":
            alt2_fsi = base_fsi * (1 + alt2_change/100)
        elif alt2_param == "Extra Carpet %":
            alt2_extra_percentage = base_extra_percentage + alt2_change
            
        # Calculate alt2 results
        alt2_results = calculate_profit(
            region=base_region,
            ready_reckoner_year=common_rr_year,
            land_area_guntha=base_land_area,
            current_carpet_area_per_member=base_carpet_area,
            total_members=base_members,
            extra_carpet_percentage=alt2_extra_percentage,
            fsi=alt2_fsi,
            fungible_fsi=common_fungible_fsi,
            construction_cost_per_sqft=alt2_construction_cost,
            market_rate_per_sqft=alt2_market_rate,
            avg_new_flat_size=common_avg_flat_size,
            rent_per_month=common_rent,
            rent_duration_months=common_rent_months,
            relocation_cost_per_member=common_relocation,
            bank_interest=common_bank_interest,
            project_type=base_project_type,
            is_self_redevelopment=base_is_self_redevelopment,
            profit_sharing_with_developer=common_profit_sharing,
            tdr_percentage=common_tdr_percentage
        )
        
        # Display results comparison
        st.header("Scenario Comparison Results")
        
        # Create a comparison table
        comparison_data = {
            "Parameter": [
                "Total Cost",
                "Project Value",
                f"Total {'Profit/Loss' if base_results['total_profit'] < 0 else 'Profit'}",
                "Society's Share",
                "Per Member"
            ],
            "Base Scenario": [
                format_currency(base_results['total_cost']),
                format_currency(base_results['project_value']),
                format_currency(base_results['total_profit']),
                format_currency(base_results['society_profit']),
                format_currency(base_results['per_member_profit'])
            ],
            f"Alt 1: {alt1_param} {'+' if alt1_change > 0 else ''}{alt1_change}%": [
                format_currency(alt1_results['total_cost']),
                format_currency(alt1_results['project_value']),
                format_currency(alt1_results['total_profit']),
                format_currency(alt1_results['society_profit']),
                format_currency(alt1_results['per_member_profit'])
            ],
            f"Alt 2: {alt2_param} {'+' if alt2_change > 0 else ''}{alt2_change}%": [
                format_currency(alt2_results['total_cost']),
                format_currency(alt2_results['project_value']),
                format_currency(alt2_results['total_profit']),
                format_currency(alt2_results['society_profit']),
                format_currency(alt2_results['per_member_profit'])
            ]
        }
        
        # Display as a Streamlit table
        st.table(comparison_data)
        
        # Visualization of the comparison
        st.subheader("Profit Comparison")
        
        # Create bar chart
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Data for the chart
        scenarios = ['Base Scenario', f'Alt 1: {alt1_param} {alt1_change}%', f'Alt 2: {alt2_param} {alt2_change}%']
        profits = [
            base_results['total_profit'], 
            alt1_results['total_profit'], 
            alt2_results['total_profit']
        ]
        
        # Determine colors based on profit/loss
        colors = ['green' if p >= 0 else 'red' for p in profits]
        
        # Create the bars
        bars = ax.bar(scenarios, profits, color=colors)
        
        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            label_text = f'₹{abs(height)/10000000:.2f} Cr'
            ax.text(
                bar.get_x() + bar.get_width()/2, 
                height * (1.05 if height >= 0 else 0.95),
                label_text,
                ha='center', 
                va='bottom' if height >= 0 else 'top',
                fontweight='bold'
            )
        
        # Add labels and title
        ax.set_ylabel('Profit/Loss (₹)')
        ax.set_title('Profit Comparison Across Scenarios')
        ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        
        # Display the chart
        st.pyplot(fig)
        
        # Additional analysis and insights
        st.subheader("Analysis and Insights")
        
        # Calculate percentage changes
        if base_results['total_profit'] != 0:
            alt1_profit_change_pct = (alt1_results['total_profit'] - base_results['total_profit']) / abs(base_results['total_profit']) * 100
            alt2_profit_change_pct = (alt2_results['total_profit'] - base_results['total_profit']) / abs(base_results['total_profit']) * 100
        else:
            alt1_profit_change_pct = 0
            alt2_profit_change_pct = 0
        
        st.markdown(f"""
        ### Impact Analysis
        
        #### Alternative Scenario 1: {alt1_param} {'+' if alt1_change > 0 else ''}{alt1_change}%
        - **Profit Change**: {format_currency(alt1_results['total_profit'] - base_results['total_profit'])} ({alt1_profit_change_pct:.1f}%)
        - **Society's Share Change**: {format_currency(alt1_results['society_profit'] - base_results['society_profit'])}
        - **Per Member Change**: {format_currency(alt1_results['per_member_profit'] - base_results['per_member_profit'])}
        
        #### Alternative Scenario 2: {alt2_param} {'+' if alt2_change > 0 else ''}{alt2_change}%
        - **Profit Change**: {format_currency(alt2_results['total_profit'] - base_results['total_profit'])} ({alt2_profit_change_pct:.1f}%)
        - **Society's Share Change**: {format_currency(alt2_results['society_profit'] - base_results['society_profit'])}
        - **Per Member Change**: {format_currency(alt2_results['per_member_profit'] - base_results['per_member_profit'])}
        """)
        
        # Key observations based on the results
        st.markdown("### Key Observations")
        
        observations = []
        
        # Check which parameter has the biggest impact
        param1_impact = abs(alt1_results['total_profit'] - base_results['total_profit']) / abs(alt1_change) if alt1_change != 0 else 0
        param2_impact = abs(alt2_results['total_profit'] - base_results['total_profit']) / abs(alt2_change) if alt2_change != 0 else 0
        
        most_sensitive = alt1_param if param1_impact > param2_impact else alt2_param
        observations.append(f"The project is most sensitive to changes in **{most_sensitive}**.")
        
        # Check if any scenario switches from profit to loss or vice versa
        base_profitable = base_results['total_profit'] >= 0
        alt1_profitable = alt1_results['total_profit'] >= 0
        alt2_profitable = alt2_results['total_profit'] >= 0
        
        if base_profitable != alt1_profitable:
            if alt1_profitable:
                observations.append(f"Increasing {alt1_param} by {alt1_change}% changes the project from loss to profit.")
            else:
                observations.append(f"Increasing {alt1_param} by {alt1_change}% changes the project from profit to loss.")
                
        if base_profitable != alt2_profitable:
            if alt2_profitable:
                observations.append(f"Changing {alt2_param} by {alt2_change}% changes the project from loss to profit.")
            else:
                observations.append(f"Changing {alt2_param} by {alt2_change}% changes the project from profit to loss.")
        
        # Check which scenario is most profitable
        scenarios = ["Base", f"Alt 1 ({alt1_param})", f"Alt 2 ({alt2_param})"]
        profits = [base_results['total_profit'], alt1_results['total_profit'], alt2_results['total_profit']]
        most_profitable_idx = profits.index(max(profits))
        observations.append(f"The **{scenarios[most_profitable_idx]}** scenario is most profitable.")
        
        # Display the observations
        for obs in observations:
            st.markdown(f"- {obs}")
            
        # Conclusion
        st.markdown("### Conclusion")
        if most_profitable_idx == 0:
            st.markdown("The base scenario appears to be the most profitable option based on the parameters analyzed.")
        else:
            better_scenario = "Alternative Scenario 1" if most_profitable_idx == 1 else "Alternative Scenario 2"
            better_param = alt1_param if most_profitable_idx == 1 else alt2_param
            better_change = alt1_change if most_profitable_idx == 1 else alt2_change
            
            st.markdown(f"""
            {better_scenario} with {better_param} changed by {better_change}% appears to be more profitable 
            than the base scenario. Consider focusing efforts on optimizing this parameter to maximize project returns.
            """)

# Add detailed documentation sections
st.markdown("---")
