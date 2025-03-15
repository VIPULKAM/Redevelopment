#!/usr/bin/env python3

def calculate_profit(
    land_area_guntha=10,
    current_carpet_area_per_member=500,
    total_members=40,
    extra_carpet_percentage=30,
    fsi=2.5,
    rent_per_month=15000,
    rent_duration_months=36,
    relocation_cost_per_member=20000,
    construction_cost_per_sqft=3000,
    tmc_premium=50000000,
    bank_interest=50000000,
    market_rate_per_sqft=17500,
    is_self_redevelopment=True
):
    # Step 1: Calculate basic areas
    GUNTHA_TO_SQM = 101.17
    SQM_TO_SQFT = 10.764
    
    land_area_sqm = land_area_guntha * GUNTHA_TO_SQM
    total_current_carpet_area = current_carpet_area_per_member * total_members
    total_offered_carpet_area = total_current_carpet_area * (1 + extra_carpet_percentage / 100)
    
    # Step 2: Calculate buildable area
    buildable_area_sqm = land_area_sqm * fsi
    ancillary_area_sqm = buildable_area_sqm * 0.6  # 60% ancillary
    total_buildable_area_sqm = buildable_area_sqm + ancillary_area_sqm
    total_buildable_area_sqft = total_buildable_area_sqm * SQM_TO_SQFT
    
    # Step 3: Apply green building bonus (7%)
    green_bonus_area_sqft = total_buildable_area_sqft * 0.07
    total_area_with_green_bonus = total_buildable_area_sqft + green_bonus_area_sqft
    
    # Step 4: Apply self-redevelopment bonus if applicable (10%)
    if is_self_redevelopment:
        self_redevelopment_bonus = total_area_with_green_bonus * 0.1
        total_final_area = total_area_with_green_bonus + self_redevelopment_bonus
    else:
        self_redevelopment_bonus = 0
        total_final_area = total_area_with_green_bonus
    
    # Step 5: Calculate sellable area
    builder_sellable_area = total_area_with_green_bonus - total_offered_carpet_area
    
    # Step 6: Calculate costs
    rent_cost = rent_per_month * total_members * rent_duration_months
    relocation_cost = relocation_cost_per_member * total_members
    accommodation_cost = rent_cost + relocation_cost
    
    # Calculate construction cost
    construction_cost = total_area_with_green_bonus * construction_cost_per_sqft
    total_construction_cost = construction_cost + accommodation_cost
    
    total_cost = total_construction_cost + tmc_premium + bank_interest
    
    # Step 7: Calculate revenue and profit
    project_value = total_final_area * market_rate_per_sqft
    total_profit = project_value - total_cost
    per_member_profit = total_profit / total_members
    
    # Calculate ROI (Return on Investment)
    roi = (total_profit / total_cost) * 100
    
    # Store the calculation steps and formulas
    calculation_steps = {
        "constants": {
            "GUNTHA_TO_SQM": GUNTHA_TO_SQM,
            "SQM_TO_SQFT": SQM_TO_SQFT,
            "ANCILLARY_PERCENTAGE": 60,
            "GREEN_BUILDING_BONUS": 7,
            "SELF_REDEVELOPMENT_BONUS": 10
        },
        "formulas": {
            "land_area_sqm": f"{land_area_guntha} Guntha × {GUNTHA_TO_SQM} = {land_area_sqm:.2f} sqm",
            "total_current_carpet_area": f"{current_carpet_area_per_member} sqft × {total_members} members = {total_current_carpet_area:.2f} sqft",
            "total_offered_carpet_area": f"{total_current_carpet_area:.2f} sqft × (1 + {extra_carpet_percentage}%) = {total_offered_carpet_area:.2f} sqft",
            "buildable_area_sqm": f"{land_area_sqm:.2f} sqm × {fsi} FSI = {buildable_area_sqm:.2f} sqm",
            "ancillary_area_sqm": f"{buildable_area_sqm:.2f} sqm × 60% = {ancillary_area_sqm:.2f} sqm",
            "total_buildable_area_sqm": f"{buildable_area_sqm:.2f} sqm + {ancillary_area_sqm:.2f} sqm = {total_buildable_area_sqm:.2f} sqm",
            "total_buildable_area_sqft": f"{total_buildable_area_sqm:.2f} sqm × {SQM_TO_SQFT} = {total_buildable_area_sqft:.2f} sqft",
            "green_bonus_area_sqft": f"{total_buildable_area_sqft:.2f} sqft × 7% = {green_bonus_area_sqft:.2f} sqft",
            "total_area_with_green_bonus": f"{total_buildable_area_sqft:.2f} sqft + {green_bonus_area_sqft:.2f} sqft = {total_area_with_green_bonus:.2f} sqft",
            "self_redevelopment_bonus": f"{total_area_with_green_bonus:.2f} sqft × 10% = {self_redevelopment_bonus:.2f} sqft" if is_self_redevelopment else "Not applicable (Builder Redevelopment)",
            "total_final_area": f"{total_area_with_green_bonus:.2f} sqft + {self_redevelopment_bonus:.2f} sqft = {total_final_area:.2f} sqft" if is_self_redevelopment else f"Same as area with green bonus: {total_final_area:.2f} sqft",
            "builder_sellable_area": f"{total_area_with_green_bonus:.2f} sqft - {total_offered_carpet_area:.2f} sqft = {builder_sellable_area:.2f} sqft",
            "rent_cost": f"₹{rent_per_month:,} × {total_members} members × {rent_duration_months} months = ₹{rent_cost:,.2f}",
            "relocation_cost": f"₹{relocation_cost_per_member:,} × {total_members} members = ₹{relocation_cost:,.2f}",
            "accommodation_cost": f"₹{rent_cost:,.2f} + ₹{relocation_cost:,.2f} = ₹{accommodation_cost:,.2f}",
            "construction_cost": f"{total_area_with_green_bonus:.2f} sqft × ₹{construction_cost_per_sqft:,}/sqft = ₹{construction_cost:,.2f}",
            "total_construction_cost": f"₹{construction_cost:,.2f} + ₹{accommodation_cost:,.2f} = ₹{total_construction_cost:,.2f}",
            "total_cost": f"₹{total_construction_cost:,.2f} + ₹{tmc_premium:,.2f} (TMC Premium) + ₹{bank_interest:,.2f} (Bank Interest) = ₹{total_cost:,.2f}",
            "project_value": f"{total_final_area:.2f} sqft × ₹{market_rate_per_sqft:,}/sqft = ₹{project_value:,.2f}",
            "total_profit": f"₹{project_value:,.2f} - ₹{total_cost:,.2f} = ₹{total_profit:,.2f}",
            "per_member_profit": f"₹{total_profit:,.2f} ÷ {total_members} members = ₹{per_member_profit:,.2f}",
            "roi": f"(₹{total_profit:,.2f} ÷ ₹{total_cost:,.2f}) × 100 = {roi:.2f}%"
        }
    }
    
    # Prepare results dictionary
    results = {
        # Area calculations
        "land_area_guntha": land_area_guntha,
        "land_area_sqm": land_area_sqm,
        "total_current_carpet_area": total_current_carpet_area,
        "total_offered_carpet_area": total_offered_carpet_area,
        "buildable_area_sqm": buildable_area_sqm,
        "ancillary_area_sqm": ancillary_area_sqm,
        "total_buildable_area_sqm": total_buildable_area_sqm,
        "total_buildable_area_sqft": total_buildable_area_sqft,
        "green_bonus_area_sqft": green_bonus_area_sqft,
        "total_area_with_green_bonus": total_area_with_green_bonus,
        "self_redevelopment_bonus": self_redevelopment_bonus,
        "total_final_area": total_final_area,
        "builder_sellable_area": builder_sellable_area,
        
        # Cost calculations
        "rent_cost": rent_cost,
        "relocation_cost": relocation_cost,
        "accommodation_cost": accommodation_cost,
        "construction_cost": construction_cost,
        "total_construction_cost": total_construction_cost,
        "tmc_premium": tmc_premium,
        "bank_interest": bank_interest,
        "total_cost": total_cost,
        
        # Revenue and profit
        "project_value": project_value,
        "total_profit": total_profit,
        "per_member_profit": per_member_profit,
        "roi": roi,
        
        # Project parameters (for reference)
        "is_self_redevelopment": is_self_redevelopment,
        
        # Input parameters
        "inputs": {
            "land_area_guntha": land_area_guntha,
            "current_carpet_area_per_member": current_carpet_area_per_member,
            "total_members": total_members,
            "extra_carpet_percentage": extra_carpet_percentage,
            "fsi": fsi,
            "rent_per_month": rent_per_month,
            "rent_duration_months": rent_duration_months,
            "relocation_cost_per_member": relocation_cost_per_member,
            "construction_cost_per_sqft": construction_cost_per_sqft,
            "tmc_premium": tmc_premium,
            "bank_interest": bank_interest,
            "market_rate_per_sqft": market_rate_per_sqft
        },
        
        # Calculation details
        "calculation_steps": calculation_steps
    }
    
    return results

