# File: calculator.py
# Contains the main calculation function

from config import REGION_CONFIG, TDR_CONFIG
from utils import get_ready_reckoner_rate, get_fsi_based_on_road_width

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
    
    # Calculate per-member profit
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
