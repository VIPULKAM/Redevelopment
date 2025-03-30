# Redevelopment Financial Calculator

A comprehensive financial calculator for housing society redevelopment projects in Maharashtra, India. This tool provides transparent calculations for profit/loss estimation, helping societies make informed decisions about redevelopment options.

## Features

- **Region-specific Calculations**: Tailored for Mumbai, Navi Mumbai, Thane, Pune, Nagpur, and Nashik
- **TDR & FSI Analysis**: Supports different TDR types with region-specific multipliers
- **Comparison Tools**: Evaluate self-redevelopment vs. builder-led approaches
- **Interactive Visualizations**: Visual breakdown of costs, profits, and FSI composition
- **Detailed Reports**: Export comprehensive financial analysis in text format

## Mathematical Model

### Area Calculations
- **Land Area Conversion**: `land_area_sqm = land_area * 101.17` (for Guntha) or direct sq.m
- **Member Area**: `total_current_carpet_area = current_carpet_area_per_member * total_members`
- **Offered Area**: `total_offered_carpet_area = total_current_carpet_area * (1 + extra_percentage/100)`

### FSI Components
- **Base FSI**: Determined by region, project type, and road width (Mumbai-specific)
- **TDR Component**: Calculated based on TDR type, percentage, and regional multipliers
- **Fungible/Ancillary FSI**: Additional components based on regional regulations
- **Total Effective FSI**: Sum of base FSI, TDR bonus, and fungible/ancillary components

### Buildable Area Calculation
- **Base Buildable Area**: `land_area_sqft * total_effective_fsi`
- **Bonus Areas**: Green building and self-redevelopment incentives
- **Sellable Area**: `total_final_area - total_offered_carpet_area`

### Cost Components
- **Premium/Ancillary Costs**: Based on ready reckoner rates and applicable percentages
- **TDR Costs**: Varies by type, region, and market rates
- **Construction**: `total_final_area * construction_cost_per_sqft`
- **Temporary Accommodation**: Rent and relocation expenses
- **Statutory Costs**: GST and stamp duty with exemptions for self-redevelopment
- **Financing**: Bank interest and other financial charges

### Profitability Analysis
- **Project Value**: `builder_sellable_area * market_rate_per_sqft`
- **Net Profit/Loss**: `project_value - total_cost`
- **Distribution**: Allocation between developer and society members

## Project Structure
```
redevelopment-calculator/
├── main.py                 # Application entry point
├── config.py               # Configuration data (FSI rules, TDR config)
├── calculator.py           # Core calculation logic
├── utils.py                # Utility functions
├── ui_components.py        # UI display components
└── visitor_counter.py      # Analytics integration (optional)
```

## Performance Optimizations

- **Data Caching**: Function results cached for improved responsiveness
- **Session State Management**: Persistent user inputs between interactions
- **Defensive Programming**: Robust error handling to prevent calculation failures

## Recent Enhancements

- Region-specific TDR calculation support
- Google Analytics integration for usage insights
- Performance improvements through strategic caching
- Modular code architecture for better maintainability

## License

This software is proprietary and is made available as a hosted service only. 

**Permitted Uses:**
- Accessing and using the software through the official hosted site
- Using the software for both personal and commercial purposes

**Prohibited Uses:**
- Downloading, copying, or distributing the software
- Modifying, adapting, or creating derivative works
- Reverse engineering or attempting to extract the source code
- Removing any copyright notices or proprietary markings

All rights to this software are reserved. No license, express or implied, is granted except for the limited use rights specified above.

© 2025 Vipul Kadam. All rights reserved.

## Analytics and Privacy

This application uses Google Analytics to collect anonymous usage data for the purpose of improving the service. We respect user privacy and do not collect personally identifiable information.

## Acknowledgements
- Shree Chandrashekhar Prabhu.
- Maharashtra real estate regulatory guidelines
- Municipal Development Control Regulations
- Streamlit framework for application development

## Contact

For questions, support, or feedback, please reach out to:
kadamvipul@gmail.com

---

**Disclaimer**: This calculator is provided for informational and educational purposes only. While we strive for accuracy, the results should not be considered as financial advice. Always consult with qualified professionals before making significant financial decisions regarding redevelopment projects. We are not liable for any consequences arising from use of this calculator website https://mh-redev-calc.streamlit.app/. By using this website you agrees to all the terms laid above!