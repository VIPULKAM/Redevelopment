import streamlit as st
import requests
import json
import time
from datetime import datetime, timedelta
import pytz
from collections import Counter

def get_visitor_data():
    """Get visitor data from Firebase."""
    try:
        # Firebase REST API endpoint for visitor data
        url = "https://redevelopment-calculator-default-rtdb.firebaseio.com/visitors.json"
        
        # Get current data
        response = requests.get(url)
        if response.status_code == 200:
            return response.json() or {}
        return {}
    except Exception as e:
        st.sidebar.error(f"Error getting visitor data: {e}")
        return {}

def get_visitor_count():
    """Get current visitor count from Firebase."""
    try:
        # Firebase REST API endpoint for the visitor count
        url = "https://redevelopment-calculator-default-rtdb.firebaseio.com/visitor_count.json"
        
        # Get current count
        response = requests.get(url)
        if response.status_code == 200:
            return response.json() or 0
        return 0
    except Exception as e:
        st.sidebar.error(f"Error getting visitor count: {e}")
        return 0

def get_visitor_location():
    """Get visitor's location based on IP address."""
    try:
        # Use a free IP geolocation API
        response = requests.get("https://ipapi.co/json/", timeout=2)
        if response.status_code == 200:
            data = response.json()
            return {
                'country': data.get('country_name', 'Unknown'),
                'region': data.get('region', 'Unknown'),
                'city': data.get('city', 'Unknown'),
                'latitude': data.get('latitude'),
                'longitude': data.get('longitude')
            }
    except Exception as e:
        # Silently fail and return default values
        pass
    
    # Default return if API failed
    return {
        'country': 'Unknown',
        'region': 'Unknown',
        'city': 'Unknown',
        'latitude': None,
        'longitude': None
    }

def store_visit_with_metadata(metadata):
    """Store visit with metadata using Firebase REST API."""
    try:
        # Firebase REST API endpoint for visitor data
        visitors_url = "https://redevelopment-calculator-default-rtdb.firebaseio.com/visitors.json"
        count_url = "https://redevelopment-calculator-default-rtdb.firebaseio.com/visitor_count.json"
        
        # Get current visitor data
        visitor_data = get_visitor_data()
        
        # Create a timestamp-based key
        timestamp = int(time.time())
        key = f"{timestamp}"
        
        # Update the visitor data
        visitor_data[key] = metadata
        
        # Get and increment the count
        current_count = get_visitor_count()
        new_count = current_count + 1
        
        # Store the updated count
        requests.put(count_url, data=json.dumps(new_count))
        
        # Store the detailed visitor data
        requests.put(visitors_url, data=json.dumps(visitor_data))
        
        return new_count
    except Exception as e:
        st.sidebar.error(f"Error updating visitor data: {e}")
        return get_visitor_count()  # Return the current count as fallback

def get_visitor_metadata():
    """Collect metadata about the current visitor."""
    # Get the current time in UTC
    now_utc = datetime.now(pytz.UTC)
    
    # Create a session ID if not already created
    if 'session_id' not in st.session_state:
        session_hash = str(hash(str(now_utc)))[:8]
        st.session_state['session_id'] = session_hash
    
    # Get location data if not already cached in this session
    if 'location_data' not in st.session_state:
        location = get_visitor_location()
        st.session_state['location_data'] = location
    else:
        location = st.session_state['location_data']
    
    # Create a metadata object - directly include location fields rather than nesting
    metadata = {
        'timestamp': now_utc.isoformat(),
        'session_id': st.session_state['session_id'],
        'visit_count': st.session_state.get('visit_count', 1),
        'country': location['country'],
        'region': location['region'],
        'city': location['city'],
        'latitude': location['latitude'],
        'longitude': location['longitude']
    }
    
    # Increment visit count for this session
    st.session_state['visit_count'] = st.session_state.get('visit_count', 1) + 1
    
    return metadata

