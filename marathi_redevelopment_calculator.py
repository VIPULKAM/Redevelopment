import streamlit as st
import matplotlib.pyplot as plt

# Set page configuration FIRST
st.set_page_config(
    page_title="पुनर्विकास नफा कॅल्क्युलेटर",
    page_icon="🏢",
    layout="wide"
)

# Then add CSS for proper Marathi font rendering
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;700&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Noto Sans Devanagari', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# Region names in Marathi
REGION_NAMES = {
    "Mumbai": "मुंबई",
    "Navi Mumbai": "नवी मुंबई",
    "Thane": "ठाणे",
    "Pune": "पुणे",
    "Nagpur": "नागपूर",
    "Nashik": "नाशिक"
}

# Get English key from Marathi region name
def get_english_region_key(marathi_name):
    for eng_key, mar_name in REGION_NAMES.items():
        if mar_name == marathi_name:
            return eng_key
    return marathi_name  # Return original if not found

# ======================
# Region Configuration
# ======================
REGION_CONFIG = {
    "Mumbai": {
        "fsi_rules": {
            "residential": 2.5, 
            "commercial": 5.0, 
            "tdr_multiplier": 2.5
        },
        "premium_rates": {
            "construction": 3000, 
            "fungible_fsi": 0.35
        },
        "bonuses": {
            "green_building": 0.07, 
            "self_redev": 0.10, 
            "ancillary": 0.60
        },
        "parking": {
            "redev_reduction": 0.20, 
            "car_lift_threshold": 2000
        },
        "tdr_rates": {
            "residential": 0.4, 
            "commercial": 0.3
        },
        "stamp_duty": {
            "builder": 0.06,  # 6% for builder redevelopment
            "self": 1000      # Flat Rs.1000 per unit for self-redevelopment
        },
        "gst": {
            "builder": 0.05,  # 5% for builder redevelopment
            "self": 0.0       # 0% for self-redevelopment
        }
    },
    "Navi Mumbai": {
        "fsi_rules": {
            "residential": 2.0, 
            "commercial": 4.0, 
            "tdr_multiplier": 2.0
        },
        "premium_rates": {
            "construction": 2800, 
            "fungible_fsi": 0.33
        },
        "bonuses": {
            "green_building": 0.06, 
            "self_redev": 0.12, 
            "ancillary": 0.50
        },
        "parking": {
            "redev_reduction": 0.25, 
            "car_lift_threshold": 1800
        },
        "tdr_rates": {
            "residential": 0.38, 
            "commercial": 0.28
        },
        "stamp_duty": {
            "builder": 0.06,
            "self": 1000
        },
        "gst": {
            "builder": 0.05,
            "self": 0.0
        }
    },
    "Thane": {
        "fsi_rules": {
            "residential": 3.0, 
            "commercial": 4.0, 
            "tdr_multiplier": 2.0
        },
        "premium_rates": {
            "construction": 2500,
            "fungible_fsi": 0.30
        },
        "bonuses": {
            "green_building": 0.05,
            "self_redev": 0.15,
            "ancillary": 0.50
        },
        "parking": {
            "redev_reduction": 0.30,
            "car_lift_threshold": 1500
        },
        "tdr_rates": {
            "residential": 0.35, 
            "commercial": 0.25
        },
        "stamp_duty": {
            "builder": 0.06,
            "self": 1000
        },
        "gst": {
            "builder": 0.05,
            "self": 0.0
        }
    },
    "Pune": {
        "fsi_rules": {
            "residential": 1.75, 
            "commercial": 3.0, 
            "tdr_multiplier": 1.8
        },
        "premium_rates": {
            "construction": 2700, 
            "fungible_fsi": 0.28
        },
        "bonuses": {
            "green_building": 0.05,
            "self_redev": 0.12,
            "ancillary": 0.45
        },
        "parking": {
            "redev_reduction": 0.25,
            "car_lift_threshold": 1800
        },
        "tdr_rates": {
            "residential": 0.35, 
            "commercial": 0.25
        },
        "stamp_duty": {
            "builder": 0.06,
            "self": 1000
        },
        "gst": {
            "builder": 0.05,
            "self": 0.0
        }
    },
    "Nagpur": {
        "fsi_rules": {
            "residential": 1.5, 
            "commercial": 2.5, 
            "tdr_multiplier": 1.5
        },
        "premium_rates": {
            "construction": 2200, 
            "fungible_fsi": 0.25
        },
        "bonuses": {
            "green_building": 0.05,
            "self_redev": 0.10,
            "ancillary": 0.40
        },
        "parking": {
            "redev_reduction": 0.20,
            "car_lift_threshold": 1500
        },
        "tdr_rates": {
            "residential": 0.30, 
            "commercial": 0.20
        },
        "stamp_duty": {
            "builder": 0.06,
            "self": 1000
        },
        "gst": {
            "builder": 0.05,
            "self": 0.0
        }
    },
    "Nashik": {
        "fsi_rules": {
            "residential": 1.6, 
            "commercial": 2.8, 
            "tdr_multiplier": 1.6
        },
        "premium_rates": {
            "construction": 2300, 
            "fungible_fsi": 0.26
        },
        "bonuses": {
            "green_building": 0.05,
            "self_redev": 0.10,
            "ancillary": 0.40
        },
        "parking": {
            "redev_reduction": 0.20,
            "car_lift_threshold": 1600
        },
        "tdr_rates": {
            "residential": 0.32, 
            "commercial": 0.22
        },
        "stamp_duty": {
            "builder": 0.06,
            "self": 1000
        },
        "gst": {
            "builder": 0.05,
            "self": 0.0
        }
    }
}

