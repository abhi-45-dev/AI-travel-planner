import streamlit as st
import openai
import json
import matplotlib.pyplot as plt

# ---------------- CONFIG ----------------
st.set_page_config(page_title="AI Travel Planner", layout="wide")

st.title("✈️ AI Travel Planning Agent")
st.caption("Generate realistic, city-specific travel itineraries with cost estimation")

# Load OpenAI key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# ---------------- INPUTS ----------------
with st.sidebar:
    st.header("Trip Details")

    start_country = st.text_input("Starting Country")
    start_city = st.text_input("Starting City")

    dest_country = st.text_input("Destination Country")
    dest_city = st.text_input("Destination City")

    days = st.number_input("Trip Duration (Days)", min_value=1, max_value=30, value=5)
    people = st.number_input("Number of People", min_value=1, max_value=10, value=1)

    generate = st.button("Generate Plan")

# ---------------- PROMPT ----------------
def build_prompt():
    return f"""
You are a professional travel planner.

Create a detailed, realistic travel itinerary.

RULES:
- DO NOT repeat the same activities every day
- Mention REAL attractions, neighborhoods, or nearby places in {dest_city}
- Each day MUST be different
- Structure output EXACTLY in JSON
- Costs should be realistic estimates in INR
- Costs should scale for {people} people

TRIP DETAILS:
From: {start_city}, {start_country}
To: {dest_city}, {dest_country}
Duration: {days} days
People: {people}

JSON FORMAT ONLY:

{{
  "itinerary": {{
    "Day 1": {{
      "Morning": "...",
      "Afternoon": "...",
      "Evening": "..."
    }}
  }},
  "cost_estimate": {{
    "Travel": number,
    "Accommodation": number,
    "Food & Activities": number
  }}
}}
"""

# ---------------- GENERATION ----------------
def generate_plan():
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": build_prompt()}],
        temperature=0.7
    )
    return json.loads(response.choices[0].message.content)

# ---------------- OUTPUT ----------------
if generate:
    try:
        data = generate_plan()
        itinerary = data["itinerary"]
        cost = data["cost_estimate"]

        st.divider()
        st.header("🗓️ Day-wise Itinerary")

        for day, plan in itinerary.items():
            with st.expander(day, expanded=True):
                st.markdown(f"🌅 **Morning:** {plan['Morning']}")
                st.markdown(f"🌞 **Afternoon:** {plan['Afternoon']}")
                st.markdown(f"🌙 **Evening:** {plan['Evening']}")

        # ---------------- COST SUMMARY ----------------
        st.divider()
        st.header("💰 Cost Summary (Estimated)")

        total_cost = sum(cost.values())

        col1, col2 = st.columns([1, 1])

        with col1:
            st.metric("Estimated Total Cost (INR)", f"₹{total_cost:,}")

        with col2:
            fig, ax = plt.subplots()
            ax.bar(cost.keys(), cost.values())
            ax.set_ylabel("Cost (INR)")
            ax.set_title("Cost Breakdown")
            st.pyplot(fig)

        st.info(
            "Costs vary based on season, booking time, and personal preferences.\n\n"
            "• Travel: Flights / trains / buses\n"
            "• Accommodation: Budget to mid-range hotels\n"
            "• Food & Activities: Local dining & attractions"
        )

    except Exception as e:
        st.error("Failed to generate plan. Please try again.")
        st.exception(e)

