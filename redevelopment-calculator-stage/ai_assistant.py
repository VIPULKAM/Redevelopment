# File: ai_assistant.py
import streamlit as st
import google.generativeai as genai
import os
import json
from dotenv import load_dotenv
import datetime
import logging
from config import REGION_CONFIG, TDR_CONFIG, ROAD_WIDTH_FSI_RULES, READY_RECKONER_RATES

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Configure Google Generative AI with API key
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    logger.info("Gemini API configured successfully")
else:
    logger.warning("No Gemini API key found. AI Assistant will be unavailable.")

# Expert system prompt with detailed redevelopment knowledge
SYSTEM_PROMPT = """You are an expert assistant specialized in Maharashtra redevelopment projects, with deep knowledge of DCR 2034 and regional variations.

Important concepts you understand in detail:
1. FSI (Floor Space Index): Ratio of total built-up area to plot area, varies by region and road width
   - Mumbai: Ranges from 1.0-3.0 for residential and 1.5-5.0 for commercial based on road width
   - Thane: 3.0 for residential, 4.0 for commercial
   - Pune: 1.75 for residential, 3.0 for commercial

2. TDR (Transfer of Development Rights): Additional development rights that can be purchased
   - Types in Mumbai: Road TDR, Reservation TDR, Slum TDR, Heritage TDR
   - Each type has different multipliers and loading factors
   - Regional TDR multipliers: Mumbai (2.5x), Thane/Navi Mumbai (2.0x), Pune (1.8x)

3. Premium FSI components:
   - Fungible FSI (Mumbai): 35% for residential, 20% for commercial
   - Ancillary FSI (other regions): Various percentages with different cost factors

4. Redevelopment bonuses:
   - Green building bonus: 5-7% of buildable area
   - Self-redevelopment bonus: 10-15% depending on region

5. Financial considerations:
   - Premium calculations based on Ready Reckoner rates
   - GST implications (5% for builder redevelopment)
   - Stamp duty differences between self and builder redevelopment
   - Per-member profit calculations
   - Construction cost variations by region

Provide concise, accurate answers about redevelopment projects. Use specific examples and numbers when helpful.
If you're unsure about something, acknowledge it rather than providing potentially incorrect information.
"""

# Cache the model to prevent reloading
@st.cache_resource
def get_gemini_model():
    """Initialize and cache the Gemini model with expert system prompt."""
    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            system_instruction=SYSTEM_PROMPT,
            generation_config={
                "temperature": 0.2,
                "top_p": 0.8,
                "top_k": 40,
                "max_output_tokens": 1000,
            }
        )
        logger.info("Gemini model initialized successfully")
        return model
    except Exception as e:
        logger.error(f"Error initializing Gemini model: {str(e)}")
        return None

