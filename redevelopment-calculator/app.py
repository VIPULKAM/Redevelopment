# File: main.py
import streamlit as st
import matplotlib.pyplot as plt
from visitor_counter import display_visitor_counter

# Import modules
from config import ROAD_WIDTH_FSI_RULES, TDR_CONFIG, REGION_CONFIG
from utils import (
    get_ready_reckoner_rate, get_fsi_based_on_road_width,
    format_currency, format_area,
    get_land_area_input, get_fungible_input, get_ancillary_input
)
from calculator import calculate_profit
from ui_components import (
    display_basic_results, display_land_details, display_premium_calculation,
    display_tdr_analysis, display_cost_analysis, display_revenue,
    display_profit_distribution, display_visualization, create_download_report
)

# Configure page and add Google Analytics
st.set_page_config(
    page_title="Redevelopment Financial Calculator",
    page_icon="🏢",
    layout="wide"
)

# Google Analytics integration
#GA_TRACKING_ID = "G-04LKXXK1GN"  # Replace with your actual tracking ID
google_analytics_js = f"""
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-S650KV1T6R"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());

  gtag('config', 'G-S650KV1T6R');
</script>
"""

def cookie_consent():
    cookie_consent_key = "cookie_consent"
    
    if cookie_consent_key not in st.session_state:
        st.session_state[cookie_consent_key] = False
       
        col1, col2 = st.columns([3, 1])
        with col1:
            st.info("This site uses cookies to analyze traffic and enhance user experience.")
        with col2:
            if st.button("Accept Cookies"):
                st.session_state[cookie_consent_key] = True
                st.rerun()
    
    return st.session_state[cookie_consent_key]

# Then use it to conditionally load GA:
#if cookie_consent():
st.markdown(google_analytics_js, unsafe_allow_html=True)


# Add Firebase visitor counter
display_visitor_counter()

# Initialize session state for parameter persistence
if 'params' not in st.session_state:
    st.session_state.params = {
        'region': 'Mumbai',
        'ready_reckoner_year': 2024,
        'project_type': 'residential',
        'is_self_redevelopment': True,
        'land_area': 1000.0,
        'road_width': 12.0,
        'total_members': 40,
        'carpet_area': 500.0,
        'extra_percentage': 30.0,
        'tdr_percentage': 0.0,
        'fungible_fsi': 0.35,
        'ancillary_fsi': 0.0,
        'construction_cost': 3000.0,
        'market_rate': 17500.0,
        'avg_flat_size': 750.0,
        'rent': 15000.0,
        'rent_months': 36,
        'relocation': 20000.0,
        'bank_interest': 50000000.0
    }

# Cache the ready reckoner rates for faster access
@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_cached_ready_reckoner_rate(region, year):
    return get_ready_reckoner_rate(region, year)

# Cache the calculator function to improve performance
@st.cache_data(ttl=60)  # Cache for 1 minute
def cached_calculate_profit(**kwargs):
    return calculate_profit(**kwargs)

# Track a GA event (can be used for button clicks, etc.)
#def track_event(event_category, event_action, event_label=None):
#    js_code = f"""
#    <script>
#    gtag('event', '{event_action}', {{
#        'event_category': '{event_category}',
#        'event_label': '{event_label or "None"}'
#    }});
#    </script>
#    """
#    st.markdown(js_code, unsafe_allow_html=True)

