# File: ui_components.py
# Contains UI components for displaying results

import streamlit as st
import matplotlib.pyplot as plt
from utils import format_currency, format_area

# Basic project info
def display_basic_results(results):
    st.subheader("PROJECT BASICS")
    st.markdown(f"""
    - **Region**: {results['region']}
    - **Project Type**: {results['project_type']}
    - **Redevelopment Type**: {'Self-Redevelopment' if results['is_self_redevelopment'] else 'Builder Redevelopment'}
    """)

# Land and area details
def display_land_details(results, region, REGION_CONFIG):
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
    
    # Format TDR percentage properly
    tdr_percentage = results['tdr_percentage']
    tdr_bonus = results['effective_fsi'] - results['base_fsi']
    
    st.markdown(f"""
    {land_area_text}
    {road_width_text}
    - **Base FSI**: {results['base_fsi']}
    - **TDR Percentage**: {tdr_percentage:.1f}%
    - **TDR Bonus to FSI**: {tdr_bonus:.2f}
    - **Effective FSI with TDR**: {results['effective_fsi']:.2f}
    """)
    
    if REGION_CONFIG[region]["has_fungible"]:
        fungible_percentage = results['fungible_fsi'] * 100
        st.markdown(f"""
        - **Fungible FSI**: {fungible_percentage:.1f}%
        - **Fungible FSI Area Factor**: {results['fungible_area_factor']:.2f}
        """)
    else:
        ancillary_percentage = results['ancillary_fsi'] * 100
        st.markdown(f"""
        - **Ancillary FSI**: {ancillary_percentage:.1f}%
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
def display_premium_calculation(results, region, REGION_CONFIG):
    st.subheader("PREMIUM & TDR CALCULATION")
    
    st.markdown(f"""
    - **Ready Reckoner Rate**: {format_currency(results['ready_reckoner_rate'])}/sqm
    - **Land Area**: {format_area(results['land_area_sqm'], 'sqm')}
    """)
    
    if REGION_CONFIG[region]["has_fungible"]:
        fungible_percentage = results['fungible_fsi'] * 100
        premium_text = f"""
        - **Fungible FSI Factor**: {results['fungible_fsi']:.2f} ({fungible_percentage:.1f}%)
        - **Premium Cost Formula**: Land Area × Ready Reckoner Rate × Fungible FSI Factor
        - **Premium Cost Calculation**: {format_area(results['land_area_sqm'], 'sqm')} × {format_currency(results['ready_reckoner_rate'])}/sqm × {results['fungible_fsi']:.2f}
        - **Total Premium Cost**: {format_currency(results['premium_cost'])}"""
    else:
        ancillary_percentage = results['ancillary_fsi'] * 100
        premium_text = f"""
        - **Ancillary FSI Factor**: {results['ancillary_fsi']:.2f} ({ancillary_percentage:.1f}%)
        - **Ancillary Cost Formula**: Land Area × Ready Reckoner Rate × Ancillary FSI × Cost Factor
        - **Ancillary Cost Factor**: {REGION_CONFIG[region]["fsi_rules"]["ancillary_cost"]:.2f} (of Ready Reckoner)
        - **Total Ancillary Cost**: {format_currency(results['premium_cost'])}"""
    
    st.markdown(premium_text)

# TDR analysis
def display_tdr_analysis(results, region, project_type, TDR_CONFIG, REGION_CONFIG):
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

# Cost analysis
def display_cost_analysis(results):
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
def display_revenue(results, is_profitable):
    profit_loss_word = "PROFIT" if is_profitable else "LOSS"
    
    st.subheader(f"REVENUE & {profit_loss_word}")
    st.markdown(f"""
    - **Market Rate**: {format_currency(results['market_rate_per_sqft'])}/sqft
    - **Project Value**: {format_currency(results['project_value'])}
    - **TOTAL {profit_loss_word}**: {format_currency(abs(results['total_profit']))}
    """)

# Profit/Loss distribution
def display_profit_distribution(results, is_profitable):
    profit_loss_word = "PROFIT" if is_profitable else "LOSS"
    
    st.subheader(f"{profit_loss_word} DISTRIBUTION")
    
    if results['is_self_redevelopment']:
        society_status = "Profit" if results['society_profit'] >= 0 else "Loss"
        member_status = "Profit" if results['per_member_profit'] >= 0 else "Loss"
        
        st.markdown(f"""
        - **Society's {society_status}**: {format_currency(abs(results['society_profit']))}
        - **{member_status} per Member**: {format_currency(abs(results['per_member_profit']))}
        """)
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

# Visualization components
def display_visualization(results, region, is_profitable, REGION_CONFIG):
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
        st.pyplot(fig2)
        
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

# Create the downloadable report text
def create_download_report(results, region, is_profitable, REGION_CONFIG):
    profit_loss_word = "PROFIT" if is_profitable else "LOSS"
    tdr_percentage = results['tdr_percentage']
    tdr_bonus = results['effective_fsi'] - results['base_fsi']
    
    # Handle fungible/ancillary FSI
    if REGION_CONFIG[region]['has_fungible']:
        fsi_type = "Fungible FSI"
        fsi_value = results['fungible_fsi'] * 100
        fsi_factor = results['fungible_area_factor']
    else:
        fsi_type = "Ancillary FSI"
        fsi_value = results['ancillary_fsi'] * 100
        fsi_factor = results['ancillary_area_factor']
    
    # Road width text (only for Mumbai)
    road_width_text = ""
    if region == "Mumbai" and results['road_width'] is not None:
        road_width_text = f"Road Width: {results['road_width']} meters"
    
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
{road_width_text}
Base FSI: {results['base_fsi']}
TDR Percentage: {tdr_percentage:.1f}%
TDR Bonus to FSI: {tdr_bonus:.2f}
Effective FSI with TDR: {results['effective_fsi']:.2f}

{fsi_type}: {fsi_value:.1f}%
{fsi_type} Area Factor: {fsi_factor:.2f}
Total Effective FSI: {results['total_effective_fsi']:.2f}

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
{fsi_type} Factor: {results['fungible_fsi'] if REGION_CONFIG[region]['has_fungible'] else results['ancillary_fsi']:.2f}
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

REVENUE & {profit_loss_word}:
--------------
Market Rate: {format_currency(results['market_rate_per_sqft'])}/sqft
Project Value: {format_currency(results['project_value'])}
TOTAL {profit_loss_word}: {format_currency(abs(results['total_profit']))}

{profit_loss_word} DISTRIBUTION:
-----------------"""
    
    # Add profit/loss distribution details
    if results['is_self_redevelopment']:
        society_status = "Profit" if results['society_profit'] >= 0 else "Loss"
        member_status = "Profit" if results['per_member_profit'] >= 0 else "Loss"
        report_text += f"""
Society's {society_status}: {format_currency(abs(results['society_profit']))}
{member_status} per Member: {format_currency(abs(results['per_member_profit']))}"""
    else:
        developer_status = "Profit" if results['developer_profit'] >= 0 else "Loss"
        society_status = "Profit" if results['society_profit'] >= 0 else "Loss"
        member_status = "Profit" if results['per_member_profit'] >= 0 else "Loss"
        report_text += f"""
Developer's {developer_status} (100%): {format_currency(abs(results['developer_profit']))}
Society's {society_status} (0%): {format_currency(abs(results['society_profit']))}
{member_status} per Member: {format_currency(abs(results['per_member_profit']))}"""

    # Add salable flats information
    report_text += f"""

SALABLE FLATS:
-----------
Number of Potential Salable Flats: {results['num_salable_flats']:.1f}
    """
    
    return report_text