# Knowledge retrieval system for Maharashtra redevelopment
class RedevelopmentKnowledgeBase:
    """Knowledge base for Maharashtra redevelopment regulations and calculations."""
    
    def __init__(self):
        """Initialize the knowledge base with configuration data."""
        self.region_config = REGION_CONFIG
        self.tdr_config = TDR_CONFIG
        self.road_width_rules = ROAD_WIDTH_FSI_RULES
        self.rr_rates = READY_RECKONER_RATES
        logger.info("Redevelopment knowledge base initialized")
    
    def get_knowledge_for_query(self, query):
        """Extract relevant knowledge based on query keywords."""
        query = query.lower()
        knowledge_sections = []
        
        # Map keywords to knowledge retrieval functions
        keyword_map = {
            'fsi': self._get_fsi_knowledge,
            'floor space': self._get_fsi_knowledge,
            'tdr': self._get_tdr_knowledge,
            'transfer': self._get_tdr_knowledge,
            'premium': self._get_premium_knowledge,
            'fungible': self._get_fungible_knowledge,
            'ancillary': self._get_ancillary_knowledge,
            'road width': self._get_road_width_knowledge,
            'self': self._get_redevelopment_type_knowledge,
            'builder': self._get_redevelopment_type_knowledge,
            'profit': self._get_financial_knowledge,
            'cost': self._get_financial_knowledge,
            'rr rate': self._get_ready_reckoner_knowledge,
            'ready reckoner': self._get_ready_reckoner_knowledge,
            'gst': self._get_taxation_knowledge,
            'stamp duty': self._get_taxation_knowledge,
            'bonus': self._get_bonus_knowledge,
            'green': self._get_bonus_knowledge,
            'carpet area': self._get_area_calculation_knowledge,
            'buildable': self._get_area_calculation_knowledge,
            'regulation': self._get_dcr_knowledge,
            'dcr': self._get_dcr_knowledge,
        }
        
        # Check for region-specific queries
        regions = ['mumbai', 'thane', 'pune', 'navi mumbai', 'nagpur', 'nashik']
        query_regions = [region for region in regions if region in query]
        
        # Collect relevant knowledge based on keywords
        for keyword, knowledge_fn in keyword_map.items():
            if keyword in query:
                knowledge = knowledge_fn(query_regions[0] if query_regions else None)
                if knowledge:
                    knowledge_sections.append(knowledge)
        
        # If no specific knowledge found, provide general overview
        if not knowledge_sections:
            knowledge_sections.append(self._get_general_knowledge())
        
        return "\n\n".join(knowledge_sections)
    
    def _get_fsi_knowledge(self, region=None):
        """Provide knowledge about FSI regulations."""
        if region:
            region = region.title()
            if region == "Mumbai":
                return f"""
FSI in Mumbai:
- Base FSI varies based on road width:
  * Roads < 9m: 1.0 for residential, 1.5 for commercial
  * Roads 9-12m: 1.33 for residential, 2.0 for commercial
  * Roads 12-18m: 2.5 for residential, 3.0 for commercial
  * Roads > 18m: 3.0 for residential, 5.0 for commercial
- Additional 35% fungible FSI available for residential projects (premium payable)
- Additional 20% fungible FSI available for commercial projects (premium payable)
- TDR multiplier: 2.5x
"""
            else:
                config = self.region_config.get(region, {})
                return f"""
FSI in {region}:
- Base FSI: {config.get('fsi_rules', {}).get('residential', 'N/A')} for residential projects
- Base FSI: {config.get('fsi_rules', {}).get('commercial', 'N/A')} for commercial projects
- {"Fungible FSI available" if config.get('has_fungible', False) else "Ancillary FSI available instead of Fungible"}
- TDR multiplier: {config.get('fsi_rules', {}).get('tdr_multiplier', 'N/A')}x
"""
        else:
            return """
FSI (Floor Space Index) in Maharashtra:
- Varies by region, road width, and project type (residential/commercial)
- Higher FSI allowed for wider roads in Mumbai
- Additional components: Base FSI + TDR + Fungible/Ancillary FSI
- Self-redevelopment and green building bonuses can further increase buildable area
- Mumbai has road width-based FSI rules, other regions have fixed base FSI
"""
    
    def _get_tdr_knowledge(self, region=None):
        """Provide knowledge about TDR regulations."""
        if region == "mumbai":
            tdr_types = self.tdr_config.get("Mumbai", {}).get("types", {})
            types_info = "\n".join([f"  * {tdr_type}: {info.get('description', '')} (FSI multiplier: {info.get('fsi_multiplier', 'N/A')}x, Cost factor: {info.get('cost_factor', 'N/A')}x)" 
                                  for tdr_type, info in tdr_types.items()])
            return f"""
TDR in Mumbai:
- Types available:
{types_info}
- TDR Loading factors: 0.8x in Island City, 1.0x in suburbs
- Current TDR market rate range: ₹{self.tdr_config.get("Mumbai", {}).get("min_rate", 'N/A')}-{self.tdr_config.get("Mumbai", {}).get("max_rate", 'N/A')} per sqft
"""
        else:
            return """
Transfer of Development Rights (TDR):
- Additional FSI that can be purchased and utilized on a receiving plot
- Generated from road widening, slum rehabilitation, or heritage conservation
- Different types have different loading factors and usage restrictions
- TDR contribution to FSI = TDR percentage × Loading factor
- Each region has specific TDR multipliers:
  * Mumbai: 2.5x
  * Thane/Navi Mumbai: 2.0x
  * Pune: 1.8x
  * Nagpur/Nashik: 1.5-1.6x
- TDR cost is calculated based on Ready Reckoner rate or current market rates
"""
    
    def _get_premium_knowledge(self, region=None):
        """Provide knowledge about premium payments."""
        return """
Premium Payments for Additional FSI:
- In Mumbai, premium is paid for Fungible FSI:
  * 40% of Ready Reckoner rate for residential projects
  * 50% of Ready Reckoner rate for commercial projects
- In other regions, premium is paid for Ancillary FSI:
  * Typically 40% of Ready Reckoner rate
- Premium calculation formula: Land Area × Ready Reckoner Rate × FSI Factor × Premium Percentage
- Premium costs are a significant component of total project cost
"""
    
    def _get_fungible_knowledge(self, region=None):
        """Provide knowledge about fungible FSI."""
        return """
Fungible FSI (Mumbai-specific):
- Additional FSI component available in Mumbai only
- 35% of base FSI for residential projects
- 20% of base FSI for commercial projects
- Premium payable: 40-50% of Ready Reckoner rate
- Not counted against TDR loading limits
- Primarily designed to account for areas like flowerbeds, balconies, etc.
- Formula: Fungible Area Factor = Base FSI × Fungible FSI Percentage
"""
    
    def _get_ancillary_knowledge(self, region=None):
        """Provide knowledge about ancillary FSI."""
        return """
Ancillary FSI (Non-Mumbai regions):
- Alternative to Mumbai's Fungible FSI in other Maharashtra regions
- Typically ranges from 40-60% of base FSI
- Premium payable: ~40% of Ready Reckoner rate
- Used for similar purposes as Fungible FSI
- Enhances buildable potential of the project
- Formula: Ancillary Area Factor = Base FSI × Ancillary FSI Percentage
"""
    
    def _get_road_width_knowledge(self, region=None):
        """Provide knowledge about road width rules."""
        if region == "mumbai":
            residential_rules = "\n".join([f"  * {min_w}-{max_w if max_w != float('inf') else 'above'}m: {fsi} FSI" 
                                         for (min_w, max_w), fsi in self.road_width_rules["Mumbai"]["residential"].items()])
            commercial_rules = "\n".join([f"  * {min_w}-{max_w if max_w != float('inf') else 'above'}m: {fsi} FSI" 
                                         for (min_w, max_w), fsi in self.road_width_rules["Mumbai"]["commercial"].items()])
            return f"""
Road Width FSI Rules in Mumbai:
- Residential:
{residential_rules}
- Commercial:
{commercial_rules}
- Wider roads allow higher FSI utilization
- Road width is measured from the property boundary
"""
        else:
            return """
Road Width Considerations:
- In Mumbai, FSI varies based on the width of the road abutting the property
- Wider roads allow for higher FSI utilization
- Road width also affects setback requirements
- For TDR utilization, usually a minimum road width is required
- Road width rules do not apply in the same way outside Mumbai
"""
    
    def _get_redevelopment_type_knowledge(self, region=None):
        """Provide knowledge about redevelopment types."""
        return """
Redevelopment Types Comparison:

Self-Redevelopment:
- Society manages the project directly
- Additional FSI bonus: 10-15% depending on region
- No GST on construction (significant saving)
- Stamp duty: Fixed fee per member (₹1000)
- Society retains 100% of profits
- Requires expertise and management capability
- Higher risk for society members

Builder Redevelopment:
- Professional developer manages the project
- No self-redevelopment bonus
- 5% GST applicable on construction
- Stamp duty: ~6% of property value
- Builder typically takes 100% of the profit
- Lower risk for society members
- Builder handles approvals and construction
"""
    
    def _get_financial_knowledge(self, region=None):
        """Provide knowledge about financial aspects."""
        return """
Financial Aspects of Redevelopment:

Cost Components:
- Premium costs for additional FSI
- TDR purchase costs
- Construction costs (varies by region and quality)
- GST (5% for builder redevelopment)
- Stamp duty
- Rent payment during construction
- Relocation costs
- Bank interest on loans

Revenue:
- Sale of additional constructed area (builder sellable area)
- Market rates vary significantly by location

Profit Calculation:
- Total Profit = Project Value - Total Costs
- Society Profit (Self-redevelopment) = Total Profit
- Per-member Profit = Society Profit / Number of Members
"""
    
    def _get_ready_reckoner_knowledge(self, region=None):
        """Provide knowledge about ready reckoner rates."""
        rates_info = "\n".join([f"  * {r}: ₹{self.rr_rates.get(r, {}).get(2024, 'N/A')}/sqm (2024)" for r in self.rr_rates.keys()])
        return f"""
Ready Reckoner Rates:
- Government-determined land value used for premium calculations
- Updated annually by the government
- Varies significantly by region:
{rates_info}
- Used as the basis for premium FSI costs, TDR calculations
- Higher RR rates lead to higher premium payments
"""
    
    def _get_taxation_knowledge(self, region=None):
        """Provide knowledge about taxation aspects."""
        return """
Taxation in Redevelopment:

GST (Goods and Services Tax):
- Builder redevelopment: 5% GST on construction cost
- Self-redevelopment: No GST applicable
- Significant impact on total project cost
- Input tax credit may be available to builders

Stamp Duty:
- Builder redevelopment: ~6% of property value for new flats
- Self-redevelopment: Fixed fee per member (₹1000)
- Major cost saving advantage for self-redevelopment
- Varies slightly by region within Maharashtra
"""
    
    def _get_bonus_knowledge(self, region=None):
        """Provide knowledge about bonus FSI."""
        bonuses = {region: config.get('bonuses', {}) for region, config in self.region_config.items()}
        bonus_info = "\n".join([f"  * {r}: Green building {b.get('green_building', 'N/A') * 100}%, Self-redevelopment {b.get('self_redev', 'N/A') * 100}%" 
                              for r, b in bonuses.items()])
        return f"""
Bonus FSI Components:

By Region:
{bonus_info}

Green Building Bonus:
- Awarded for implementing green building features
- Ranges from 5-7% of buildable area
- No premium payable
- Requires certification or specific sustainable features

Self-Redevelopment Bonus:
- Only applicable in self-redevelopment projects
- Ranges from 10-15% depending on region
- Incentive for societies to undertake redevelopment themselves
- No premium payable
"""
    
    def _get_area_calculation_knowledge(self, region=None):
        """Provide knowledge about area calculations."""
        return """
Area Calculation Concepts:

Carpet Area:
- Actual usable floor area within walls
- Typically 65-70% of built-up area
- What residents actually receive and use

Built-up Area:
- Carpet area + wall thickness
- Approximately 10-15% more than carpet area

Super Built-up Area:
- Built-up area + proportionate common areas
- Typically 25-30% more than carpet area
- Often used for marketing purposes

Calculation Flow:
1. Land Area × Total Effective FSI = Total Buildable Area
2. Add bonuses (green building, self-redevelopment)
3. Deduct society member entitlement area
4. Remainder is builder sellable area
"""
    
    def _get_dcr_knowledge(self, region=None):
        """Provide knowledge about DCR regulations."""
        return """
Development Control Regulations (DCR):

DCR 2034 (Mumbai):
- Latest comprehensive regulation for Mumbai
- Defines FSI limits, TDR usage, road width rules
- Includes provisions for fungible FSI

Key DCR Components:
- FSI limitations by zone and road width
- Setback requirements
- Parking provisions
- Open space requirements
- TDR utilization guidelines
- Premium FSI regulations
- Height restrictions and fire safety norms
- Special provisions for redevelopment of old buildings

Regional DCRs:
- Each municipal corporation has its own DCR
- Rules vary by region but follow similar principles
- Regular amendments update specific provisions
"""
    
    def _get_general_knowledge(self):
        """Provide general knowledge about redevelopment."""
        return """
Maharashtra Redevelopment Overview:

Key Components:
1. FSI (Floor Space Index): Determines how much can be built on a plot
2. TDR (Transfer of Development Rights): Additional development rights
3. Premium FSI: Additional FSI available by paying premium
4. Bonuses: Additional incentives for green building, self-redevelopment

Financial Considerations:
- Construction costs vary by region and quality
- Market rates determine sale value of additional area
- Premium costs based on Ready Reckoner rates
- Various bonuses can improve project viability

Redevelopment Process:
1. Society resolution for redevelopment
2. Appointment of PMC/developer
3. Obtaining NOCs and approvals
4. Preparation of plans and FSI calculations
5. Premium and TDR procurement
6. Construction and temporary rehabilitation
7. Completion and occupation
"""

