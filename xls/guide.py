#!/usr/bin/env python3
"""
Installation Guide for Redevelopment Profit Calculator Excel Generator

This file provides instructions for installing the required packages
and running the Excel generator script.
"""

def print_installation_guide():
    """Print installation instructions."""
    print("INSTALLATION GUIDE FOR REDEVELOPMENT PROFIT CALCULATOR")
    print("=" * 60)
    print("\nPREREQUISITES:")
    print("1. Python 3.7 or higher")
    print("2. pip (Python package installer)")
    
    print("\nINSTALLATION STEPS:")
    print("1. Install the required package using pip:")
    print("   pip install openpyxl")
    print("   (or)")
    print("   pip3 install openpyxl")
    
    print("\n2. Save the excel_generator.py script to your computer")
    
    print("\n3. Run the script:")
    print("   python excel_generator.py")
    print("   (or)")
    print("   python3 excel_generator.py")
    
    print("\nTROUBLESHOOTING:")
    print("- If you get an error about missing openpyxl module, make sure you've run the pip install command.")
    print("- If you have multiple Python versions, you might need to use python3 instead of python.")
    print("- Make sure you have write permission in the folder where you're running the script.")
    
    print("\nAFTER INSTALLATION:")
    print("1. The script will generate a file named 'Redevelopment_Profit_Calculator.xlsx'")
    print("2. Open this file with Microsoft Excel or a compatible spreadsheet program")
    print("3. Enter your parameters in the 'Inputs' sheet")
    print("4. All calculations will update automatically")
    print("5. View the summary and results in the 'Summary Dashboard' sheet")
    
    print("\nNOTE:")
    print("This calculator is for educational purposes only.")
    print("Please consult with professionals before making redevelopment decisions.")
    
    print("\nINTRODUCING THE CALCULATOR TO OTHERS:")
    print("1. Share both the Excel file and the Python script")
    print("2. The Excel file is ready to use and doesn't require Python to operate")
    print("3. Encourage users to explore all sheets to understand the calculations")
    print("4. Highlight the 'Documentation' sheet for explanations of terms and concepts")


if __name__ == "__main__":
    print_installation_guide()
