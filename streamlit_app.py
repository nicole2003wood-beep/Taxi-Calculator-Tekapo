import streamlit as st

st.title("Taxi Calculator!")

# Initialise session state
if 'journeys' not in st.session_state:
    st.session_state.journeys = [{}]  # Start with one empty journey
if 'total_price' not in st.session_state:
    st.session_state.total_price = 0

st.subheader("Add Journey Details")

for idx, journey in enumerate(st.session_state.journeys):
    st.markdown(f"### Journey {idx + 1}")
    
    km_without = st.number_input("Enter km WITHOUT passengers:", min_value=0.0, key=f"km_without_{idx}")
    km_with = st.number_input("Enter km WITH passengers:", min_value=0.0, key=f"km_with_{idx}")
    
    # Number of passengers
    num_passengers = st.number_input("Enter number of passengers:", min_value=0, key=f"num_passengers_{idx}")
    
    # Hours driver will wait - with hours and minutes
    st.write("Enter time driver will wait")
    col1, col2 = st.columns(2)
    with col1:
        waiting_hours = st.number_input("Hours", min_value=0.0, key=f"waiting_hours_{idx}")
    with col2:
        waiting_mins = st.number_input("Minutes", min_value=0.0, max_value=59.0, key=f"waiting_mins_{idx}")
    hours_waiting = waiting_hours + (waiting_mins / 60)
    
    # Time spent driving - with hours and minutes
    st.write("Enter time spent driving")
    col3, col4 = st.columns(2)
    with col3:
        hours = st.number_input("Hours", min_value=0.0, key=f"hours_{idx}")
    with col4:
        mins = st.number_input("Minutes", min_value=0.0, max_value=59.0, key=f"mins_{idx}")
    hours_total = hours + (mins / 60)
    
    # Store in journey dictionary 
    st.session_state.journeys[idx] = {
        'km_without': km_without,
        'km_with': km_with,
        'num_passengers': num_passengers,
        'hours_waiting': hours_waiting,
        'hours_total': hours_total
    }

# Add journey
if st.button("➕ Add Another Journey", type="primary"):
    st.session_state.journeys.append({})
    st.rerun()

if st.button("🗑️ Reset All", type="secondary"):
    st.session_state.journeys = [{}]
    st.session_state.total_price = 0
    st.rerun()
  
if st.button("💰 Calculate Total", type="primary"):
    # Calculate total from all journeys
    total = 0
    for journey in st.session_state.journeys:
        km_without = journey.get('km_without', 0)
        km_with = journey.get('km_with', 0)
        num_passengers = journey.get('num_passengers', 0)
        hours_waiting = journey.get('hours_waiting', 0)
        hours_total = journey.get('hours_total', 0)
        
        # Base journey price
        journey_price = (km_without * 1.5) + (km_with * 2.5) + (hours_waiting * 50) + (hours_total * 32)
        
        # Add passenger surcharge if more than 3 passengers
        if num_passengers > 3:
            total_km = km_without + km_with
            extra_passengers = num_passengers - 3
            
            if total_km < 200:
                journey_price += extra_passengers * 30
            else:
                journey_price += extra_passengers * 100
        
        total += journey_price
    
    st.session_state.total_price = total
    st.rerun()

st.success(f"## **Final Quote: ${st.session_state.total_price:.2f}**")
