# File: utils.py
# Contains utility functions for the application

import streamlit as st
from config import ROAD_WIDTH_FSI_RULES, REGION_CONFIG, READY_RECKONER_RATES

@st.cache_data(ttl=3600 * 24)  # Cache for 24 hours
def get_ready_reckoner_rate(region, year):
    """Get ready reckoner rate for region and year."""
    return READY_RECKONER_RATES.get(region, {}).get(year, 0)

@st.cache_data(ttl=3600)  # Cache for 1 hour
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
    try:
        if amount >= 10000000:  # Convert to crores
            return f"₹{amount/10000000:.2f} Cr (₹{amount:,.2f})"
        elif amount >= 100000:  # Convert to lakhs
            return f"₹{amount/100000:.2f} Lakh (₹{amount:,.2f})"
        else:
            return f"₹{amount:,.2f}"
    except (TypeError, ValueError):
        return f"₹{0:,.2f}"

def format_area(area, unit="sqft"):
    """Format area with commas and unit."""
    try:
        return f"{area:,.2f} {unit}"
    except (TypeError, ValueError):
        return f"{0:,.2f} {unit}"

def get_land_area_input(region):
    """Conditional land area input based on region"""
    if REGION_CONFIG[region]["uses_guntha"]:
        return st.number_input("Land Area (Guntha)", 
                              min_value=0.1, 
                              value=st.session_state.params.get('land_area', 10.0),
                              key="land_area_guntha")
    else:
        return st.number_input("Land Area (Sq.m)", 
                              min_value=1.0, 
                              value=st.session_state.params.get('land_area', 1000.0),
                              key="land_area_sqm")

def get_fungible_input(region):
    """Show fungible FSI input only for Mumbai"""
    if REGION_CONFIG[region]["has_fungible"]:
        default = REGION_CONFIG[region]["premium_rates"]["fungible_fsi"] * 100
        saved_value = st.session_state.params.get('fungible_fsi', default/100) * 100
        return st.number_input("Fungible FSI (%)", 
                             min_value=0.0, 
                             max_value=40.0, 
                             value=saved_value,
                             help="In Mumbai, this adds to the buildable area and incurs premium cost",
                             key="fungible_fsi_input") / 100
    return 0.0

def get_ancillary_input(region):
    """Ancillary FSI input for non-Mumbai regions"""
    if not REGION_CONFIG[region]["has_fungible"]:
        saved_value = st.session_state.params.get('ancillary_fsi', 0.0) * 100
        return st.number_input("Ancillary FSI (%)", 
                             min_value=0.0, 
                             max_value=30.0,
                             value=saved_value,
                             help="Percentage of FSI to purchase as ancillary, which adds to buildable area",
                             key="ancillary_fsi_input") / 100
    return 0.0

# Function to validate numerical inputs
def validate_number(value, min_value=None, max_value=None, default=0):
    """Validate a numerical input and return a safe value."""
    try:
        value = float(value)
        if min_value is not None and value < min_value:
            return min_value
        if max_value is not None and value > max_value:
            return max_value
        return value
    except (TypeError, ValueError):
        return default

def get_default_parameters(region):
    """Get default parameters for a region"""
    params = {
        'ready_reckoner_year': 2024,
        'project_type': 'residential',
        'is_self_redevelopment': True,
        'land_area': 1000.0 if not REGION_CONFIG[region]["uses_guntha"] else 10.0,
        'road_width': 12.0 if region == 'Mumbai' else None,
        'total_members': 40,
        'carpet_area': 500.0,
        'extra_percentage': 30.0,
        'tdr_percentage': 0.0,
        'tdr_type': 'Road TDR' if region == 'Mumbai' else 'Standard TDR',
        'tdr_market_rate': TDR_CONFIG['Mumbai']['market_rate'] if region == 'Mumbai' else None,
        'fungible_fsi': REGION_CONFIG[region]["premium_rates"]["fungible_fsi"] if REGION_CONFIG[region]["has_fungible"] else 0.0,
        'ancillary_fsi': 0.0,
        'construction_cost': REGION_CONFIG[region]["premium_rates"]["construction"],
        'market_rate': 17500.0,
        'avg_flat_size': 750.0,
        'rent': 15000.0,
        'rent_months': 36,
        'relocation': 20000.0,
        'bank_interest': 50000000.0
    }
    return params