def print_report(results, show_detailed_calculations=False):
    print("\nREDEVELOPMENT PROJECT ANALYSIS")
    print("=" * 60)
    
    project_type = "Self-Redevelopment" if results['is_self_redevelopment'] else "Builder Redevelopment"
    print(f"Project Type: {project_type}")
    
    print("\nINPUT PARAMETERS:")
    print("-" * 20)
    inputs = results['inputs']
    print(f"Land Area: {inputs['land_area_guntha']} Guntha")
    print(f"Total Members: {inputs['total_members']}")
    print(f"Carpet Area per Member: {inputs['current_carpet_area_per_member']} sqft")
    print(f"Extra Carpet Area: {inputs['extra_carpet_percentage']}%")
    print(f"FSI (Floor Space Index): {inputs['fsi']}")
    print(f"Construction Cost: ₹{inputs['construction_cost_per_sqft']:,}/sqft")
    print(f"Market Rate: ₹{inputs['market_rate_per_sqft']:,}/sqft")
    
    print("\nLAND & AREA CALCULATIONS:")
    print("-" * 30)
    
    steps = results['calculation_steps']['formulas']
    
    if show_detailed_calculations:
        print("Step 1: Convert land area from Guntha to square meters")
        print(f"  {steps['land_area_sqm']}")
        
        print("\nStep 2: Calculate carpet areas")
        print(f"  Current Total Carpet Area: {steps['total_current_carpet_area']}")
        print(f"  Offered Carpet Area (with {inputs['extra_carpet_percentage']}% extra): {steps['total_offered_carpet_area']}")
        
        print("\nStep 3: Calculate buildable area using FSI")
        print(f"  Basic FSI Area: {steps['buildable_area_sqm']}")
        print(f"  Ancillary Area (60% of FSI): {steps['ancillary_area_sqm']}")
        print(f"  Total Buildable Area (sqm): {steps['total_buildable_area_sqm']}")
        print(f"  Total Buildable Area (sqft): {steps['total_buildable_area_sqft']}")
        
        print("\nStep 4: Apply Green Building Bonus (7%)")
        print(f"  Green Building Bonus Area: {steps['green_bonus_area_sqft']}")
        print(f"  Area with Green Bonus: {steps['total_area_with_green_bonus']}")
        
        print("\nStep 5: Apply Self-Redevelopment Bonus (if applicable)")
        print(f"  Self-Redevelopment Bonus: {steps['self_redevelopment_bonus']}")
        print(f"  Total Final Area: {steps['total_final_area']}")
        
        print("\nStep 6: Calculate Sellable Area")
        print(f"  Builder Sellable Area: {steps['builder_sellable_area']}")
    else:
        print(f"Land Area: {results['land_area_guntha']} Guntha ({results['land_area_sqm']:.2f} sqm)")
        print(f"Current Carpet Area: {results['total_current_carpet_area']:.2f} sqft")
        print(f"Offered Carpet Area: {results['total_offered_carpet_area']:.2f} sqft")
        print(f"Total Buildable Area: {results['total_buildable_area_sqft']:.2f} sqft")
        print(f"Area with Green Bonus: {results['total_area_with_green_bonus']:.2f} sqft")
        
        if results['is_self_redevelopment']:
            print(f"Self-Redevelopment Bonus: {results['self_redevelopment_bonus']:.2f} sqft")
            
        print(f"Total Final Area: {results['total_final_area']:.2f} sqft")
        print(f"Builder Sellable Area: {results['builder_sellable_area']:.2f} sqft")
    
    print("\nCOST CALCULATIONS:")
    print("-" * 30)
    
    if show_detailed_calculations:
        print("Step 7: Calculate Accommodation Costs")
        print(f"  Rent Cost: {steps['rent_cost']}")
        print(f"  Relocation Cost: {steps['relocation_cost']}")
        print(f"  Total Accommodation Cost: {steps['accommodation_cost']}")
        
        print("\nStep 8: Calculate Construction Costs")
        print(f"  Construction Cost: {steps['construction_cost']}")
        print(f"  Total Construction Cost: {steps['total_construction_cost']}")
        
        print("\nStep 9: Calculate Total Project Cost")
        print(f"  Total Project Cost: {steps['total_cost']}")
    else:
        print(f"Rent Cost: ₹{results['rent_cost']:,.2f}")
        print(f"Relocation Cost: ₹{results['relocation_cost']:,.2f}")
        print(f"Total Accommodation Cost: ₹{results['accommodation_cost']:,.2f}")
        print(f"Construction Cost: ₹{results['construction_cost']:,.2f}")
        print(f"Total Construction Cost: ₹{results['total_construction_cost']:,.2f}")
        print(f"TMC Premium: ₹{results['tmc_premium']:,.2f}")
        print(f"Bank Interest: ₹{results['bank_interest']:,.2f}")
        print(f"TOTAL PROJECT COST: ₹{results['total_cost']:,.2f}")
    
    print("\nREVENUE & PROFIT CALCULATIONS:")
    print("-" * 30)
    
    if show_detailed_calculations:
        print("Step 10: Calculate Project Value")
        print(f"  Project Value: {steps['project_value']}")
        
        print("\nStep 11: Calculate Profit")
        print(f"  Total Profit: {steps['total_profit']}")
        print(f"  Profit per Member: {steps['per_member_profit']}")
        
        print("\nStep 12: Calculate ROI")
        print(f"  Return on Investment: {steps['roi']}")
    else:
        print(f"Project Value: ₹{results['project_value']:,.2f}")
        print(f"TOTAL PROFIT: ₹{results['total_profit']:,.2f}")
        print(f"Profit per Member: ₹{results['per_member_profit']:,.2f}")
        print(f"Return on Investment (ROI): {results['roi']:.2f}%")
    
    # Calculate in crores
    profit_cr = results['total_profit'] / 10000000
    per_member_cr = results['per_member_profit'] / 10000000
    print(f"\nTotal Profit: ₹{profit_cr:.2f} Cr")
    print(f"Profit per Member: ₹{per_member_cr:.2f} Cr")

