import streamlit as st

st.title("Taxi Calculator!")

#initialise session state
if 'journeys' not in st.session_state:
    st.session_state.journeys = [{}]  # Start with one empty journey
if 'total_price' not in st.session_state:
    st.session_state.total_price = 0

st.subheader("Add Journey Details")

for idx, journey in enumerate(st.session_state.journeys):
    st.markdown(f"### Journey {idx + 1}")
    km_without = st.number_input("Enter km WITHOUT passengers:", min_value=0.0, key=f"km_without_{idx}")
    km_with = st.number_input("Enter km WITH passengers:", min_value=0.0, key=f"km_with_{idx}")
    hours_waiting = st.number_input("Enter Hours driver will wait:", min_value=0.0, key=f"hours_waiting_{idx}")
    col1, col2 = st.columns(2)
    st.write("Enter time spent driving")
    with col1:
          hours = st.number_input("Hours", min_value=0.0, key=f"hours_{idx}")
    with col2:
          mins = st.number_input("Minutes", min_value=0.0, max_value=59.0, key=f"mins_{idx}")
    hours_total = hours + (mins / 60)
    
    #store in journey dictionary 
    st.session_state.journeys[idx] = {
        'km_without': km_without,
        'km_with': km_with,
        'hours_waiting': hours_waiting,
        'hours_total': hours_total
    }

#add journey
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
            hours_waiting = journey.get('hours_waiting', 0)
            hours_total = journey.get('hours_total', 0)
            
            journey_price = (km_without * 1.5) + (km_with * 2.5) + (hours_waiting * 50) + (hours_total * 32)
            total += journey_price
        
        st.session_state.total_price = total
        st.rerun()

st.success(f"## **Final Quote: ${st.session_state.total_price:.2f}**")
