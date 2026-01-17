import streamlit as st
import pandas as pd

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="AI Travel Planning Agent",
    page_icon="✈️",
    layout="wide"
)

# ------------------ SIDEBAR INPUTS ------------------
st.sidebar.title("🧳 Trip Details")

start_country = st.sidebar.text_input("Starting Country")
start_city = st.sidebar.text_input("Starting City")

dest_country = st.sidebar.text_input("Destination Country")
dest_city = st.sidebar.text_input("Destination City")

days = st.sidebar.number_input(
    "Trip Duration (Days)",
    min_value=1,
    max_value=30,
    value=5,
    step=1
)

people = st.sidebar.number_input(
    "Number of People",
    min_value=1,
    max_value=10,
    value=1,
    step=1
)

generate = st.sidebar.button("Generate Plan")

# ------------------ HEADER ------------------
st.title("✈️ AI Travel Planning Agent")
st.caption("Structured itinerary, cost estimation & route planning")

# ------------------ HELPER FUNCTIONS ------------------
def generate_itinerary(city, days):
    itinerary = {}
    for d in range(1, days + 1):
        itinerary[f"Day {d}"] = {
            "Morning": f"Explore a major landmark or popular attraction in {city}.",
            "Afternoon": f"Visit museums, cultural areas, or local neighborhoods in {city}.",
            "Evening": f"Relax, dine locally, or enjoy nightlife in {city}."
        }
    return itinerary


def estimate_cost(days, people):
    return {
        "Accommodation": days * 4500 * people,
        "Food & Activities": days * 2500 * people,
        "Travel": 30000 * people
    }


# ------------------ MAIN OUTPUT ------------------
if generate:

    # ---------- VALIDATION ----------
    if not all([start_country, start_city, dest_country, dest_city]):
        st.error("⚠️ Please fill in all location fields.")
        st.stop()

    st.success("✅ Travel plan generated successfully!")

    # ---------- DESTINATION OVERVIEW ----------
    st.subheader("🌍 Destination Overview")
    st.write(
        f"You are traveling from **{start_city}, {start_country}** "
        f"to **{dest_city}, {dest_country}** for **{days} days** "
        f"with **{people} traveler(s)**."
    )

    # ---------- TRAVEL ROUTE ----------
    st.subheader("🗺️ Travel Route")

    origin = f"{start_city}, {start_country}".replace(" ", "+")
    destination = f"{dest_city}, {dest_country}".replace(" ", "+")

    map_url = (
        "https://www.google.com/maps/dir/?api=1"
        f"&origin={origin}&destination={destination}"
    )

    st.markdown(f"🔗 **View Route on Google Maps:** [Open Map]({map_url})")

    map_df = pd.DataFrame({
        "lat": [20.5937, 48.8566],
        "lon": [78.9629, 2.3522]
    })
    st.map(map_df)

    # ---------- ITINERARY ----------
    st.subheader("📅 Day-wise Itinerary")

    itinerary = generate_itinerary(dest_city, days)

    for day, plan in itinerary.items():
        with st.expander(day, expanded=True):
            st.markdown(f"**🌅 Morning:** {plan['Morning']}")
            st.markdown(f"**🌞 Afternoon:** {plan['Afternoon']}")
            st.markdown(f"**🌙 Evening:** {plan['Evening']}")

    # ---------- COST SUMMARY ----------
    st.subheader("💰 Cost Summary (Estimated)")

    cost = estimate_cost(days, people)
    total_cost = sum(cost.values())

    st.metric(
        "Estimated Total Cost (INR)",
        f"₹{total_cost:,}"
    )

    cost_df = pd.DataFrame({
        "Category": cost.keys(),
        "Cost (INR)": cost.values()
    })

    st.bar_chart(cost_df.set_index("Category"))

    st.info(
        "💡 Costs are estimated per person and depend on season, "
        "travel mode, and accommodation preferences."
    )

    # ---------- DOWNLOAD ----------
    report_text = f"""
TRAVEL PLAN REPORT

From: {start_city}, {start_country}
To: {dest_city}, {dest_country}
Duration: {days} days
Number of People: {people}

ITINERARY:
"""

    for day, plan in itinerary.items():
        report_text += f"\n{day}\n"
        for k, v in plan.items():
            report_text += f"- {k}: {v}\n"

    report_text += "\nCOST ESTIMATE:\n"
    for k, v in cost.items():
        report_text += f"{k}: INR {v}\n"

    report_text += f"\nTOTAL: INR {total_cost}\n"

    st.download_button(
        "⬇️ Download Trip Report",
        report_text,
        file_name="travel_plan.txt"
    )

else:
    st.info("👈 Enter trip details and click **Generate Plan**")
