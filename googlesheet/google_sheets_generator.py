#!/usr/bin/env python3
"""
Google Sheets Generator for Redevelopment Profit Calculator

This script creates a Google Sheets document with all the formulas and calculations
for the redevelopment profit calculator.

Prerequisites:
1. Install required packages:
   pip install gspread oauth2client

2. Set up Google Sheets API:
   - Go to Google Cloud Console (https://console.cloud.google.com/)
   - Create a new project
   - Enable the Google Sheets API
   - Create credentials (Service Account Key)
   - Download the JSON credentials file
   - Share your target Google Sheet with the email in the credentials file
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

def create_redevelopment_google_sheet(creds_file, sheet_title="Redevelopment Profit Calculator"):
    """Create a Google Sheet with redevelopment profit calculations."""
    
    # Define scope and authenticate
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    
    credentials = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)
    client = gspread.authorize(credentials)
    
    # Create a new Google Sheet
    print(f"Creating new Google Sheet: {sheet_title}")
    workbook = client.create(sheet_title)
    
    # Share the document with the user (optional)
    # workbook.share('your-email@example.com', perm_type='user', role='writer')
    
    print(f"Google Sheet created: {workbook.url}")
    
    # Get the default sheet and rename it
    worksheet = workbook.get_worksheet(0)
    worksheet.update_title("Inputs")
    
    # Create the additional sheets
    area_sheet = workbook.add_worksheet(title="Area Calculations", rows=50, cols=20)
    cost_sheet = workbook.add_worksheet(title="Cost Calculations", rows=50, cols=20)
    profit_sheet = workbook.add_worksheet(title="Profit & Surplus", rows=50, cols=20)
    summary_sheet = workbook.add_worksheet(title="Summary Dashboard", rows=50, cols=20)
    docs_sheet = workbook.add_worksheet(title="Documentation", rows=100, cols=20)
    
    # Get all worksheets for easier reference
    inputs_sheet = workbook.worksheet("Inputs")
    
    # -------------------------------------------------------------
    # INPUTS SHEET
    # -------------------------------------------------------------
    print("Configuring Inputs sheet...")
    
    # Add title
    inputs_sheet.merge_cells('A1:D1')
    inputs_sheet.update('A1', "REDEVELOPMENT PROFIT CALCULATOR - INPUTS")
    inputs_sheet.format('A1', {
        "textFormat": {"bold": True, "fontSize": 14},
        "horizontalAlignment": "CENTER"
    })
    
    # Column headers
    headers = ['Parameter', 'Value', 'Unit', 'Description']
    inputs_sheet.update('A3:D3', [headers])
    inputs_sheet.format('A3:D3', {
        "backgroundColor": {"red": 0.2, "green": 0.4, "blue": 0.6},
        "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}},
        "horizontalAlignment": "CENTER"
    })
    
    # Input parameters with sections
    parameters = [
        # Land & Member Parameters
        ["Land & Member Parameters", "", "", ""],
        ["Land Area", 10, "Guntha", "Total land area of the society"],
        ["Total Members", 40, "flats", "Number of existing flats/members"],
        ["Carpet Area per Member", 500, "sqft", "Current carpet area per flat"],
        ["Extra Carpet Percentage", 30, "%", "Additional area to be offered"],
        
        # Development Parameters
        ["Development Parameters", "", "", ""],
        ["FSI", 2.5, "", "Floor Space Index (Chatai Kshetra Nirdeshank)"],
        ["Ancillary Percentage", 60, "%", "Percentage of ancillary area allowed on top of FSI"],
        ["Green Building Bonus", 7, "%", "Percentage of additional FSI for green building"],
        ["Self-Redevelopment Bonus", 10, "%", "Percentage of additional FSI for self-redevelopment"],
        
        # Cost Parameters
        ["Cost Parameters", "", "", ""],
        ["Monthly Rent per Flat", 15000, "₹", "Monthly rent paid during construction"],
        ["Rent Duration", 36, "months", "Duration of rent payment"],
        ["Relocation Cost per Member", 20000, "₹", "Relocation and brokerage cost per member"],
        ["Construction Cost", 3000, "₹/sqft", "Construction cost per square foot"],
        ["TMC Premium", 50000000, "₹", "Premium to be paid to municipal corporation"],
        ["Bank Interest", 50000000, "₹", "Bank interest amount"],
        
        # Revenue Parameters
        ["Revenue Parameters", "", "", ""],
        ["Market Rate", 17500, "₹/sqft", "Market rate per square foot for selling"],
        ["Average New Flat Size", 750, "sqft", "Average size of new salable flats"],
        
        # Project Type
        ["Project Type", "", "", ""],
        ["Is Self-Redevelopment", "Yes", "", "Self-redevelopment or builder project"],
        ["Profit Sharing with Developer", 50, "%", "Only applicable if not self-redevelopment"]
    ]
    
    # Update the cells with the parameter data
    inputs_sheet.update('A4', parameters)
    
    # Format section headers
    section_rows = [4, 9, 14, 21, 24]
    for row in section_rows:
        inputs_sheet.merge_cells(f'A{row}:D{row}')
        inputs_sheet.format(f'A{row}:D{row}', {
            "backgroundColor": {"red": 0.85, "green": 0.9, "blue": 0.95},
            "textFormat": {"bold": True},
            "horizontalAlignment": "LEFT"
        })
    
    # Format input value cells
    input_rows = list(range(5, 30))
    for row in input_rows:
        if row not in section_rows:
            inputs_sheet.format(f'B{row}', {
                "backgroundColor": {"red": 1, "green": 0.95, "blue": 0.8},
                "horizontalAlignment": "RIGHT",
                "numberFormat": {"type": "NUMBER"}
            })
    
    # Set data validation for Yes/No field
    inputs_sheet.data_validation('B29', {
        "condition": {"type": "ONE_OF_LIST", "values": ["Yes", "No"]},
        "showCustomUi": True
    })
    
    # Name the ranges in Google Sheets
    # Note: Google Sheets uses named ranges differently
    # We'll use proper cell references in formulas instead
    
    # Set column widths
    inputs_sheet.column_dimensions('A', 250)  # Parameter
    inputs_sheet.column_dimensions('B', 120)  # Value
    inputs_sheet.column_dimensions('C', 80)   # Unit
    inputs_sheet.column_dimensions('D', 350)  # Description
    
    # -------------------------------------------------------------
    # AREA CALCULATIONS SHEET
    # -------------------------------------------------------------
    print("Configuring Area Calculations sheet...")
    
    # Add title
    area_sheet.merge_cells('A1:E1')
    area_sheet.update('A1', "AREA CALCULATIONS")
    area_sheet.format('A1', {
        "textFormat": {"bold": True, "fontSize": 14},
        "horizontalAlignment": "CENTER"
    })
    
    # Column headers
    area_headers = ['Step', 'Calculation', 'Formula', 'Value', 'Unit']
    area_sheet.update('A3:E3', [area_headers])
    area_sheet.format('A3:E3', {
        "backgroundColor": {"red": 0.2, "green": 0.4, "blue": 0.6},
        "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}},
        "horizontalAlignment": "CENTER"
    })
    
    # Area calculation steps with formulas
    # Note: Google Sheets formulas reference sheets differently
    area_calculations = [
        # Basic Land Area
        ["1", "Land Area in Square Meters", "=Inputs!B5*101.17", "", "sqm"],
        
        # Carpet Areas
        ["2", "Current Total Carpet Area", "=Inputs!B7*Inputs!B6", "", "sqft"],
        ["2", "Offered Carpet Area (with extra)", "=C5*(1+Inputs!B8/100)", "", "sqft"],
        
        # FSI Area
        ["3", "Basic FSI Area", "=C4*Inputs!B11", "", "sqm"],
        ["3", "Ancillary Area", "=C7*(Inputs!B12/100)", "", "sqm"],
        ["3", "Total Buildable Area (sqm)", "=C7+C8", "", "sqm"],
        ["3", "Total Buildable Area (sqft)", "=C9*10.764", "", "sqft"],
        
        # Green Building Bonus
        ["4", "Green Building Bonus Area", "=C10*(Inputs!B13/100)", "", "sqft"],
        ["4", "Area with Green Bonus", "=C10+C11", "", "sqft"],
        
        # Self-Redevelopment Bonus
        ["5", "Self-Redevelopment Bonus", "=IF(Inputs!B29=\"Yes\",C12*(Inputs!B14/100),0)", "", "sqft"],
        ["5", "Total Final Area", "=C12+C13", "", "sqft"],
        
        # Sellable Area
        ["6", "Builder Sellable Area", "=C12-C6", "", "sqft"]
    ]
    
    # Update cells with area calculations
    area_sheet.update('A4', area_calculations)
    
    # Format the formula and result columns
    for row in range(4, 4 + len(area_calculations)):
        # Format formula column
        area_sheet.format(f'C{row}', {
            "backgroundColor": {"red": 0.9, "green": 0.95, "blue": 0.9}
        })
        
        # Format value column (result)
        area_sheet.update(f'D{row}', f'=ROUND({area_calculations[row-4][2]},2)')
        area_sheet.format(f'D{row}', {
            "backgroundColor": {"red": 0.85, "green": 0.9, "blue": 0.95},
            "numberFormat": {"type": "NUMBER", "pattern": "#,##0.00"}
        })
    
    # Set column widths
    area_sheet.column_dimensions('A', 50)    # Step
    area_sheet.column_dimensions('B', 250)   # Calculation
    area_sheet.column_dimensions('C', 300)   # Formula
    area_sheet.column_dimensions('D', 120)   # Value
    area_sheet.column_dimensions('E', 80)    # Unit
    
    # Add a chart
    # Note: In Google Sheets API, we'd need to use the Charts API for this
    # This is more complex and would require additional code
    
    # -------------------------------------------------------------
    # COST CALCULATIONS SHEET
    # -------------------------------------------------------------
    print("Configuring Cost Calculations sheet...")
    
    # Add title
    cost_sheet.merge_cells('A1:E1')
    cost_sheet.update('A1', "COST CALCULATIONS")
    cost_sheet.format('A1', {
        "textFormat": {"bold": True, "fontSize": 14},
        "horizontalAlignment": "CENTER"
    })
    
    # Column headers
    cost_headers = ['Step', 'Calculation', 'Formula', 'Value', 'Unit']
    cost_sheet.update('A3:E3', [cost_headers])
    cost_sheet.format('A3:E3', {
        "backgroundColor": {"red": 0.2, "green": 0.4, "blue": 0.6},
        "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}},
        "horizontalAlignment": "CENTER"
    })
    
    # Cost calculation steps
    cost_calculations = [
        # Accommodation Costs
        ["7", "Rent Cost", "=Inputs!B17*Inputs!B6*Inputs!B18", "", "₹"],
        ["7", "Relocation Cost", "=Inputs!B19*Inputs!B6", "", "₹"],
        ["7", "Total Accommodation Cost", "=C4+C5", "", "₹"],
        
        # Construction Costs
        ["8", "Construction Cost", "='Area Calculations'!D12*Inputs!B20", "", "₹"],
        ["8", "Total Construction Cost", "=C7+C6", "", "₹"],
        
        # Total Project Cost
        ["9", "TMC Premium", "=Inputs!B21", "", "₹"],
        ["9", "Bank Interest", "=Inputs!B22", "", "₹"],
        ["9", "Total Project Cost", "=C8+C9+C10", "", "₹"]
    ]
    
    # Update cells with cost calculations
    cost_sheet.update('A4', cost_calculations)
    
    # Format the formula and result columns
    for row in range(4, 4 + len(cost_calculations)):
        # Format formula column
        cost_sheet.format(f'C{row}', {
            "backgroundColor": {"red": 0.9, "green": 0.95, "blue": 0.9}
        })
        
        # Format value column (result)
        cost_sheet.update(f'D{row}', f'=ROUND({cost_calculations[row-4][2]},2)')
        cost_sheet.format(f'D{row}', {
            "backgroundColor": {"red": 0.85, "green": 0.9, "blue": 0.95},
            "numberFormat": {"type": "NUMBER", "pattern": "#,##0"}
        })
    
    # Set column widths
    cost_sheet.column_dimensions('A', 50)    # Step
    cost_sheet.column_dimensions('B', 250)   # Calculation
    cost_sheet.column_dimensions('C', 300)   # Formula
    cost_sheet.column_dimensions('D', 120)   # Value
    cost_sheet.column_dimensions('E', 80)    # Unit
    
    # -------------------------------------------------------------
    # PROFIT & SURPLUS SHEET
    # -------------------------------------------------------------
    print("Configuring Profit & Surplus sheet...")
    
    # Add title
    profit_sheet.merge_cells('A1:E1')
    profit_sheet.update('A1', "PROFIT & SURPLUS CALCULATIONS")
    profit_sheet.format('A1', {
        "textFormat": {"bold": True, "fontSize": 14},
        "horizontalAlignment": "CENTER"
    })
    
    # Column headers
    profit_headers = ['Step', 'Calculation', 'Formula', 'Value', 'Unit']
    profit_sheet.update('A3:E3', [profit_headers])
    profit_sheet.format('A3:E3', {
        "backgroundColor": {"red": 0.2, "green": 0.4, "blue": 0.6},
        "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}},
        "horizontalAlignment": "CENTER"
    })
    
    # Profit & Surplus calculation steps
    profit_calculations = [
        # Project Value
        ["10", "Project Value", "='Area Calculations'!D14*Inputs!B25", "", "₹"],
        
        # Profit
        ["11", "Total Profit", "=C4-'Cost Calculations'!D11", "", "₹"],
        
        # Salable Flats
        ["12", "Number of Salable Flats", "='Area Calculations'!D15/Inputs!B26", "", "flats"],
        
        # Profit Distribution
        ["13", "Developer's Profit", "=IF(Inputs!B29=\"No\",C5*(Inputs!B30/100),0)", "", "₹"],
        ["13", "Society's Profit", "=C5-C8", "", "₹"],
        
        # Per Member Profit
        ["14", "Profit per Member", "=C9/Inputs!B6", "", "₹"],
        
        # Surplus Corpus
        ["15", "Surplus Corpus for Existing Members", "=C9", "", "₹"],
        
        # ROI
        ["16", "Return on Investment (ROI)", "=(C5/'Cost Calculations'!D11)*100", "", "%"]
    ]
    
    # Update cells with profit calculations
    profit_sheet.update('A4', profit_calculations)
    
    # Format the formula and result columns
    for row in range(4, 4 + len(profit_calculations)):
        # Format formula column
        profit_sheet.format(f'C{row}', {
            "backgroundColor": {"red": 0.9, "green": 0.95, "blue": 0.9}
        })
        
        # Format value column (result)
        profit_sheet.update(f'D{row}', f'=ROUND({profit_calculations[row-4][2]},2)')
        
        # Apply number formatting based on the unit
        if profit_calculations[row-4][4] == "%":
            profit_sheet.format(f'D{row}', {
                "backgroundColor": {"red": 0.85, "green": 0.9, "blue": 0.95},
                "numberFormat": {"type": "NUMBER", "pattern": "0.00%"}
            })
        elif profit_calculations[row-4][4] == "flats":
            profit_sheet.format(f'D{row}', {
                "backgroundColor": {"red": 0.85, "green": 0.9, "blue": 0.95},
                "numberFormat": {"type": "NUMBER", "pattern": "0.00"}
            })
        else:
            profit_sheet.format(f'D{row}', {
                "backgroundColor": {"red": 0.85, "green": 0.9, "blue": 0.95},
                "numberFormat": {"type": "NUMBER", "pattern": "#,##0"}
            })
    
    # Add Crore Conversion Section
    profit_sheet.update('A13', "Conversion to Crores")
    profit_sheet.merge_cells('A13:E13')
    profit_sheet.format('A13', {
        "backgroundColor": {"red": 0.85, "green": 0.9, "blue": 0.95},
        "textFormat": {"bold": True},
        "horizontalAlignment": "LEFT"
    })
    
    crore_conversions = [
        ["", "Total Profit in Crores", "=C5/10000000", "", "Cr"],
        ["", "Society's Profit in Crores", "=C9/10000000", "", "Cr"],
        ["", "Profit per Member in Crores", "=C10/10000000", "", "Cr"]
    ]
    
    # Update cells with crore conversions
    profit_sheet.update('A14', crore_conversions)
    
    # Format the formula and result columns for crore conversions
    for row in range(14, 14 + len(crore_conversions)):
        profit_sheet.format(f'C{row}', {
            "backgroundColor": {"red": 0.9, "green": 0.95, "blue": 0.9}
        })
        
        profit_sheet.update(f'D{row}', f'=ROUND({crore_conversions[row-14][2]},2)')
        profit_sheet.format(f'D{row}', {
            "backgroundColor": {"red": 0.85, "green": 0.9, "blue": 0.95},
            "numberFormat": {"type": "NUMBER", "pattern": "#,##0.00"}
        })
    
    # Set column widths
    profit_sheet.column_dimensions('A', 50)    # Step
    profit_sheet.column_dimensions('B', 250)   # Calculation
    profit_sheet.column_dimensions('C', 300)   # Formula
    profit_sheet.column_dimensions('D', 120)   # Value
    profit_sheet.column_dimensions('E', 80)    # Unit
    
    # -------------------------------------------------------------
    # SUMMARY DASHBOARD SHEET
    # -------------------------------------------------------------
    print("Configuring Summary Dashboard sheet...")
    
    # Add title
    summary_sheet.merge_cells('A1:D1')
    summary_sheet.update('A1', "REDEVELOPMENT PROFIT SUMMARY")
    summary_sheet.format('A1', {
        "textFormat": {"bold": True, "fontSize": 14},
        "horizontalAlignment": "CENTER"
    })
    
    # Project Type Section
    summary_sheet.update('A3', "PROJECT TYPE:")
    summary_sheet.format('A3', {
        "textFormat": {"bold": True}
    })
    
    summary_sheet.update('B3', "=IF(Inputs!B29=\"Yes\",\"Self-Redevelopment\",\"Builder Redevelopment\")")
    summary_sheet.format('B3', {
        "textFormat": {"bold": True, "foregroundColor": {"red": 0, "green": 0, "blue": 1}}
    })
    
    # Key Metrics Section
    summary_sheet.update('A5', "KEY METRICS")
    summary_sheet.merge_cells('A5:D5')
    summary_sheet.format('A5', {
        "backgroundColor": {"red": 0.85, "green": 0.9, "blue": 0.95},
        "textFormat": {"bold": True},
        "horizontalAlignment": "LEFT"
    })
    
    metrics = [
        ["Land Area", "=Inputs!B5", "Guntha"],
        ["Total Members", "=Inputs!B6", "flats"],
        ["Total Final Area", "='Area Calculations'!D14", "sqft"],
        ["Builder Sellable Area", "='Area Calculations'!D15", "sqft"],
        ["Total Project Cost", "='Cost Calculations'!D11", "₹"],
        ["Project Value", "='Profit & Surplus'!D4", "₹"],
        ["Total Profit", "='Profit & Surplus'!D5", "₹"],
        ["Number of Salable Flats", "=ROUND('Profit & Surplus'!D7,0)", "flats"],
        ["Return on Investment (ROI)", "='Profit & Surplus'!D12", "%"]
    ]
    
    # Update cells with metrics
    cell_data = []
    for metric in metrics:
        cell_data.append([metric[0], metric[1], metric[2]])
    
    summary_sheet.update('A6', cell_data)
    
    # Format the metrics
    for row in range(6, 6 + len(metrics)):
        # Format value column
        summary_sheet.format(f'B{row}', {
            "horizontalAlignment": "RIGHT",
            "numberFormat": {"type": "NUMBER", "pattern": "#,##0.00"}
        })
    
    # Member Benefits Section
    summary_sheet.update('A16', "MEMBER BENEFITS")
    summary_sheet.merge_cells('A16:D16')
    summary_sheet.format('A16', {
        "backgroundColor": {"red": 0.85, "green": 0.9, "blue": 0.95},
        "textFormat": {"bold": True},
        "horizontalAlignment": "LEFT"
    })
    
    benefits = [
        ["Current Carpet Area", "=Inputs!B7", "sqft/member"],
        ["Offered Carpet Area", "='Area Calculations'!D6/Inputs!B6", "sqft/member"],
        ["Area Increase", "=('Area Calculations'!D6-'Area Calculations'!D5)/Inputs!B6", "sqft/member"],
        ["Area Increase Percentage", "=('Area Calculations'!D6/'Area Calculations'!D5-1)*100", "%"],
        ["Surplus per Member", "='Profit & Surplus'!D10", "₹"],
        ["Surplus per Member (Crores)", "='Profit & Surplus'!D16", "Cr"]
    ]
    
    # Update cells with benefits
    cell_data = []
    for benefit in benefits:
        cell_data.append([benefit[0], benefit[1], benefit[2]])
    
    summary_sheet.update('A17', cell_data)
    
    # Format the benefits
    for row in range(17, 17 + len(benefits)):
        # Format value column
        if benefits[row-17][2] == "%":
            summary_sheet.format(f'B{row}', {
                "horizontalAlignment": "RIGHT",
                "numberFormat": {"type": "PERCENT", "pattern": "0.00%"}
            })
        else:
            summary_sheet.format(f'B{row}', {
                "horizontalAlignment": "RIGHT",
                "numberFormat": {"type": "NUMBER", "pattern": "#,##0.00"}
            })
    
    # Add notice about builder profit
    summary_sheet.update('A24', "=IF(Inputs!B29=\"No\",\"Builder's Profit per Flat: \" & TEXT('Profit & Surplus'!D8/Inputs!B6/10000000,\"0.00\") & \" Cr\",\"\")")
    summary_sheet.merge_cells('A24:D24')
    summary_sheet.format('A24', {
        "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 0, "blue": 0}}
    })
    
    # Add warning about self-redevelopment
    summary_sheet.update('A26', "NOTE: Self-redevelopment can yield significantly higher returns but requires professional management and commitment from society members.")
    summary_sheet.merge_cells('A26:D26')
    summary_sheet.format('A26', {
        "textFormat": {"italic": True}
    })
    
    # Set column widths
    summary_sheet.column_dimensions('A', 250)   # Parameter
    summary_sheet.column_dimensions('B', 150)   # Value
    summary_sheet.column_dimensions('C', 100)   # Unit
    summary_sheet.column_dimensions('D', 250)   # Extra space
    
    # -------------------------------------------------------------
    # DOCUMENTATION SHEET
    # -------------------------------------------------------------
    print("Configuring Documentation sheet...")
    
    # Add title
    docs_sheet.merge_cells('A1:C1')
    docs_sheet.update('A1', "DOCUMENTATION & HELP")
    docs_sheet.format('A1', {
        "textFormat": {"bold": True, "fontSize": 14},
        "horizontalAlignment": "CENTER"
    })
    
    # Add sections
    docs_data = [
        ["OVERVIEW", "", ""],
        ["This spreadsheet calculates the financial aspects of a housing society redevelopment project. It shows the profit potential, distribution of benefits, and number of salable flats that can be generated.", "", ""],
        ["", "", ""],
        ["KEY CONCEPTS", "", ""],
        ["Guntha", "A unit of land measurement used in parts of India. 1 Guntha = 101.17 square meters.", ""],
        ["FSI (Floor Space Index)", "The ratio of a building's total floor area to the size of the land upon which it is built.", "Also known as FAR (Floor Area Ratio)"],
        ["Ancillary Area", "Additional construction area allowed beyond the basic FSI, typically 60% of the FSI area.", ""],
        ["Green Building Bonus", "Additional FSI incentive (typically 7%) for implementing green building features.", ""],
        ["Self-Redevelopment Bonus", "Additional FSI incentive (typically 10%) for societies undertaking self-redevelopment.", ""],
        ["", "", ""],
        ["HOW TO USE THIS CALCULATOR", "", ""],
        ["1. Enter all parameters in the 'Inputs' sheet.", "", ""],
        ["2. Review the detailed calculations in the 'Area Calculations', 'Cost Calculations', and 'Profit & Surplus' sheets.", "", ""],
        ["3. See the summary of results in the 'Summary Dashboard' sheet.", "", ""],
        ["", "", ""],
        ["IMPORTANT NOTES", "", ""],
        ["- All calculations are based on standard redevelopment practices in Maharashtra, India.", "", ""],
        ["- The actual profit may vary based on market conditions, approvals, and project execution.", "", ""],
        ["- Self-redevelopment requires professional project management and commitment from society members.", "", ""],
        ["- This calculator reveals the true profit potential of redevelopment projects, which is often not transparent in builder offers.", "", ""],
        ["", "", ""],
        ["FORMULA EXPLANATIONS", "", ""],
        ["Area Conversion", "1 Guntha = 101.17 square meters; 1 square meter = 10.764 square feet", ""],
        ["Offered Carpet Area", "Current carpet area × (1 + extra percentage / 100)", ""],
        ["Builder Sellable Area", "Total area with green bonus - Offered carpet area", ""],
        ["Number of Salable Flats", "Builder sellable area ÷ Average new flat size", ""],
        ["Profit Distribution", "In builder redevelopment: Builder gets profit sharing %, society gets the rest", ""],
        ["Surplus Corpus", "Society's profit that will be distributed among existing members", ""],
        ["", "", ""],
        ["CREATED BY", "", ""],
        ["This calculator was created to bring transparency to redevelopment economics and reveal the true profit potential for housing societies.", "", ""],
        ["For educational purposes only. Please consult professionals before making redevelopment decisions.", "", ""]
    ]
    
    # Update documentation cells
    docs_sheet.update('A3', docs_data)
    
    # Format section headers
    section_rows = [3, 6, 13, 17, 23]
    for row in section_rows:
        docs_sheet.format(f'A{row}', {
            "textFormat": {"bold": True},
            "backgroundColor": {"red": 0.85, "green": 0.9, "blue": 0.95}
        })
    
    # Format item headers (first column with short text)
    for row in range(7, 30):
        cell_value = docs_data[row-3][0]
        if len(cell_value) < 30 and len(cell_value) > 0 and cell_value[0] != '-':
            docs_sheet.format(f'A{row}', {
                "textFormat": {"bold": True}
            })
   # Set column widths
    docs_sheet.column_dimensions('A', 250)   # Concept
    docs_sheet.column_dimensions('B', 450)   # Description
    docs_sheet.column_dimensions('C', 250)   # Additional notes
    
    print("All sheets configured successfully!")
    
    return workbook.url


def setup_instructions():
    """Print setup instructions for Google Sheets API."""
    print("SETUP INSTRUCTIONS FOR GOOGLE SHEETS API")
    print("=" * 40)
    print("\n1. Set up a Google Cloud Project:")
    print("   a. Go to https://console.cloud.google.com/")
    print("   b. Create a new project")
    print("   c. Enable the Google Sheets API and Google Drive API")
    
    print("\n2. Create credentials:")
    print("   a. Go to 'APIs & Services' > 'Credentials'")
    print("   b. Click 'Create credentials' > 'Service account'")
    print("   c. Fill in the details and create the account")
    print("   d. Click on the service account email")
    print("   e. Go to 'Keys' tab > 'Add key' > 'Create new key' > 'JSON'")
    print("   f. Save the JSON file to your computer")
    
    print("\n3. Install required packages:")
    print("   pip install gspread oauth2client")
    
    print("\n4. Run this script with your credentials file:")
    print("   python google_sheets_generator.py /path/to/credentials.json")


def main():
    """Main function to run the Google Sheets generator."""
    import sys
    
    print("REDEVELOPMENT PROFIT CALCULATOR - GOOGLE SHEETS GENERATOR")
    print("=" * 60)
    
    # Check for credentials file
    if len(sys.argv) < 2:
        print("Error: Credentials file not provided.")
        print("Usage: python google_sheets_generator.py /path/to/credentials.json")
        setup_instructions()
        return
    
    creds_file = sys.argv[1]
    
    try:
        print("\nThis script will create a Google Sheet with all calculations.")
        print("The Google Sheet will have multiple sheets for inputs, calculations, and summary.")
        
        sheet_title = input("\nEnter a name for your Google Sheet [Redevelopment Profit Calculator]: ") or "Redevelopment Profit Calculator"
        
        # Create the Google Sheet
        print("\nCreating and configuring Google Sheet...")
        sheet_url = create_redevelopment_google_sheet(creds_file, sheet_title)
        
        print("\nGOOGLE SHEET CREATED SUCCESSFULLY!")
        print(f"You can access it at: {sheet_url}")
        print("\nThe Google Sheet contains the following sheets:")
        print("1. Inputs - Enter all parameters here")
        print("2. Area Calculations - Detailed area calculations")
        print("3. Cost Calculations - All cost components")
        print("4. Profit & Surplus - Profit calculations and surplus distribution")
        print("5. Summary Dashboard - Key metrics and results")
        print("6. Documentation - Help and explanations")
        
        print("\nInstructions:")
        print("1. Open the Google Sheet using the URL above")
        print("2. Start by entering your parameters in the 'Inputs' sheet")
        print("3. All calculations will update automatically")
        print("4. Review the results in the 'Summary Dashboard'")
        
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        import traceback
        traceback.print_exc()
        print("\nPlease make sure you have:")
        print("1. Installed the required packages: pip install gspread oauth2client")
        print("2. Set up Google Sheets API correctly")
        print("3. Provided a valid credentials file")
        setup_instructions()


if __name__ == "__main__":
    main() 
