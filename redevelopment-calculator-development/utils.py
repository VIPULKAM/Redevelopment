# File: utils.py
# Contains utility functions for the application

import streamlit as st
from config import ROAD_WIDTH_FSI_RULES, REGION_CONFIG, READY_RECKONER_RATES

def get_ready_reckoner_rate(region, year):
    """Get ready reckoner rate for region and year."""
    return READY_RECKONER_RATES.get(region, {}).get(year, 0)

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