def get_ready_reckoner_rate(region, year):
    """Get ready reckoner rate for region and year."""
    ready_reckoner_rates = {
        "Mumbai": {2022: 150000, 2023: 160000, 2024: 170000},
        "Navi Mumbai": {2022: 120000, 2023: 130000, 2024: 140000},
        "Thane": {2022: 100000, 2023: 110000, 2024: 120000},
        "Pune": {2022: 80000, 2023: 85000, 2024: 90000},
        "Nagpur": {2022: 60000, 2023: 65000, 2024: 70000},
        "Nashik": {2022: 70000, 2023: 75000, 2024: 80000}
    }
    return ready_reckoner_rates.get(region, {}).get(year, 0)

def format_currency(amount):
    """Format amount in Indian Rupees with commas."""
    if amount >= 10000000:  # Convert to crores
        return f"₹{amount/10000000:.2f} कोटी (₹{amount:,.2f})"
    elif amount >= 100000:  # Convert to lakhs
        return f"₹{amount/100000:.2f} लाख (₹{amount:,.2f})"
    else:
        return f"₹{amount:,.2f}"

def format_area(area, unit="sqft"):
    """Format area with commas and unit."""
    if unit == "sqft":
        unit = "चौरस फूट"
    elif unit == "sqm":
        unit = "चौरस मीटर"
    elif unit == "Guntha":
        unit = "गुंठा"
    return f"{area:,.2f} {unit}"

