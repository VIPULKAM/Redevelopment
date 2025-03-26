import streamlit as st
import requests
import json

def get_and_increment_visitor_count():
    """Get and increment visitor count using Firebase REST API."""
    try:
        # Firebase REST API endpoint for the visitor count
        url = "https://redevelopment-calculator-default-rtdb.firebaseio.com/visitor_count.json"
        
        # Get current count
        response = requests.get(url)
        current_count = 0
        if response.status_code == 200:
            current_count = response.json() or 0
        
        # Increment count
        new_count = current_count + 1
        requests.put(url, data=json.dumps(new_count))
        
        return new_count
    except Exception as e:
        print(f"Error updating visitor count: {e}")
        return None

def display_visitor_counter():
    """Display the visitor counter in the app."""
    # Only count the visit once per session
    if 'visitor_counted' not in st.session_state:
        visitor_count = get_and_increment_visitor_count()
        st.session_state.visitor_counted = True
        st.session_state.visitor_count = visitor_count
    else:
        visitor_count = st.session_state.visitor_count
    
    # Display the visitor count with some styling
    st.sidebar.markdown("---")
    if visitor_count is not None:
        st.sidebar.markdown(f"👥 **Total Visitors**: {visitor_count}")
    else:
        st.sidebar.markdown("👥 **Visitor Counter Unavailable**")
