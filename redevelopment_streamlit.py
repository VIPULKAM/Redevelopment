import streamlit as st

# Copy your constants and functions from redev.py
# ----------------------------------------------------
# First, copy the REGION_CONFIG dictionary
REGION_CONFIG = {
    "Mumbai": {
        "fsi_rules": {
            "residential": 2.5,
            "commercial": 5.0,
            "tdr_multiplier": 2.5
        },
        "premium_rates": {
            "construction": 3000,  # Default construction cost per sqft
            "fungible_fsi": 0.35   # Fungible FSI percentage
        },
        "bonuses": {
            "green_building": 0.07,
            "self_redev": 0.10,
            "ancillary": 0.60
        },
        "parking": {
            "redev_reduction": 0.20,
            "car_lift_threshold": 2000
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
        }
    }
}

# Copy your other functions: get_ready_reckoner_rate, calculate_profit, format_currency, format_area
# ...

def get_ready_reckoner_rate(region, year):
    ready_reckoner_rates = {
        "Mumbai": {2022: 150000, 2023: 160000, 2024: 170000},
        "Thane": {2022: 100000, 2023: 110000, 2024: 120000}
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
        profit_sharing_with_developer
    ):
    """Calculate profit from redevelopment project."""
    # Convert guntha to square meters (1 guntha = 101.17 sqm)
    land_area_sqm = land_area_guntha * 101.17
    
    # Get ready reckoner rate for the region and year
    ready_reckoner_rate = get_ready_reckoner_rate(region, ready_reckoner_year)
    
    # Calculate current carpet area
    total_current_carpet_area = current_carpet_area_per_member * total_members
    
    # Calculate offered carpet area (with extra percentage)
    total_offered_carpet_area = total_current_carpet_area * (1 + extra_carpet_percentage/100)
    
    # Calculate buildable area
    # Convert to sqft (1 sqm = 10.764 sqft)
    land_area_sqft = land_area_sqm * 10.764
    total_buildable_area_sqft = land_area_sqft * fsi
    
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
    
    # Calculate construction cost
    construction_cost = total_final_area * construction_cost_per_sqft
    
    # Calculate rent cost
    rent_cost = total_members * rent_per_month * rent_duration_months
    
    # Calculate relocation cost
    relocation_cost = total_members * relocation_cost_per_member
    
    # Calculate total cost
    total_cost = premium_cost + construction_cost + rent_cost + relocation_cost + bank_interest
    
    # Calculate project value
    project_value = builder_sellable_area * market_rate_per_sqft
    
    # Calculate total profit
    total_profit = project_value - total_cost
    
    # Calculate profit distribution
    profit_sharing_percentage = profit_sharing_with_developer
    developer_profit = 0
    society_profit = total_profit
    
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
""")

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
    default_fsi = REGION_CONFIG[region]["fsi_rules"][project_type]
    fsi = st.number_input(f"FSI Value", value=default_fsi, min_value=0.1)
    
    default_fungible = REGION_CONFIG[region]["premium_rates"]["fungible_fsi"]
    default_fungible_pct = default_fungible * 100
    fungible_input = st.number_input(
        "Fungible FSI Percentage (25-40%)", 
        value=default_fungible_pct,
        min_value=0.0,
        max_value=100.0,
        help="Used to calculate premium cost based on Ready Reckoner rates"
    )
    fungible_fsi = fungible_input / 100  # Convert to decimal
    
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
            profit_sharing_with_developer=profit_sharing
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
        - **FSI Applied**: {results['fsi']}
        - **Fungible FSI**: {results['fungible_fsi'] * 100:.1f}%
        - **Current Carpet Area**: {format_area(results['total_current_carpet_area'])}
        - **Offered Carpet Area**: {format_area(results['total_offered_carpet_area'])}
        - **Total Buildable Area**: {format_area(results['total_buildable_area_sqft'])}
        - **Green Building Bonus**: {format_area(results['green_bonus'])}
        - **Total Area with Bonuses**: {format_area(results['total_final_area'])}
        - **Builder Sellable Area**: {format_area(results['builder_sellable_area'])}
        """)
        
        # Premium calculation
        st.subheader("PREMIUM CALCULATION")
        st.markdown(f"""
        - **Ready Reckoner Rate**: {format_currency(results['ready_reckoner_rate'])}/sqm
        - **Fungible FSI Factor**: {results['fungible_fsi']:.2f} ({results['fungible_fsi'] * 100:.1f}%)
        - **Land Area**: {format_area(results['land_area_sqm'], 'sqm')}
        - **Premium Cost Formula**: Land Area × Ready Reckoner Rate × Fungible FSI Factor
        - **Premium Cost Calculation**: {format_area(results['land_area_sqm'], 'sqm')} × {format_currency(results['ready_reckoner_rate'])}/sqm × {results['fungible_fsi']:.2f}
        - **Premium Cost per sqm**: {format_currency(results['premium_cost_per_sqm'])}/sqm
        - **Total Premium Cost**: {format_currency(results['premium_cost'])}
        """)
        
        # Cost analysis
        st.subheader("COST ANALYSIS")
        st.markdown(f"""
        - **Premium Cost**: {format_currency(results['premium_cost'])}
        - **Construction Cost**: {format_currency(results['construction_cost'])} ({format_currency(results['construction_cost_per_sqft'])}/sqft)
        - **Rent Cost**: {format_currency(results['rent_cost'])}
        - **Relocation Cost**: {format_currency(results['relocation_cost'])}
        - **Bank Interest**: {format_currency(results['bank_interest'])}
        - **TOTAL PROJECT COST**: {format_currency(results['total_cost'])}
        """)
        
        # Revenue and profit
        st.subheader("REVENUE & PROFIT")
        st.markdown(f"""
        - **Market Rate**: {format_currency(results['market_rate_per_sqft'])}/sqft
        - **Project Value**: {format_currency(results['project_value'])}
        - **TOTAL PROFIT**: {format_currency(results['total_profit'])}
        """)
        
        # Profit distribution
        st.subheader("PROFIT DISTRIBUTION")
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
FSI Applied: {results['fsi']}
Fungible FSI: {results['fungible_fsi'] * 100:.1f}%
Current Carpet Area: {format_area(results['total_current_carpet_area'])}
Offered Carpet Area: {format_area(results['total_offered_carpet_area'])}
Total Buildable Area: {format_area(results['total_buildable_area_sqft'])}
Green Building Bonus: {format_area(results['green_bonus'])}
Total Area with Bonuses: {format_area(results['total_final_area'])}
Builder Sellable Area: {format_area(results['builder_sellable_area'])}

