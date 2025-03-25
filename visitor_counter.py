import streamlit as st
import pyrebase

def initialize_firebase():
    """Initialize Firebase with your project config."""
    firebase_config = {
        "apiKey": st.secrets["firebase"]["apiKey"],
        "authDomain": st.secrets["firebase"]["authDomain"],
        "databaseURL": st.secrets["firebase"]["databaseURL"],
        "projectId": st.secrets["firebase"]["projectId"],
        "storageBucket": st.secrets["firebase"]["storageBucket"],
        "messagingSenderId": st.secrets["firebase"]["messagingSenderId"],
        "appId": st.secrets["firebase"]["appId"]
    }
    firebase = pyrebase.initialize_app(firebase_config)
    return firebase.database()

def get_visitor_count(db):
    """Get the current visitor count."""
    visitor_ref = db.child("visitor_count").get()
    if visitor_ref.val() is not None:
        return visitor_ref.val()
    else:
        return 0

def increment_visitor_count(db):
    """Increment the visitor count and return the new count."""
    current_count = get_visitor_count(db)
    new_count = current_count + 1
    db.child("visitor_count").set(new_count)
    return new_count

def display_visitor_counter():
    """Display the visitor counter in the app."""
    # Only initialize Firebase once per session
    if 'firebase_db' not in st.session_state:
        st.session_state.firebase_db = initialize_firebase()
    
    # Only count the visit once per session
    if 'visitor_counted' not in st.session_state:
        visitor_count = increment_visitor_count(st.session_state.firebase_db)
        st.session_state.visitor_counted = True
        st.session_state.visitor_count = visitor_count
    else:
        visitor_count = st.session_state.visitor_count
    
    # Display the visitor count
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"👥 **Total Visitors**: {visitor_count}")