# Initialize the knowledge base
knowledge_base = RedevelopmentKnowledgeBase()

# Chat session manager for Gemini
class GeminiChatManager:
    """Manages chat sessions with Gemini API."""
    
    def __init__(self):
        """Initialize the chat manager."""
        self.model = get_gemini_model()
        self.knowledge_base = knowledge_base
        logger.info("Chat manager initialized")
        
    def get_response(self, user_query, calculator_data=None, chat_history=None):
        """Generate a response using Gemini API with context."""
        if not GOOGLE_API_KEY:
            return "API key not configured. Please add your Gemini API key to the .env file."
        
        if not self.model:
            return "Unable to initialize Gemini model. Please check your API key and connection."
        
        try:
            # Get relevant knowledge
            knowledge = self.knowledge_base.get_knowledge_for_query(user_query)
            
            # Format calculator data if available
            calculator_context = self._format_calculator_data(calculator_data) if calculator_data else ""
            
            # Format chat history if available
            history_context = self._format_chat_history(chat_history) if chat_history else ""
            
            # Combine all context elements
            full_context = f"""
{calculator_context}

{knowledge}

{history_context}
"""
            # Combine context and query
            prompt = f"{full_context}\n\nUser question: {user_query}"
            
            # Log the length of the prompt for debugging
            logger.info(f"Prompt length: {len(prompt)} characters")
            
            # Generate response
            response = self.model.generate_content(prompt)
            
            # Save the successful interaction
            self._log_interaction(user_query, response.text)
            
            return response.text
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return f"Error generating response: {str(e)}"
    
    def _format_calculator_data(self, data):
        """Format calculator data for context."""
        if not data:
            return ""
        
        # Focus on the most relevant data for context
        key_params = [
            'region', 'project_type', 'is_self_redevelopment', 
            'land_area', 'road_width', 'base_fsi', 'effective_fsi',
            'total_effective_fsi', 'tdr_percentage', 'tdr_type',
            'fungible_fsi', 'ancillary_fsi',
            'total_profit', 'per_member_profit', 'market_rate_per_sqft',
            'construction_cost_per_sqft', 'total_cost', 'project_value',
            'num_salable_flats'
        ]
        
        formatted_data = "Current calculator data:\n"
        for key in key_params:
            if key in data and data[key] is not None:
                value = data[key]
                # Format boolean values
                if isinstance(value, bool):
                    value = "Yes" if value else "No"
                # Format project type
                elif key == 'project_type' and isinstance(value, str):
                    value = value.title()
                # Format numeric values
                elif isinstance(value, (int, float)):
                    if key in ['total_profit', 'per_member_profit', 'market_rate_per_sqft', 
                              'construction_cost_per_sqft', 'total_cost', 'project_value']:
                        value = f"₹{value:,.2f}"
                    elif key in ['base_fsi', 'effective_fsi', 'total_effective_fsi', 
                                'fungible_fsi', 'ancillary_fsi']:
                        value = f"{value:.2f}"
                    elif key == 'tdr_percentage':
                        value = f"{value:.1f}%"
                    else:
                        value = f"{value:,}"
                
                # Format key for display
                display_key = key.replace('_', ' ').title()
                formatted_data += f"- {display_key}: {value}\n"
        
        return formatted_data
    
    def _format_chat_history(self, history, max_entries=3):
        """Format recent chat history for context."""
        if not history or len(history) < 2:
            return ""
        
        # Only include the most recent exchanges (up to max_entries)
        recent_history = history[-min(len(history), max_entries*2):]
        
        formatted_history = "Recent conversation history:\n"
        for i, msg in enumerate(recent_history):
            role = "User" if msg["role"] == "user" else "Assistant"
            # Truncate very long messages
            content = msg["content"]
            if len(content) > 200:
                content = content[:197] + "..."
            
            formatted_history += f"{role}: {content}\n"
        
        return formatted_history
    
    def _log_interaction(self, query, response):
        """Log successful interactions for analytics."""
        try:
            # Create logs directory if it doesn't exist
            os.makedirs('logs', exist_ok=True)
            
            # Get current date for log file
            current_date = datetime.datetime.now().strftime('%Y-%m-%d')
            log_file = f'logs/gemini_interactions_{current_date}.log'
            
            # Log interaction with timestamp
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"\n[{timestamp}] QUERY: {query}\n")
                f.write(f"[{timestamp}] RESPONSE: {response}\n")
                f.write("-" * 80 + "\n")
        except Exception as e:
            logger.error(f"Error logging interaction: {str(e)}")