def calculate_profit(
        region,
        ready_reckoner_year,
        land_area_guntha,
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
        tdr_percentage=0.0
    ):
    """Calculate profit from redevelopment project with TDR support and tax considerations."""
    # Convert guntha to square meters (1 guntha = 101.17 sqm)
    land_area_sqm = land_area_guntha * 101.17
    
    # Get ready reckoner rate for the region and year
    ready_reckoner_rate = get_ready_reckoner_rate(region, ready_reckoner_year)
    
    # Calculate current carpet area
    total_current_carpet_area = current_carpet_area_per_member * total_members
    
    # Calculate offered carpet area (with extra percentage)
    total_offered_carpet_area = total_current_carpet_area * (1 + extra_carpet_percentage/100)
    
    # Convert to sqft (1 sqm = 10.764 sqft)
    land_area_sqft = land_area_sqm * 10.764
    
    # TDR Calculation
    tdr_factor = REGION_CONFIG[region]["tdr_rates"][project_type]
    tdr_multiplier = REGION_CONFIG[region]["fsi_rules"]["tdr_multiplier"]
    tdr_bonus = (tdr_percentage/100) * tdr_factor * fsi
    effective_fsi = fsi + tdr_bonus
    
    # Calculate buildable area with effective FSI
    total_buildable_area_sqft = land_area_sqft * effective_fsi
    
    # Calculate green building bonus
    green_bonus = total_buildable_area_sqft * REGION_CONFIG[region]["bonuses"]["green_building"]
    
    # Calculate self-redevelopment bonus if applicable
    self_redev_bonus = 0
    if is_self_redevelopment:
        self_redev_bonus = total_buildable_area_sqft * REGION_CONFIG[region]["bonuses"]["self_redev"]
    
    # Calculate total area with bonuses
    total_final_area = total_buildable_area_sqft + green_bonus + self_redev_bonus
    
    # Calculate builder sellable area
    builder_sellable_area = total_final_area - total_offered_carpet_area
    
    # Calculate premium cost
    premium_cost_per_sqm = ready_reckoner_rate * fungible_fsi
    premium_cost = land_area_sqm * premium_cost_per_sqm
    
    # Calculate TDR cost
    tdr_cost = 0
    if tdr_percentage > 0:
        tdr_cost = land_area_sqm * ready_reckoner_rate * (tdr_percentage/100) * tdr_factor
    
    # Calculate construction cost
    construction_cost = total_final_area * construction_cost_per_sqft
    
    # Calculate rent cost
    rent_cost = total_members * rent_per_month * rent_duration_months
    
    # Calculate relocation cost
    relocation_cost = total_members * relocation_cost_per_member
    
    # Calculate GST (only for builder redevelopment)
    gst_cost = 0
    if not is_self_redevelopment:
        gst_rate = REGION_CONFIG[region]["gst"]["builder"]
        gst_cost = construction_cost * gst_rate
    
    # Calculate stamp duty
    stamp_duty_cost = 0
    if is_self_redevelopment:
        # Flat rate per unit for self-redevelopment
        stamp_duty_cost = REGION_CONFIG[region]["stamp_duty"]["self"] * total_members
    else:
        # Percentage of project value for builder redevelopment
        stamp_duty_rate = REGION_CONFIG[region]["stamp_duty"]["builder"]
        # Apply stamp duty to the offered carpet area value (for members' agreements)
        member_area_value = total_offered_carpet_area * market_rate_per_sqft
        stamp_duty_cost = member_area_value * stamp_duty_rate
    
    # Calculate total cost (now with GST and stamp duty)
    total_cost = premium_cost + tdr_cost + construction_cost + rent_cost + relocation_cost + bank_interest + gst_cost + stamp_duty_cost
    
    # Calculate project value
    project_value = builder_sellable_area * market_rate_per_sqft
    
    # Calculate total profit
    total_profit = project_value - total_cost
    
    # Calculate profit distribution
    profit_sharing_percentage = profit_sharing_with_developer
    developer_profit = 0
    society_profit = total_profit
    
    # Handle loss scenario differently
    if total_profit < 0:
        # In case of loss, society bears all loss in self-redevelopment
        if not is_self_redevelopment:
            # In builder redevelopment with loss, the loss sharing would depend on the agreement
            # For simplicity, we're assuming the loss is shared according to the profit sharing ratio
            developer_profit = total_profit * (profit_sharing_percentage / 100)
            society_profit = total_profit - developer_profit
    else:
        # Normal profit distribution for profitable projects
        if not is_self_redevelopment:
            developer_profit = total_profit * (profit_sharing_percentage / 100)
            society_profit = total_profit - developer_profit
    
    # Calculate per member profit (handle zero members)
    per_member_profit = society_profit / max(1, total_members)  # Prevent division by zero
    
    # Calculate number of salable flats
    num_salable_flats = builder_sellable_area / avg_new_flat_size
    
    # Return results
    return {
        "region": region,
        "project_type": project_type,
        "is_self_redevelopment": is_self_redevelopment,
        "land_area_guntha": land_area_guntha,
        "land_area_sqm": land_area_sqm,
        "ready_reckoner_rate": ready_reckoner_rate,
        "fsi": fsi,
        "effective_fsi": effective_fsi,
        "tdr_percentage": tdr_percentage,
        "tdr_cost": tdr_cost,
        "fungible_fsi": fungible_fsi,
        "total_current_carpet_area": total_current_carpet_area,
        "total_offered_carpet_area": total_offered_carpet_area,
        "total_buildable_area_sqft": total_buildable_area_sqft,
        "green_bonus": green_bonus,
        "self_redev_bonus": self_redev_bonus,
        "total_final_area": total_final_area,
        "builder_sellable_area": builder_sellable_area,
        "premium_cost_per_sqm": premium_cost_per_sqm,
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
        "profit_sharing_percentage": profit_sharing_percentage,
        "developer_profit": developer_profit,
        "society_profit": society_profit,
        "per_member_profit": per_member_profit,
        "num_salable_flats": num_salable_flats
    }

# Title and description in Marathi
st.title("पुनर्विकास नफा कॅल्क्युलेटर")
st.markdown("""
    हा कॅल्क्युलेटर गृहनिर्माण संस्थांना पुनर्विकास प्रकल्पांच्या आर्थिक पैलूंचे मूल्यांकन करण्यात मदत करतो. 
    हे नफा, अतिरिक्त निधी, आणि विक्रीयोग्य सदनिकांसाठी पारदर्शक गणना प्रदान करते.
""")

# Create two columns - one for inputs, one for results
col1, col2 = st.columns([1, 2])

