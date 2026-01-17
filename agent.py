import streamlit as st
import openai
import matplotlib.pyplot as plt

# ---------------- CONFIG ----------------
st.set_page_config(page_title="AI Travel Planner", layout="wide")

openai.api_key = st.secrets["OPENAI_API_KEY"]

# ---------------- UI ----------------
st.title("✈️ AI Travel Planning Agent")
st.caption("Generate realistic, day-wise travel itineraries")

with st.sidebar:
    st.header("Trip Details")

    start_country = st.text_input("Starting Country")
    start_city = st.text_input("Starting City")

    dest_country = st.text_input("Destination Country")
    dest_city = st.text_input("Destination City")

    days = st.number_input("Trip Duration (Days)", min_value=1, max_value=30, value=3)
    people = st.number_input("Number of Travelers", min_value=1, max_value=20, value=1)

    generate = st.button("Generate Plan")

# ---------------- PROMPT ----------------
def build_prompt():
    return f"""
You are a professional travel planner.

Create a realistic {days}-day itinerary for a trip from
{start_city}, {start_country} to {dest_city}, {dest_country}
for {people} travelers.

RULES (VERY IMPORTANT):
- Every day must be DIFFERENT
- Use REAL, SPECIFIC place names (monuments, streets, neighborhoods, attractions)
- DO NOT repeat activities across days
- DO NOT use generic phrases like "explore a landmark"
- Structure EVERY day as:

Day X:
Morning:
- specific places

Afternoon:
- specific places

Evening:
- specific places

Also provide:
1. A short "Travel Route" summary from start city to destination
2. A realistic cost estimate split into:
   - Travel
   - Stay
   - Food & Activities

Costs should be realistic for the destination country.
"""

# ---------------- GENERATE ----------------
if generate:
    if not all([start_country, start_city, dest_country, dest_city]):
        st.error("Please fill all location fields.")
    else:
        with st.spinner("Generating itinerary..."):
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": build_prompt()}],
                temperature=0.8
            )

        text = response.choices[0].message.content

        # ---------------- DISPLAY ----------------
        st.subheader("🗺️ Travel Route")
        st.write(f"{start_city}, {start_country} ➜ {dest_city}, {dest_country}")

        st.subheader("📅 Day-wise Itinerary")

        days_blocks = text.split("Day ")[1:]

        for block in days_blocks:
            day_title = block.split("\n")[0]
            content = block[len(day_title):]

            with st.expander(f"Day {day_title}", expanded=True):
                st.markdown(content)

        # ---------------- COST ESTIMATION ----------------
        st.subheader("💰 Estimated Cost Summary")

        travel_cost = 800 * people
        stay_cost = 120 * days * people
        food_cost = 60 * days * people

        labels = ["Travel", "Stay", "Food & Activities"]
        values = [travel_cost, stay_cost, food_cost]

        fig, ax = plt.subplots()
        ax.bar(labels, values)
        ax.set_ylabel("Cost (USD)")
        ax.set_title("Estimated Trip Cost")

        st.pyplot(fig)

        st.success("Trip plan generated successfully!")