# Initialize the chat manager
chat_manager = GeminiChatManager()

# Add assistant tab to main app
def add_ai_assistant_tab():
    """Add AI Assistant tab to the main Streamlit app."""
    st.subheader("AI Assistant for Redevelopment")
    
    # Check if API key is configured
    if not GOOGLE_API_KEY:
        st.error("⚠️ Gemini API key not configured. Please add GEMINI_API_KEY to your .env file.")
        
        with st.expander("How to set up your API key"):
            st.markdown("""
            1. Create a Google AI Studio account at [https://aistudio.google.com/](https://aistudio.google.com/)
            2. Generate an API key
            3. Create a `.env` file in your project directory
            4. Add the following line to your .env file:
            ```
            GEMINI_API_KEY=your_api_key_here
            ```
            5. Restart your Streamlit app
            """)
        return
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Add a welcome message
        st.session_state.messages.append({
            "role": "assistant", 
            "content": "👋 Hi! I'm your Maharashtra Redevelopment Assistant. I can help answer questions about FSI, TDR, premiums, and other redevelopment calculations. What would you like to know?"
        })
    
    # Custom CSS for chat interface
    st.markdown("""
    <style>
    .chat-message {
        padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem;
        display: flex; align-items: center;
    }
    .chat-message.user {
        background-color: #2b313e;
    }
    .chat-message.assistant {
        background-color: #475063;
    }
    .chat-message .avatar {
        width: 20%;
    }
    .chat-message .avatar img {
        max-width: 78px;
        max-height: 78px;
        border-radius: 50%;
        object-fit: cover;
    }
    .chat-message .message {
        width: 80%;
        padding-left: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Get calculator data from session state
    calculator_data = st.session_state.get("params", {})
    results = st.session_state.get("results", {})
    
    # Combine params and results if both are available
    if results:
        calculator_data.update(results)
    
    # Chat input
    if prompt := st.chat_input("Ask about Maharashtra redevelopment..."):
        # Add user message to chat history and display
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chat_manager.get_response(
                    prompt, 
                    calculator_data=calculator_data,
                    chat_history=st.session_state.messages[:-1]  # Exclude the current message
                )
                st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Sidebar for chat options
    with st.sidebar:
        st.subheader("AI Assistant Settings")
        
        # Show example questions that users can click on
        st.markdown("#### Example Questions:")
        example_questions = [
            "What is fungible FSI and how is it calculated?",
            "How does road width affect FSI in Mumbai?",
            "What are the differences between self and builder redevelopment?",
            "How is TDR calculated and what types are available?",
            "What costs are involved in a redevelopment project?",
            "How can I maximize profit in my redevelopment project?",
            "What is the difference between carpet area and built-up area?",
            "Explain the premium calculation for fungible FSI"
        ]
        
        for question in example_questions:
            if st.button(question, key=f"btn_{hash(question)}", use_container_width=True):
                # Add the selected question to chat
                st.session_state.messages.append({"role": "user", "content": question})
                # Force a rerun to process the question
                st.rerun()
        
        # Clear chat history button
        if st.button("Clear Chat History", use_container_width=True):
            clear_chat_history()
            st.rerun()

# Function to clear chat history
def clear_chat_history():
    """Reset the chat history with a welcome message."""
    if "messages" in st.session_state:
        st.session_state.messages = [{
            "role": "assistant", 
            "content": "👋 Hi! I'm your Maharashtra Redevelopment Assistant. I can help answer questions about FSI, TDR, premiums, and other redevelopment calculations. What would you like to know?"
        }]