def get_input_with_default(prompt, default, convert_func=float):
    """Get user input with a default value."""
    user_input = input(f"{prompt} [{default}]: ")
    if user_input.strip() == "":
        return default
    try:
        return convert_func(user_input)
    except ValueError:
        print(f"Invalid input. Using default value: {default}")
        return default

def main():
    print("REDEVELOPMENT PROFIT CALCULATOR")
    print("=" * 30)
    
    choice = input("Use (D)efault values or (C)ustom inputs? [D]: ").strip().upper()
    
    if choice == "C":
        print("\nEnter project parameters:")
        print("-" * 25)
        
        # Get area inputs
        land_area = get_input_with_default("Enter land area in Guntha", 10)
        members = get_input_with_default("Enter number of members/flats", 40, int)
        carpet_area = get_input_with_default("Enter current carpet area per member in sqft", 500)
        extra_percentage = get_input_with_default("Enter extra carpet percentage offered", 30)
        fsi = get_input_with_default("Enter FSI value", 2.5)
        
        # Get cost inputs
        rent = get_input_with_default("Enter monthly rent per flat in Rs.", 15000)
        rent_months = get_input_with_default("Enter rent duration in months", 36, int)
        relocation = get_input_with_default("Enter relocation cost per member in Rs.", 20000)
        construction_cost = get_input_with_default("Enter construction cost per sqft in Rs.", 3000)
        
        # Get additional costs
        tmc_premium = get_input_with_default("Enter TMC premium in Rs.", 50000000)
        bank_interest = get_input_with_default("Enter estimated bank interest in Rs.", 50000000)
        
        # Get market rate
        market_rate = get_input_with_default("Enter market rate per sqft in Rs.", 17500)
        
        # Project type
        is_self_input = input("Is this a self-redevelopment project? (y/n) [y]: ").strip().lower()
        is_self = is_self_input != "n"
        
        # Calculate with user inputs
        print("\nCalculating with custom parameters...")
        results = calculate_profit(
            land_area_guntha=land_area,
            current_carpet_area_per_member=carpet_area,
            total_members=members,
            extra_carpet_percentage=extra_percentage,
            fsi=fsi,
            rent_per_month=rent,
            rent_duration_months=rent_months,
            relocation_cost_per_member=relocation,
            construction_cost_per_sqft=construction_cost,
            tmc_premium=tmc_premium,
            bank_interest=bank_interest,
            market_rate_per_sqft=market_rate,
            is_self_redevelopment=is_self
        )
    else:
        print("\nCalculating with default parameters...")
        results = calculate_profit()
    
    # Ask if user wants detailed calculations
    detailed = input("\nShow detailed step-by-step calculations? (y/n) [y]: ").strip().lower()
    show_detailed = detailed != "n"
    
    # Print the results
    print_report(results, show_detailed)
    
    print("\nSUMMARY:")
    print("-" * 15)
    project_type = "Self-Redevelopment" if results['is_self_redevelopment'] else "Builder Redevelopment"
    print(f"Project Type: {project_type}")
    print(f"Total Profit: ₹{results['total_profit']/10000000:.2f} Cr")
    print(f"Profit per Member: ₹{results['per_member_profit']/10000000:.2f} Cr")
    print(f"ROI: {results['roi']:.2f}%")
    print("=" * 30)
    
    # Ask if user wants to save report to a file
    save_option = input("\nSave this report to a file? (y/n): ").strip().lower()
    if save_option == "y":
        filename = input("Enter filename [redevelopment_report.txt]: ").strip() or "redevelopment_report.txt"
        try:
            with open(filename, 'w') as f:
                # Save to file
                import sys
                original_stdout = sys.stdout
                sys.stdout = f
                
                print("REDEVELOPMENT PROFIT CALCULATOR - DETAILED REPORT")
                print("=" * 50)
                print(f"Date: {import_module('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print_report(results, True)  # Always show detailed calculations in file
                
                print("\nSUMMARY:")
                print("-" * 15)
                print(f"Project Type: {project_type}")
                print(f"Total Profit: ₹{results['total_profit']/10000000:.2f} Cr")
                print(f"Profit per Member: ₹{results['per_member_profit']/10000000:.2f} Cr")
                print(f"ROI: {results['roi']:.2f}%")
                
                # Reset stdout
                sys.stdout = original_stdout
                
            print(f"Report saved to {filename}")
        except Exception as e:
            print(f"Error saving report: {e}")

# Import modules only when needed
def import_module(name):
    """Import a module dynamically."""
    return __import__(name)

# Call the main function
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