# Main Application UI
def main():
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
            region = st.selectbox(
                "Region", 
                list(REGION_CONFIG.keys()),
                key="region",
                on_change=lambda: track_event("Input", "Region Change", st.session_state.region)
            )
            st.session_state.params['region'] = region
            
            ready_reckoner_year = st.selectbox(
                "Ready Reckoner Year", 
                [2022, 2023, 2024],
                key="ready_reckoner_year"
            )
            st.session_state.params['ready_reckoner_year'] = ready_reckoner_year
            
            project_type = st.selectbox(
                "Project Type", 
                ["residential", "commercial"],
                key="project_type"
            )
            st.session_state.params['project_type'] = project_type
            
            is_self_redevelopment = st.radio(
                "Redevelopment Type", 
                ["Self-Redevelopment", "Builder Redevelopment"],
                key="redevelopment_type"
            ) == "Self-Redevelopment"
            st.session_state.params['is_self_redevelopment'] = is_self_redevelopment
            
            # Land Parameters
            st.subheader("Land Parameters")
            land_area = get_land_area_input(region)
            st.session_state.params['land_area'] = land_area
            
            # Show road width input only for Mumbai
            road_width = None
            if region == "Mumbai":
                road_width = st.number_input(
                    "Road Width Abutting Property (meters)", 
                    min_value=6.0, 
                    max_value=30.0, 
                    value=12.0,
                    key="road_width",
                    help="FSI varies based on road width in Mumbai"
                )
                st.session_state.params['road_width'] = road_width
            
            total_members = st.number_input(
                "Number of Members/Flats", 
                value=40, 
                min_value=1, 
                step=1,
                key="total_members"
            )
            st.session_state.params['total_members'] = total_members
            
            carpet_area = st.number_input(
                "Current Carpet Area per Member (sqft)", 
                value=500.0, 
                min_value=100.0,
                key="carpet_area"
            )
            st.session_state.params['carpet_area'] = carpet_area
            
            extra_percentage = st.number_input(
                "Extra Carpet Percentage", 
                value=30.0, 
                min_value=0.0,
                key="extra_percentage"
            )
            st.session_state.params['extra_percentage'] = extra_percentage
            
            # Construction Parameters
            st.subheader("Construction Parameters")
            
            # Base FSI - dynamic based on road width for Mumbai
            if region == "Mumbai" and road_width is not None:
                default_fsi = get_fsi_based_on_road_width(region, project_type, road_width)
                fsi_text = f"Base FSI Value (Road width based: {default_fsi})"
            else:
                default_fsi = REGION_CONFIG[region]["fsi_rules"][project_type]
                fsi_text = "Base FSI Value"
                
            fsi = st.number_input(
                fsi_text, 
                value=float(default_fsi), 
                min_value=0.1,
                key="fsi"
            )
            st.session_state.params['fsi'] = fsi
            
            # TDR Input
            tdr_percentage = st.number_input(
                "TDR Percentage (0-100%)", 
                min_value=0.0, 
                max_value=100.0, 
                value=st.session_state.params.get('tdr_percentage', 0.0),
                key="tdr_percentage",
                help="Percentage of Transfer of Development Rights to apply"
            )
            st.session_state.params['tdr_percentage'] = tdr_percentage
            
            tdr_type = None
            tdr_market_rate = None
            if tdr_percentage > 0:
                if region == "Mumbai":
                    tdr_type = st.selectbox(
                        "TDR Type",
                        options=REGION_CONFIG[region]["tdr_types_available"],
                        format_func=lambda x: f"{x} ({TDR_CONFIG['Mumbai']['types'][x]['description']})",
                        key="tdr_type",
                        help="Select the type of TDR being utilized"
                    )
                    st.session_state.params['tdr_type'] = tdr_type
                    
                    tdr_market_rate = st.slider(
                        "Current TDR Market Rate (₹/sqft)",
                        min_value=TDR_CONFIG["Mumbai"]["min_rate"],
                        max_value=TDR_CONFIG["Mumbai"]["max_rate"],
                        value=TDR_CONFIG["Mumbai"]["market_rate"],
                        key="tdr_market_rate",
                        help="Adjust based on current market conditions"
                    )
                    st.session_state.params['tdr_market_rate'] = tdr_market_rate
                else:
                    tdr_type = "Standard TDR"
                    st.session_state.params['tdr_type'] = tdr_type
                    st.info(f"Using standard TDR with region-specific multiplier of {REGION_CONFIG[region]['fsi_rules']['tdr_multiplier']}x for {region}")
            
            # Conditional inputs for fungible vs ancillary FSI
            fungible_fsi = get_fungible_input(region)
            st.session_state.params['fungible_fsi'] = fungible_fsi
            
            ancillary_fsi = get_ancillary_input(region)
            st.session_state.params['ancillary_fsi'] = ancillary_fsi
            
            # Cost parameters
            default_construction = REGION_CONFIG[region]["premium_rates"]["construction"]
            construction_cost = st.number_input(
                "Construction Cost per sqft (₹)", 
                value=float(default_construction),
                min_value=1000.0,
                key="construction_cost"
            )
            st.session_state.params['construction_cost'] = construction_cost
            
            market_rate = st.number_input(
                "Market Rate per sqft (₹)", 
                value=17500.0, 
                min_value=5000.0,
                key="market_rate"
            )
            st.session_state.params['market_rate'] = market_rate
            
            avg_flat_size = st.number_input(
                "Average Size of New Salable Flats (sqft)", 
                value=750.0, 
                min_value=200.0,
                key="avg_flat_size"
            )
            st.session_state.params['avg_flat_size'] = avg_flat_size
            
            # Financial Parameters
            st.subheader("Financial Parameters")
            rent = st.number_input(
                "Monthly Rent per Flat (₹)", 
                value=15000.0, 
                min_value=0.0,
                key="rent"
            )
            st.session_state.params['rent'] = rent
            
            rent_months = st.number_input(
                "Rent Duration (months)", 
                value=36, 
                min_value=0, 
                step=1,
                key="rent_months"
            )
            st.session_state.params['rent_months'] = rent_months
            
            relocation = st.number_input(
                "Relocation Cost per Member (₹)", 
                value=20000.0, 
                min_value=0.0,
                key="relocation"
            )
            st.session_state.params['relocation'] = relocation
            
            bank_interest = st.number_input(
                "Bank Interest (₹)", 
                value=50000000.0, 
                min_value=0.0,
                key="bank_interest"
            )
            st.session_state.params['bank_interest'] = bank_interest
            
            # Profit Sharing (if builder redevelopment)
            profit_sharing = 100  # Default to 100% for builder as requested
            if not is_self_redevelopment:
                st.info("For builder redevelopment, the builder typically takes 100% of the profit/loss.")
                profit_sharing = 100  # Fixed at 100% for builder redevelopment
            
            # Add save button for current parameters
            if st.button("Save Parameters"):
                st.session_state.saved_params = st.session_state.params.copy()
                st.success("Parameters saved successfully!")
                track_event("User Action", "Save Parameters")
            
            # Calculate button
            calculate_button = st.button(
                "Calculate Result", 
                type="primary",
                on_click=lambda: track_event("User Action", "Calculate", f"Region:{region}")
            )

        # Results in the second column
        with col2:
            if calculate_button:
                # Use the cached calculation function
                results = cached_calculate_profit(
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
                
                # Track if project is profitable in GA
                is_profitable = results['total_profit'] >= 0
                track_event("Result", "Profitability", "Profitable" if is_profitable else "Loss-making")
                
                # Display all results
                st.header("REDEVELOPMENT PROJECT ANALYSIS")
                
                # Display results using UI components
                display_basic_results(results)
                display_land_details(results, region, REGION_CONFIG)
                display_premium_calculation(results, region, REGION_CONFIG)
                
                # Show TDR information if applicable
                if results.get('tdr_percentage', 0) > 0:
                    display_tdr_analysis(results, region, project_type, TDR_CONFIG, REGION_CONFIG)
                
                display_cost_analysis(results)
                
                # Handle profit/loss
                is_profitable = results['total_profit'] >= 0
                display_revenue(results, is_profitable)
                display_profit_distribution(results, is_profitable)
                
                # Visualizations
                display_visualization(results, region, is_profitable, REGION_CONFIG)
                
                # Report download
                report_text = create_download_report(results, region, is_profitable, REGION_CONFIG)
                
                # Track download event
                download_button = st.download_button(
                    label="Download Report as Text",
                    data=report_text,
                    file_name=f"redevelopment_report_{region}.txt",
                    mime="text/plain",
                    on_click=lambda: track_event("User Action", "Download Report")
                )

    # Scenario comparison tab
    with scenario_tab:
        st.header("Scenario Comparison")
        st.markdown("""
        Coming soon! This feature will allow you to compare multiple redevelopment scenarios side by side.
        """)
        
        if st.button("Notify me when this feature is available", key="notify-feature"):
            track_event("User Interest", "Feature Interest", "Scenario Comparison")
            st.success("Thank you for your interest! We'll notify you when this feature becomes available.")

if __name__ == "__main__":
    main()