# Input form in the first column
with col1:
    st.header("प्रकल्प तपशील प्रविष्ट करा")
    
    # Location Parameters
    st.subheader("स्थान")
    region_display = st.selectbox("प्रदेश", list(REGION_NAMES.values()))
    # Convert display name back to English key
    region = get_english_region_key(region_display)
    
    ready_reckoner_year = st.selectbox("रेडी रेकनर वर्ष", [2022, 2023, 2024])
    project_type_display = st.selectbox("प्रकल्प प्रकार", ["निवासी", "वाणिज्यिक"])
    # Convert to English key
    if project_type_display == "निवासी":
        project_type = "residential"
    else:
        project_type = "commercial"
        
    redevelopment_type = st.radio(
        "पुनर्विकास प्रकार", 
        ["स्वयं पुनर्विकास", "बिल्डर पुनर्विकास"]
    )
    is_self_redevelopment = (redevelopment_type == "स्वयं पुनर्विकास")
    
    # Land Parameters
    st.subheader("जमीन मापदंड")
    land_area_guntha = st.number_input("जमीन क्षेत्र (गुंठा)", value=10.0, min_value=0.1)
    total_members = st.number_input("सदस्य/सदनिकांची संख्या", value=40, min_value=1, step=1)
    carpet_area = st.number_input("प्रति सदस्य वर्तमान कार्पेट क्षेत्र (चौरस फूट)", value=500.0, min_value=100.0)
    extra_percentage = st.number_input("अतिरिक्त कार्पेट टक्केवारी", value=30.0, min_value=0.0)
    
    # Construction Parameters
    st.subheader("बांधकाम मापदंड")
    
    # Base FSI
    default_fsi = REGION_CONFIG[region]["fsi_rules"][project_type]
    fsi = st.number_input("मूळ एफएसआय मूल्य", value=float(default_fsi), min_value=0.1)
    
    # TDR Input
    tdr_percentage = st.number_input(
        "टीडीआर टक्केवारी (0-100%)", 
        min_value=0.0, 
        max_value=100.0, 
        value=0.0
    )
    
    # Fungible FSI
    default_fungible = REGION_CONFIG[region]["premium_rates"]["fungible_fsi"]
    default_fungible_pct = default_fungible * 100
    fungible_input = st.number_input(
        "फंजिबल एफएसआय टक्केवारी (25-40%)", 
        value=float(default_fungible_pct),
        min_value=0.0,
        max_value=100.0
    )
    fungible_fsi = fungible_input / 100  # Convert to decimal
    
    # Cost parameters
    default_construction = REGION_CONFIG[region]["premium_rates"]["construction"]
    construction_cost = st.number_input(
        "प्रति चौरस फूट बांधकाम खर्च (₹)", 
        value=float(default_construction),
        min_value=1000.0
    )
    
    market_rate = st.number_input("प्रति चौरस फूट बाजार दर (₹)", value=17500.0, min_value=5000.0)
    avg_flat_size = st.number_input("नवीन विक्रीयोग्य सदनिकांचा सरासरी आकार (चौरस फूट)", value=750.0, min_value=200.0)
    
    # Financial Parameters
    st.subheader("आर्थिक मापदंड")
    rent = st.number_input("प्रति सदनिका मासिक भाडे (₹)", value=15000.0, min_value=0.0)
    rent_months = st.number_input("भाडे कालावधी (महिने)", value=36, min_value=0, step=1)
    relocation = st.number_input("प्रति सदस्य स्थलांतर खर्च (₹)", value=20000.0, min_value=0.0)
    bank_interest = st.number_input("बँक व्याज (₹)", value=50000000.0, min_value=0.0)
    
    # Profit Sharing (if builder redevelopment)
    profit_sharing = 0
    if not is_self_redevelopment:
        profit_sharing = st.number_input(
            "डेव्हलपरसह नफा वाटप (%)", 
            value=30.0,
            min_value=0.0,
            max_value=100.0
        )
    
    # Calculate button
    calculate_button = st.button("नफा गणना करा", type="primary")