PREMIUM CALCULATION:
-----------------
Ready Reckoner Rate: {format_currency(results['ready_reckoner_rate'])}/sqm
Fungible FSI Factor: {results['fungible_fsi']:.2f} ({results['fungible_fsi'] * 100:.1f}%)
Land Area: {format_area(results['land_area_sqm'], 'sqm')}
Premium Cost Formula: Land Area × Ready Reckoner Rate × Fungible FSI Factor
Premium Cost: {format_currency(results['premium_cost'])}

COST ANALYSIS:
------------
Premium Cost: {format_currency(results['premium_cost'])}
Construction Cost: {format_currency(results['construction_cost'])} ({format_currency(results['construction_cost_per_sqft'])}/sqft)
Rent Cost: {format_currency(results['rent_cost'])}
Relocation Cost: {format_currency(results['relocation_cost'])}
Bank Interest: {format_currency(results['bank_interest'])}
TOTAL PROJECT COST: {format_currency(results['total_cost'])}

REVENUE & PROFIT:
--------------
Market Rate: {format_currency(results['market_rate_per_sqft'])}/sqft
Project Value: {format_currency(results['project_value'])}
TOTAL PROFIT: {format_currency(results['total_profit'])}

PROFIT DISTRIBUTION:
-----------------
{"Society's Profit: " + format_currency(results['society_profit'])}
{"Developer's Profit (" + str(results['profit_sharing_percentage']) + "%): " + format_currency(results['developer_profit']) if not results['is_self_redevelopment'] else ""}
Profit per Member: {format_currency(results['per_member_profit'])}

SALABLE FLATS:
-----------
Number of Potential Salable Flats: {results['num_salable_flats']:.1f}
            """,
            file_name="redevelopment_report.txt",
            mime="text/plain",
        )

# Add information section at the bottom
st.markdown("---")
with st.expander("About Premium Calculation in Maharashtra"):
    st.markdown("""
    ## UNDERSTANDING PREMIUM CALCULATION FOR REDEVELOPMENT

    1. **REGULATORY BASIS**
       The premium calculation for redevelopment projects in Maharashtra is based on
       the Maharashtra Regional and Town Planning Act and subsequent government resolutions.
       
    2. **FORMULA COMPONENTS**
       Premium Cost = Land Area (sqm) × Ready Reckoner Rate (₹/sqm) × Fungible FSI Factor
       
       Where:
       - Land Area: Total plot area in square meters
       - Ready Reckoner Rate: Government-published property valuation rates (updated annually)
       - Fungible FSI Factor: Additional construction rights multiplier (typically 0.25-0.40)
       
    3. **READY RECKONER RATES**
       - Published annually by the Inspector General of Registration and Controller of Stamps
       - Varies by locality and street
       - Represents the minimum value for property transactions
       
    4. **FUNGIBLE FSI FACTOR**
       - Mumbai: 0.35 (35% of Ready Reckoner rate)
       - Thane: 0.30 (30% of Ready Reckoner rate)
       - Typically ranges from 0.25 to 0.40 depending on municipality
    """)

with st.expander("About This Calculator"):
    st.markdown("""
    ## About This Calculator

    This calculator was created to bring transparency to housing society redevelopment projects. It helps society members understand:

    - The true financial impact of redevelopment
    - Potential profits for builders and society members
    - Number of salable flats generated
    - All costs involved in the redevelopment process

    This tool is for educational purposes only. Please consult with professionals before making redevelopment decisions.
    """)
