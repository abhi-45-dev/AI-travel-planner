import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI Travel Planner", layout="wide")

st.title("✈️ AI Travel Planning Agent")
st.caption("Dynamic, destination-aware travel itineraries")

# -------- INPUTS --------
with st.sidebar:
    st.header("Trip Details")

    start_country = st.text_input("Starting Country")
    start_city = st.text_input("Starting City")

    dest_country = st.text_input("Destination Country")
    dest_city = st.text_input("Destination City")

    days = st.number_input("Trip Duration (Days)", min_value=1, max_value=30, value=5)
    people = st.number_input("Number of People", min_value=1, max_value=10, value=1)

    generate = st.button("Generate Plan")

# -------- LOGIC --------
def generate_itinerary(city, days):
    places = [
        "Historic City Center",
        "Famous Landmark",
        "Local Market",
        "Popular Museum",
        "Scenic Neighborhood",
        "Cultural District",
        "Riverside Walk",
        "Hidden Café Area",
        "Art & Street Zone",
        "Viewpoint / Hilltop"
    ]

    itinerary = {}

    for d in range(days):
        place = places[d % len(places)]
        itinerary[f"Day {d+1}"] = {
            "Morning": f"Visit the {place} of {city}",
            "Afternoon": f"Explore nearby attractions and local food spots in {city}",
            "Evening": f"Relax, dine, or explore nightlife in {city}"
        }

    return itinerary


def estimate_cost(days, people):
    cost = {
        "Travel": 15000 * people,
        "Stay": 4000 * days * people,
        "Food & Activities": 2500 * days * people
    }
    return cost


# -------- OUTPUT --------
if generate:
    if not dest_city or not dest_country:
        st.error("Please enter destination city and country.")
    else:
        st.subheader("🗓️ Day-wise Itinerary")

        itinerary = generate_itinerary(dest_city, days)

        for day, plan in itinerary.items():
            with st.expander(day, expanded=True):
                st.markdown(f"🌅 **Morning:** {plan['Morning']}")
                st.markdown(f"🌞 **Afternoon:** {plan['Afternoon']}")
                st.markdown(f"🌙 **Evening:** {plan['Evening']}")

        # -------- COST --------
        st.subheader("💰 Cost Summary (Estimated)")
        cost = estimate_cost(days, people)

        total = sum(cost.values())
        st.metric("Estimated Total Cost (INR)", f"₹{total:,}")

        fig, ax = plt.subplots()
        ax.bar(cost.keys(), cost.values())
        ax.set_ylabel("INR")
        ax.set_title("Cost Breakdown")
        st.pyplot(fig)

        # -------- MAP --------
        st.subheader("🗺️ Travel Route")
        map_url = (
            f"https://www.google.com/maps/dir/"
            f"{start_city},{start_country}/"
            f"{dest_city},{dest_country}"
        )
        st.markdown(f"[View Route on Google Maps]({map_url})")