# Results in the second column
with col2:
    if calculate_button:
        results = calculate_profit(
            # Location parameters
            region=region,
            ready_reckoner_year=ready_reckoner_year,
            
            # Land parameters
            land_area_guntha=land_area_guntha,
            current_carpet_area_per_member=carpet_area,
            total_members=total_members,
            extra_carpet_percentage=extra_percentage,
            
            # Construction parameters
            fsi=fsi,
            fungible_fsi=fungible_fsi,
            construction_cost_per_sqft=construction_cost,
            market_rate_per_sqft=market_rate,
            avg_new_flat_size=avg_flat_size,
            
            # Financial parameters
            rent_per_month=rent,
            rent_duration_months=rent_months,
            relocation_cost_per_member=relocation,
            bank_interest=bank_interest,
            
            # Project type
            project_type=project_type,
            is_self_redevelopment=is_self_redevelopment,
            profit_sharing_with_developer=profit_sharing,
            
            # TDR parameter
            tdr_percentage=tdr_percentage
        )
        
        # Display results in sections
        st.header("पुनर्विकास प्रकल्प विश्लेषण")
        
        # Project basics
        st.subheader("प्रकल्प मूलभूत")
        st.markdown(f"""
        - **प्रदेश**: {REGION_NAMES[results['region']]}
        - **प्रकल्प प्रकार**: {"निवासी" if results['project_type'] == "residential" else "वाणिज्यिक"}
        - **पुनर्विकास प्रकार**: {"स्वयं पुनर्विकास" if results['is_self_redevelopment'] else "बिल्डर पुनर्विकास"}
        """)
        
        # Land and area details
        st.subheader("जमीन आणि क्षेत्र तपशील")
        st.markdown(f"""
        - **जमीन क्षेत्र**: {format_area(results['land_area_guntha'], 'Guntha')} ({format_area(results['land_area_sqm'], 'sqm')})
        - **मूळ एफएसआय**: {results['fsi']}
        - **टीडीआर टक्केवारी**: {results['tdr_percentage']:.1f}%
        - **प्रभावी एफएसआय (टीडीआर सह)**: {results['effective_fsi']:.2f}
        - **फंजिबल एफएसआय**: {results['fungible_fsi'] * 100:.1f}%
        - **वर्तमान कार्पेट क्षेत्र**: {format_area(results['total_current_carpet_area'])}
        - **देऊ केलेले कार्पेट क्षेत्र**: {format_area(results['total_offered_carpet_area'])}
        - **एकूण बांधकामयोग्य क्षेत्र**: {format_area(results['total_buildable_area_sqft'])}
        - **हरित इमारत बोनस**: {format_area(results['green_bonus'])}
        - **स्वयं पुनर्विकास बोनस**: {format_area(results['self_redev_bonus'])}
        - **बोनससह एकूण क्षेत्र**: {format_area(results['total_final_area'])}
        - **बिल्डर विक्रीयोग्य क्षेत्र**: {format_area(results['builder_sellable_area'])}
        """)
        
        # Premium calculation
        st.subheader("प्रीमियम आणि टीडीआर गणना")
        st.markdown(f"""
        - **रेडी रेकनर दर**: {format_currency(results['ready_reckoner_rate'])}/sqm
        - **फंजिबल एफएसआय फॅक्टर**: {results['fungible_fsi']:.2f} ({results['fungible_fsi'] * 100:.1f}%)
        - **जमीन क्षेत्र**: {format_area(results['land_area_sqm'], 'sqm')}
        - **प्रीमियम खर्च सूत्र**: जमीन क्षेत्र × रेडी रेकनर दर × फंजिबल एफएसआय फॅक्टर
        - **प्रीमियम खर्च गणना**: {format_area(results['land_area_sqm'], 'sqm')} × {format_currency(results['ready_reckoner_rate'])}/sqm × {results['fungible_fsi']:.2f}
        - **प्रति चौरस मीटर प्रीमियम खर्च**: {format_currency(results['premium_cost_per_sqm'])}/sqm
        - **एकूण प्रीमियम खर्च**: {format_currency(results['premium_cost'])}
        - **टीडीआर खर्च**: {format_currency(results['tdr_cost'])}
        """)
        
        # Cost analysis
        st.subheader("खर्च विश्लेषण")
        st.markdown(f"""
        - **प्रीमियम खर्च**: {format_currency(results['premium_cost'])}
        - **टीडीआर खर्च**: {format_currency(results['tdr_cost'])}
        - **बांधकाम खर्च**: {format_currency(results['construction_cost'])} ({format_currency(results['construction_cost_per_sqft'])}/sqft)
        - **जीएसटी (बांधकाम वर 5%)**: {format_currency(results['gst_cost'])}
        - **मुद्रांक शुल्क**: {format_currency(results['stamp_duty_cost'])}
        - **भाडे खर्च**: {format_currency(results['rent_cost'])}
        - **स्थलांतर खर्च**: {format_currency(results['relocation_cost'])}
        - **बँक व्याज**: {format_currency(results['bank_interest'])}
        - **एकूण प्रकल्प खर्च**: {format_currency(results['total_cost'])}
        """)
        
        # Revenue and profit/loss
        if results['total_profit'] >= 0:
            st.subheader("महसूल आणि नफा")
        else:
            st.subheader("महसूल आणि तोटा")
            
        st.markdown(f"""
        - **बाजार दर**: {format_currency(results['market_rate_per_sqft'])}/sqft
        - **प्रकल्प मूल्य**: {format_currency(results['project_value'])}
        - **एकूण {"नफा" if results['total_profit'] >= 0 else "तोटा"}**: {format_currency(abs(results['total_profit']))}
        """)
        
        # Profit/Loss distribution
        if results['total_profit'] >= 0:
            st.subheader("नफा वितरण")
        else:
            st.subheader("तोटा वितरण")
            
        if results['total_profit'] >= 0:
            # Profit scenario
            if results['is_self_redevelopment']:
                st.markdown(f"""
                - **सोसायटी नफा**: {format_currency(results['society_profit'])}
                - **प्रति सदस्य नफा**: {format_currency(results['per_member_profit'])}
                """)
            else:
                st.markdown(f"""
                - **डेव्हलपर नफा ({results['profit_sharing_percentage']}%)**: {format_currency(results['developer_profit'])}
                - **सोसायटी नफा**: {format_currency(results['society_profit'])}
                - **प्रति सदस्य नफा**: {format_currency(results['per_member_profit'])}
                """)
        else:
            # Loss scenario
            if results['is_self_redevelopment']:
                st.markdown(f"""
                - **सोसायटी तोटा**: {format_currency(abs(results['society_profit']))}
                - **प्रति सदस्य तोटा**: {format_currency(abs(results['per_member_profit']))}
                """)
            else:
                st.markdown(f"""
                - **डेव्हलपर तोटा ({results['profit_sharing_percentage']}%)**: {format_currency(abs(results['developer_profit']))}
                - **सोसायटी तोटा**: {format_currency(abs(results['society_profit']))}
                - **प्रति सदस्य तोटा**: {format_currency(abs(results['per_member_profit']))}
                """)
        
        # Salable flats
        st.subheader("विक्रीयोग्य सदनिका")
        st.markdown(f"""
        - **संभाव्य विक्रीयोग्य सदनिकांची संख्या**: {results['num_salable_flats']:.1f}
        """)
        
        # Add a download button for the report
        st.download_button(
            label="अहवाल मजकूर म्हणून डाउनलोड करा",
            data=f"""
पुनर्विकास प्रकल्प विश्लेषण
==================================================

प्रकल्प मूलभूत:
--------------
प्रदेश: {REGION_NAMES[results['region']]}
प्रकल्प प्रकार: {"निवासी" if results['project_type'] == "residential" else "वाणिज्यिक"}
पुनर्विकास प्रकार: {"स्वयं पुनर्विकास" if results['is_self_redevelopment'] else "बिल्डर पुनर्विकास"}

जमीन आणि क्षेत्र तपशील:
------------------
जमीन क्षेत्र: {format_area(results['land_area_guntha'], 'Guntha')} ({format_area(results['land_area_sqm'], 'sqm')})
मूळ एफएसआय: {results['fsi']}
टीडीआर टक्केवारी: {results['tdr_percentage']:.1f}%
प्रभावी एफएसआय (टीडीआर सह): {results['effective_fsi']:.2f}
फंजिबल एफएसआय: {results['fungible_fsi'] * 100:.1f}%
वर्तमान कार्पेट क्षेत्र: {format_area(results['total_current_carpet_area'])}
देऊ केलेले कार्पेट क्षेत्र: {format_area(results['total_offered_carpet_area'])}
एकूण बांधकामयोग्य क्षेत्र: {format_area(results['total_buildable_area_sqft'])}
हरित इमारत बोनस: {format_area(results['green_bonus'])}
स्वयं पुनर्विकास बोनस: {format_area(results['self_redev_bonus'])}
बोनससह एकूण क्षेत्र: {format_area(results['total_final_area'])}
बिल्डर विक्रीयोग्य क्षेत्र: {format_area(results['builder_sellable_area'])}

प्रीमियम आणि टीडीआर गणना:
-----------------
रेडी रेकनर दर: {format_currency(results['ready_reckoner_rate'])}/sqm
फंजिबल एफएसआय फॅक्टर: {results['fungible_fsi']:.2f} ({results['fungible_fsi'] * 100:.1f}%)
जमीन क्षेत्र: {format_area(results['land_area_sqm'], 'sqm')}
प्रीमियम खर्च सूत्र: जमीन क्षेत्र × रेडी रेकनर दर × फंजिबल एफएसआय फॅक्टर
प्रीमियम खर्च: {format_currency(results['premium_cost'])}
टीडीआर खर्च: {format_currency(results['tdr_cost'])}

खर्च विश्लेषण:
------------
प्रीमियम खर्च: {format_currency(results['premium_cost'])}
टीडीआर खर्च: {format_currency(results['tdr_cost'])}
बांधकाम खर्च: {format_currency(results['construction_cost'])} ({format_currency(results['construction_cost_per_sqft'])}/sqft)
जीएसटी (बांधकामावर 5%): {format_currency(results['gst_cost'])}
मुद्रांक शुल्क: {format_currency(results['stamp_duty_cost'])}
भाडे खर्च: {format_currency(results['rent_cost'])}
स्थलांतर खर्च: {format_currency(results['relocation_cost'])}
बँक व्याज: {format_currency(results['bank_interest'])}
एकूण प्रकल्प खर्च: {format_currency(results['total_cost'])}

महसूल आणि {"नफा" if results['total_profit'] >= 0 else "तोटा"}:
--------------
बाजार दर: {format_currency(results['market_rate_per_sqft'])}/sqft
प्रकल्प मूल्य: {format_currency(results['project_value'])}
एकूण {"नफा" if results['total_profit'] >= 0 else "तोटा"}: {format_currency(abs(results['total_profit']))}

{"नफा" if results['total_profit'] >= 0 else "तोटा"} वितरण:
-----------------
{"सोसायटी " + ("नफा" if results['society_profit'] >= 0 else "तोटा") + ": " + format_currency(abs(results['society_profit']))}
{"डेव्हलपर " + ("नफा" if results['developer_profit'] >= 0 else "तोटा") + " (" + str(results['profit_sharing_percentage']) + "%): " + format_currency(abs(results['developer_profit'])) if not results['is_self_redevelopment'] else ""}
प्रति सदस्य {"नफा" if results['per_member_profit'] >= 0 else "तोटा"}: {format_currency(abs(results['per_member_profit']))}

विक्रीयोग्य सदनिका:
-----------
संभाव्य विक्रीयोग्य सदनिकांची संख्या: {results['num_salable_flats']:.1f}
            """,
            file_name="punarvikās_ahavāl.txt",
            mime="text/plain",
        )
        
        # Add visualization section - with ENGLISH labels for the charts
        st.subheader("प्रकल्प आर्थिक व्हिज्युअलायझेशन")
        
        # Create tabs for different visualizations
        viz_tab1, viz_tab2 = st.tabs(["खर्च विभाजन", "नफा विश्लेषण"])
        
        with viz_tab1:
            # Cost breakdown pie chart - using English labels
            cost_labels = [
                'Premium Cost', 
                'TDR Cost', 
                'Construction Cost', 
                'GST', 
                'Stamp Duty', 
                'Rent Cost', 
                'Relocation Cost', 
                'Bank Interest'
            ]
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
            plt.title('Cost Breakdown')  # English title
            st.pyplot(fig1)
        
        with viz_tab2:
            # Check if project is profitable or in loss
            is_profitable = results['total_profit'] >= 0
            
            # Profit and area allocation
            fig2, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
            
            # Area allocation - using English labels
            area_labels = ['Society Area', 'Sellable Area']
            area_values = [
                results['total_offered_carpet_area'],
                results['builder_sellable_area']
            ]
            ax1.bar(area_labels, area_values, color=['#3498db', '#2ecc71'])
            ax1.set_ylabel('Square Feet')
            ax1.set_title('Area Allocation')
            
            # For profit/loss distribution visualization - using English labels
            if is_profitable:
                # Handle profit scenario
                if not results['is_self_redevelopment']:
                    # Builder redevelopment with profit
                    profit_labels = ['Developer Profit', 'Society Profit']
                    profit_values = [
                        max(0, results['developer_profit']),  # Ensure positive values
                        max(0, results['society_profit'])     # Ensure positive values
                    ]
                    # Only create pie chart if we have positive values
                    if all(v > 0 for v in profit_values):
                        ax2.pie(profit_values, labels=profit_labels, autopct='%1.1f%%', startangle=90, colors=['#e74c3c', '#3498db'])
                        ax2.axis('equal')
                        ax2.set_title('Profit Distribution')
                    else:
                        # Fallback to bar chart if any value is not positive
                        ax2.bar(profit_labels, profit_values, color=['#e74c3c', '#3498db'])
                        ax2.set_ylabel('Profit Amount (₹)')
                        ax2.set_title('Profit Distribution')
                else:
                    # For self-redevelopment with profit - compare cost vs project value with bar chart
                    ax2.bar(['Total Cost', 'Project Value'], 
                          [results['total_cost'], results['project_value']], 
                          color=['#e74c3c', '#3498db'])
                    ax2.set_ylabel('Amount (₹)')
                    ax2.set_title('Cost vs. Project Value')
            else:
                # Handle loss scenario with a bar chart
                if not results['is_self_redevelopment']:
                    # Builder redevelopment with loss
                    loss_labels = ['Developer Loss', 'Society Loss']
                    loss_values = [
                        abs(results['developer_profit']),
                        abs(results['society_profit'])
                    ]
                    ax2.bar(loss_labels, loss_values, color=['#e74c3c', '#3498db'])
                    ax2.set_ylabel('Loss Amount (₹)')
                    ax2.set_title('Loss Distribution')
                else:
                    # Self-redevelopment with loss - show cost vs value comparison
                    ax2.bar(['Total Cost', 'Project Value'], 
                          [results['total_cost'], results['project_value']], 
                          color=['#e74c3c', '#3498db'])
                    ax2.set_ylabel('Amount (₹)')
                    ax2.set_title('Cost vs. Project Value (Loss Scenario)')
            
            plt.tight_layout()
            st.pyplot(fig2)

