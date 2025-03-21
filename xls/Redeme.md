# Redevelopment Profit Calculator

## Overview

The Redevelopment Profit Calculator is a tool designed to bring transparency to housing society redevelopment projects. It reveals the actual profits builders make, calculates the number of additional flats that can be sold, and determines the surplus corpus available for distribution to existing society members.

This tool empowers housing society members with knowledge typically not accessible during redevelopment negotiations.

## What This Tool Provides

- **Complete Transparency**: Step-by-step calculations of all redevelopment economics
- **Area Calculations**: Precise calculations of FSI, bonus areas, and sellable space
- **Financial Analysis**: Construction costs, project value, and profit calculations
- **Salable Flats**: Number of new flats that can be sold based on your parameters
- **Profit Distribution**: How profits are shared between developer and society
- **Surplus Corpus**: Amount available for distribution to existing members
- **Self vs. Builder**: Comparison between self-redevelopment and builder options

## Contents

This package contains:

1. `gen.py` - Python script that generates the Excel calculator
2. `guide.py` - Installation instructions
3. `README.md` - This file
4. `Redevelopment_Profit_Calculator.xlsx` - (Generated by the script) Ready-to-use Excel calculator

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Steps

1. Install the required package:
   ```
   pip install openpyxl
   ```

2. Run the generator script:
   ```
   python excel_generator.py
   ```

3. Open the generated Excel file (`Redevelopment_Profit_Calculator.xlsx`)

## Using the Calculator

1. Open the Excel file in Microsoft Excel or compatible spreadsheet software
2. Navigate to the 'Inputs' sheet and enter your parameters:
   - Land area, members, carpet area, etc.
   - FSI, bonus percentages
   - Construction costs, market rates
   - Project type (self or builder redevelopment)
3. All calculations will update automatically
4. View the 'Summary Dashboard' for key metrics and results
5. Explore other sheets for detailed calculations

## Example Calculation

Using standard parameters for a Mumbai redevelopment project:
- 10 Guntha land area
- 40 existing members with 500 sqft flats each
- 30% extra area offered
- 2.5 FSI with various bonuses
- Construction cost of ₹3,000/sqft
- Market rate of ₹17,500/sqft

The calculator reveals that builders typically make approximately ₹1.46 Cr profit per flat.

## Educational Purpose

This calculator was created for educational purposes to empower society members with knowledge about redevelopment economics. Please consult with professionals before making redevelopment decisions.

## Sharing

Feel free to share this tool with housing societies and resident welfare associations. The Excel file can be used directly without requiring Python to be installed.

## License

This tool is provided for free educational use. Please use it to promote transparency in redevelopment projects.