def is_suspicious_timing(time_diffs, threshold=0.1):
    """
    Detect if a series of time differences has suspiciously consistent intervals.
    Returns True if the coefficient of variation is below the threshold.
    """
    if not time_diffs or len(time_diffs) < 3:
        return False
    
    mean = sum(time_diffs) / len(time_diffs)
    if mean <= 0:
        return False
    
    variance = sum((x - mean) ** 2 for x in time_diffs) / len(time_diffs)
    std_dev = variance ** 0.5
    
    # Coefficient of variation (lower means more consistent)
    cv = std_dev / mean
    
    return cv < threshold

def analyze_visit_patterns():
    """Analyze visitor patterns to detect bot-like behavior."""
    # Force fresh data fetch
    visitor_data = get_visitor_data()
    
    if not visitor_data:
        st.warning("No visitor data available for analysis.")
        return
    
    # Convert to a list of visit records
    visits = []
    for key, metadata in visitor_data.items():
        try:
            # Skip entries that don't have proper metadata
            if not isinstance(metadata, dict) or 'timestamp' not in metadata:
                continue
                
            # Parse the timestamp
            visit_time = datetime.fromisoformat(metadata['timestamp'].replace('Z', '+00:00'))
            
            # Extract session ID and location - handle both direct fields and nested location
            session_id = metadata.get('session_id', 'unknown')
            
            # Check for location information in the metadata
            # First try direct fields (new format)
            country = metadata.get('country', 'Unknown')
            region = metadata.get('region', 'Unknown')
            city = metadata.get('city', 'Unknown')
            
            # If not found, check for nested 'location' object (old format)
            if country == 'Unknown' and 'location' in metadata and isinstance(metadata['location'], dict):
                country = metadata['location'].get('country', 'Unknown')
                region = metadata['location'].get('region', 'Unknown')
                city = metadata['location'].get('city', 'Unknown')
            
            visits.append({
                'key': key,
                'timestamp': visit_time,
                'session_id': session_id,
                'country': country,
                'region': region,
                'city': city
            })
        except Exception as e:
            st.error(f"Error parsing visit data for key {key}: {str(e)}")
    
    if not visits:
        st.warning("No valid visit data found for analysis.")
        return
    
    # Sort visits by timestamp
    visits.sort(key=lambda x: x['timestamp'])
    
    # Group visits by session ID
    sessions = {}
    for visit in visits:
        session_id = visit['session_id']
        if session_id not in sessions:
            sessions[session_id] = []
        sessions[session_id].append(visit)
    
    # Analyze time patterns per session
    session_analysis = {}
    for session_id, session_visits in sessions.items():
        if len(session_visits) < 2:
            continue
            
        # Calculate time differences between consecutive visits
        time_diffs = []
        for i in range(1, len(session_visits)):
            diff_seconds = (session_visits[i]['timestamp'] - session_visits[i-1]['timestamp']).total_seconds()
            time_diffs.append(diff_seconds)
        
        # Check for suspicious timing
        suspicious_timing = is_suspicious_timing(time_diffs)
        
        # Store analysis results
        session_analysis[session_id] = {
            'visits': session_visits,
            'time_diffs': time_diffs,
            'suspicious_timing': suspicious_timing,
            'avg_diff': sum(time_diffs) / len(time_diffs) if time_diffs else 0,
            'visit_count': len(session_visits),
            'first_visit': session_visits[0]['timestamp'],
            'last_visit': session_visits[-1]['timestamp'],
            'country': session_visits[0]['country'],
            'region': session_visits[0]['region'],
            'city': session_visits[0]['city']
        }
    
    # Get timestamps for recent visits
    now = datetime.now(pytz.UTC)
    recent_visits = []
    for visit in visits:
        # Check if the visit is within the last hour
        if (now - visit['timestamp']).total_seconds() < 3600:
            recent_visits.append(visit)
    
    # Display the analysis results
    st.subheader("Visit Pattern Analysis")
    st.write(f"Last updated: {now.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    
    # Debug information - this can help identify issues
    st.write("**Debug Information:**")
    st.write(f"""
    - Total visits in database: {len(visitor_data)}
    - Valid visits processed: {len(visits)}
    - Visits with known country: {sum(1 for v in visits if v['country'] != 'Unknown')}
    - Visits with unknown country: {sum(1 for v in visits if v['country'] == 'Unknown')}
    """)
    
    # Recent activity
    st.subheader("Recent Activity (Last Hour)")
    if recent_visits:
        st.write(f"Found {len(recent_visits)} visits in the last hour")
        
        # Group by session
        recent_sessions = {}
        for visit in recent_visits:
            if visit['session_id'] not in recent_sessions:
                recent_sessions[visit['session_id']] = []
            recent_sessions[visit['session_id']].append(visit)
        
        st.write(f"From {len(recent_sessions)} unique sessions")
        
        # Check for suspicious patterns in recent visits
        suspicious_recent = False
        for session_id, session_visits in recent_sessions.items():
            if len(session_visits) >= 3:
                time_diffs = []
                for i in range(1, len(session_visits)):
                    diff = (session_visits[i]['timestamp'] - session_visits[i-1]['timestamp']).total_seconds()
                    time_diffs.append(diff)
                
                if is_suspicious_timing(time_diffs):
                    suspicious_recent = True
                    break
        
        if suspicious_recent:
            st.warning("⚠️ **Suspicious activity detected in the last hour!**")
        else:
            st.success("✅ Recent activity appears normal")
    else:
        st.write("No visits in the last hour")
    
    # Geographic analysis
    st.subheader("Geographic Distribution")
    
    # Count visits by country and region
    country_counts = Counter()
    region_counts = Counter()
    
    for visit in visits:
        if visit['country'] != 'Unknown':
            country_counts[visit['country']] += 1
            
            if visit['region'] != 'Unknown':
                region_counts[f"{visit['region']}, {visit['country']}"] += 1
    
    # Display countries
    if country_counts:
        st.write("**Top Countries:**")
        for country, count in country_counts.most_common(10):
            st.write(f"🌎 {country}: {count} visits ({round(count/len(visits)*100, 1)}%)")
    else:
        st.write("**No country data available**")
    
    # Display regions
    if region_counts:
        st.write("**Top Regions:**")
        for region, count in region_counts.most_common(10):
            st.write(f"📍 {region}: {count} visits")
    else:
        st.write("**No region data available**")
    
    # Summary statistics
    st.subheader("Overall Statistics")
    total_visits = len(visits)
    unique_sessions = len(sessions)
    bot_sessions = sum(1 for s in session_analysis.values() if s['suspicious_timing'])
    human_sessions = unique_sessions - bot_sessions
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Visits", total_visits)
    col2.metric("Unique Sessions", unique_sessions)
    col3.metric("Likely Human Sessions", human_sessions)
    col4.metric("Suspicious Sessions", bot_sessions)
    
    # Time pattern analysis
    st.subheader("Session Analysis")
    
    # Sort sessions by suspiciousness
    sorted_sessions = sorted(
        session_analysis.items(), 
        key=lambda x: (x[1]['suspicious_timing'], -x[1]['visit_count']),
        reverse=True
    )
    
    # Display session analysis
    for session_id, analysis in sorted_sessions:
        # Determine status icon
        if analysis['suspicious_timing']:
            icon = "🤖"
            status = "Suspicious"
        else:
            icon = "👤"
            status = "Normal"
        
        # Get location info
        location_str = ""
        if analysis['city'] != 'Unknown' and analysis['country'] != 'Unknown':
            location_str = f" from {analysis['city']}, {analysis['country']}"
        elif analysis['country'] != 'Unknown':
            location_str = f" from {analysis['country']}"
        
        # Create an expander for this session
        with st.expander(f"{icon} Session {session_id} - {status}{location_str} ({analysis['visit_count']} visits)"):
            # Session details
            st.write(f"**First visit:** {analysis['first_visit'].strftime('%Y-%m-%d %H:%M:%S UTC')}")
            st.write(f"**Last visit:** {analysis['last_visit'].strftime('%Y-%m-%d %H:%M:%S UTC')}")
            
            # Location details
            if analysis['country'] != 'Unknown':
                st.write(f"**Location:** {analysis['city']}, {analysis['region']}, {analysis['country']}")
            
            # Timing analysis
            if analysis['time_diffs']:
                st.write(f"**Average time between visits:** {round(analysis['avg_diff'], 2)} seconds")
                
                if analysis['suspicious_timing']:
                    st.warning("⚠️ **Suspiciously consistent timing detected!** This is a strong indicator of automated traffic.")
                    
                    # Display the consistent intervals
                    intervals = [round(td, 2) for td in analysis['time_diffs']]
                    st.write(f"Time intervals (seconds): {intervals}")
            
            # Visit details
            st.subheader("Individual Visits")
            for i, visit in enumerate(analysis['visits']):
                time_str = visit['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
                
                if i > 0:
                    time_diff = (visit['timestamp'] - analysis['visits'][i-1]['timestamp']).total_seconds()
                    st.write(f"{i+1}. {time_str} - Time since last: {round(time_diff, 2)}s")
                else:
                    st.write(f"{i+1}. {time_str}")
    
    # Time of day analysis
    st.subheader("Visit Time Analysis")
    
    # Create histogram of visit times by hour
    visit_hours = [v['timestamp'].hour for v in visits]
    hour_counts = Counter(visit_hours)
    
    # Prepare data for chart
    hours = list(range(24))
    counts = [hour_counts.get(hour, 0) for hour in hours]
    
    # Create a simple bar chart
    st.bar_chart({"Visits by Hour (UTC)": counts})
    
    # Check for suspicious hours with many visits
    suspicious_hours = []
    for hour, count in hour_counts.items():
        if count > total_visits * 0.2 and count > 10:  # If more than 20% of visits are in one hour and at least 10 visits
            suspicious_hours.append((hour, count))
    
    if suspicious_hours:
        st.subheader("Potential Automated Traffic Hours")
        for hour, count in sorted(suspicious_hours, key=lambda x: x[1], reverse=True):
            st.write(f"⚠️ Hour {hour}:00 UTC has {count} visits ({round(count/total_visits*100, 1)}% of all traffic)")

def display_visitor_counter():
    """Display the visitor counter in the app with analytics capabilities."""
    # Only count the visit once per session
    if 'visitor_counted' not in st.session_state:
        metadata = get_visitor_metadata()
        visitor_count = store_visit_with_metadata(metadata)
        st.session_state.visitor_counted = True
        st.session_state.visitor_count = visitor_count
    else:
        visitor_count = st.session_state.visitor_count
    
    # Display the visitor count with some styling
    st.sidebar.markdown("---")
    if visitor_count is not None:
        st.sidebar.markdown(f"👥 **Total Visitors**: {visitor_count}")
        
        # Add an admin toggle
        with st.sidebar.expander("Admin Analytics", expanded=False):
            admin_password = st.text_input("Password", type="password", key="admin_password")
            
            if admin_password == "analyzeme":  # Simple password protection
                # Manual refresh button - prominently displayed
                if st.button("🔄 Refresh Analytics Data", use_container_width=True):
                    # Force a refresh by clearing any cached data
                    st.rerun()
                
                # Reset session button - secondary action
                if st.button("Reset Session", use_container_width=True):
                    for key in list(st.session_state.keys()):
                        if key.startswith('visitor_') or key == 'session_id' or key == 'location_data':
                            del st.session_state[key]
                    st.rerun()
                
                # Show the current time
                current_time = datetime.now()
                st.write(f"Current time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Info about manual refresh
                st.info("📊 Analytics are not automatically refreshed. Use the 'Refresh Analytics Data' button to see the latest data.")
                
                # Always show the analysis when admin is logged in
                analyze_visit_patterns()
    else:
        st.sidebar.markdown("👥 **Visitor Counter Unavailable**")