# Add documentation section
st.markdown("---")

# Premium & TDR calculation documentation
with st.expander("महाराष्ट्रातील प्रीमियम आणि टीडीआर गणनेबद्दल"):
    st.markdown("""
    ## महाराष्ट्रातील पुनर्विकासासाठी प्रीमियम आणि टीडीआर गणना समजून घेणे

    1. **नियामक आधार**
       महाराष्ट्रातील पुनर्विकास प्रकल्पांसाठी प्रीमियम आणि टीडीआर गणना महाराष्ट्र प्रादेशिक आणि नगररचना अधिनियम आणि त्यानंतरच्या शासन निर्णयांवर आधारित आहे.
       
    2. **प्रीमियम सूत्र घटक**
       प्रीमियम खर्च = जमीन क्षेत्र (चौरस मीटर) × रेडी रेकनर दर (₹/चौरस मीटर) × फंजिबल एफएसआय फॅक्टर
       
       जेथे:
       - जमीन क्षेत्र: चौरस मीटरमध्ये एकूण भूखंड क्षेत्र
       - रेडी रेकनर दर: सरकार-प्रकाशित मालमत्ता मूल्यांकन दर (वार्षिक अद्यतनित)
       - फंजिबल एफएसआय फॅक्टर: अतिरिक्त बांधकाम अधिकार गुणक (सामान्यतः 0.25-0.40)
    
    3. **टीडीआर (विकास अधिकारांचे हस्तांतरण)**
       टीडीआर एका भूखंडावरून दुसऱ्या भूखंडावर विकास क्षमता हस्तांतरित करण्याची अनुमती देते.
       
       - प्रादेशिक गुणकानुसार प्रभावी एफएसआय वाढवते
       - टीडीआर खर्च रेडी रेकनर दराच्या टक्केवारीनुसार गणना केली जाते
       - वेगवेगळ्या प्रदेशांमध्ये वेगवेगळे टीडीआर गुणक आणि दर आहेत
       - टीडीआर बांधकामयोग्य क्षेत्र लक्षणीयरित्या वाढवू शकतो आणि बहुतेकदा प्रीमियम एफएसआयपेक्षा अधिक किफायतशीर असतो
       
    4. **जीएसटी आणि मुद्रांक शुल्क विचार**
       - **बिल्डर पुनर्विकासासाठी**: 
         - जीएसटी: बांधकाम खर्चावर 5%
         - मुद्रांक शुल्क: करारनाम्याच्या मूल्याचे 5-6% (प्रदेशानुसार वेगवेगळे)
       - **स्वयं पुनर्विकासासाठी**:
         - जीएसटी: 0% (सेवा प्रदाता सहभागी नाही)
         - मुद्रांक शुल्क: प्रति युनिट ₹1,000 फ्लॅट
    
    5. **रेडी रेकनर दर**
       - नोंदणी आणि मुद्रांक नियंत्रकांच्या महानिरीक्षकाद्वारे वार्षिक प्रकाशित
       - भागानुसार आणि रस्त्यानुसार बदलते
       - मालमत्ता व्यवहारांसाठी किमान मूल्य दर्शवते
       
    6. **फंजिबल एफएसआय फॅक्टर**
       - मुंबई: 0.35 (35% रेडी रेकनर दराचे)
       - नवी मुंबई: 0.33 (33% रेडी रेकनर दराचे)
       - ठाणे: 0.30 (30% रेडी रेकनर दराचे)
       - पुणे: 0.28 (28% रेडी रेकनर दराचे)
       - नागपूर: 0.25 (25% रेडी रेकनर दराचे)
       - नाशिक: 0.26 (26% रेडी रेकनर दराचे)
    """)
