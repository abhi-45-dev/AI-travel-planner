import streamlit as st
import pandas as pd
import random

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="AI Travel Planning Agent",
    page_icon="✈️",
    layout="wide"
)

# ------------------ HEADER ------------------
st.title("✈️ AI Travel Planning Agent")
st.caption("Dynamic, destination-aware travel itineraries")

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

# ------------------ LARGE ACTIVITY POOLS ------------------
MORNING_ACTIVITIES = [
    "start the day with relaxed sightseeing",
    "explore key areas at an easy pace",
    "take a walking exploration route",
    "visit an important cultural area",
    "discover architectural highlights",
    "begin with a scenic exploration",
    "visit an early-opening attraction",
    "enjoy a calm morning stroll",
    "experience local morning routines",
    "explore historic surroundings",
    "visit public squares or centers",
    "walk through iconic districts",
    "explore urban landmarks",
    "start with panoramic viewpoints",
    "visit traditional neighborhoods",
    "enjoy a self-guided exploration",
    "explore old-town style areas",
    "visit open public spaces",
    "discover cultural landmarks",
    "start the day with exploration on foot",
    "explore heritage zones",
    "visit central city locations",
    "experience morning city life",
    "explore prominent streets",
    "visit community hubs",
    "discover local history areas",
    "walk through scenic routes",
    "visit culturally significant areas",
    "explore major attractions",
    "experience architectural diversity",
    "visit popular city highlights",
    "enjoy a calm discovery walk",
    "explore historic streets",
    "visit urban viewpoints",
    "discover central landmarks",
    "experience the city waking up",
    "visit public gardens or spaces",
    "walk through cultural corridors",
    "explore traditional districts",
    "visit early-day attractions",
    "discover local charm areas",
    "experience heritage trails",
    "walk scenic urban paths",
    "explore classic city routes",
    "visit iconic zones",
    "experience peaceful surroundings",
    "explore well-known areas",
    "start with cultural exploration",
    "visit historic cores"
]

AFTERNOON_ACTIVITIES = [
    "visit museums or galleries",
    "explore cultural institutions",
    "walk through local neighborhoods",
    "visit popular markets",
    "experience regional food options",
    "explore shopping districts",
    "visit cultural centers",
    "engage in leisure activities",
    "explore creative districts",
    "visit artisan or craft areas",
    "experience cultural exhibitions",
    "walk through vibrant streets",
    "visit community markets",
    "explore educational attractions",
    "experience mid-day cultural life",
    "visit interactive exhibits",
    "explore modern city areas",
    "visit historic museums",
    "experience food-focused areas",
    "walk cultural walking routes",
    "visit traditional marketplaces",
    "explore entertainment districts",
    "experience local commerce",
    "visit cultural hubs",
    "explore architectural spaces",
    "engage in casual exploration",
    "visit urban attractions",
    "experience city diversity",
    "walk through mixed-use areas",
    "visit art-focused locations",
    "explore neighborhood culture",
    "experience cultural immersion",
    "visit historical exhibits",
    "explore creative spaces",
    "experience culinary exploration",
    "visit retail and leisure zones",
    "walk social gathering areas",
    "experience mid-day relaxation",
    "visit local institutions",
    "explore cultural streets",
    "experience modern attractions",
    "visit open cultural areas",
    "walk food-centric districts",
    "experience artistic neighborhoods",
    "visit city museums",
    "explore traditional markets",
    "experience regional specialties",
    "visit public cultural spaces",
    "walk lively streets"
]

EVENING_ACTIVITIES = [
    "relax after a full day",
    "enjoy a leisurely dinner",
    "experience local nightlife",
    "take an evening walk",
    "explore illuminated areas",
    "visit entertainment districts",
    "enjoy casual evening dining",
    "experience night-time culture",
    "walk scenic evening routes",
    "visit social gathering spots",
    "relax in calm surroundings",
    "experience evening leisure",
    "visit live performance areas",
    "walk vibrant streets",
    "experience night markets",
    "enjoy local cuisine",
    "explore evening city life",
    "visit popular night zones",
    "relax at public spaces",
    "experience cultural nightlife",
    "walk lit-up landmarks",
    "visit music or art venues",
    "enjoy late evening snacks",
    "experience social nightlife",
    "walk along evening promenades",
    "visit cafes or lounges",
    "relax with scenic views",
    "experience nighttime atmosphere",
    "visit popular evening districts",
    "walk entertainment corridors",
    "enjoy casual night exploration",
    "experience calm night walks",
    "visit evening attractions",
    "enjoy relaxed dining",
    "experience cultural evenings",
    "visit social hotspots",
    "walk night-friendly streets",
    "experience evening relaxation",
    "visit late-opening venues",
    "enjoy local evening vibes",
    "experience laid-back nightlife",
    "walk scenic evening paths",
    "visit popular evening areas",
    "relax before resting",
    "experience quiet city moments",
    "enjoy informal nightlife",
    "visit well-lit city areas",
    "experience urban evenings",
    "walk evening cultural routes"
]

# ------------------ ITINERARY GENERATOR (NO REPEATS) ------------------
def generate_itinerary(city, country, days):
    seed = f"{city.lower()}_{country.lower()}"
    random.seed(seed)

    morning = MORNING_ACTIVITIES.copy()
    afternoon = AFTERNOON_ACTIVITIES.copy()
    evening = EVENING_ACTIVITIES.copy()

    random.shuffle(morning)
    random.shuffle(afternoon)
    random.shuffle(evening)

    itinerary = {}

    for d in range(days):
        itinerary[f"Day {d + 1}"] = {
            "Morning": morning[d % len(morning)],
            "Afternoon": afternoon[d % len(afternoon)],
            "Evening": evening[d % len(evening)]
        }

    return itinerary

# ------------------ COST MODEL ------------------
def estimate_cost(days, people):
    return {
        "Accommodation": days * 4500 * people,
        "Food & Activities": days * 2500 * people,
        "Travel": 30000 * people
    }

# ------------------ MAIN OUTPUT ------------------
if generate:

    if not all([start_country, start_city, dest_country, dest_city]):
        st.error("⚠️ Please fill in all location fields.")
        st.stop()

    st.success("✅ Travel plan generated successfully!")

    st.subheader("🌍 Destination Overview")
    st.write(
        f"From **{start_city}, {start_country}** → "
        f"**{dest_city}, {dest_country}** | "
        f"**{days} days**, **{people} traveler(s)**"
    )

    st.subheader("📅 Day-wise Itinerary")
    itinerary = generate_itinerary(dest_city, dest_country, days)

    for day, plan in itinerary.items():
        with st.expander(day, expanded=(day == "Day 1")):
            st.markdown(f"**🌅 Morning:** {plan['Morning']}")
            st.markdown(f"**🌞 Afternoon:** {plan['Afternoon']}")
            st.markdown(f"**🌙 Evening:** {plan['Evening']}")

    st.subheader("💰 Cost Summary (Estimated)")
    cost = estimate_cost(days, people)
    total_cost = sum(cost.values())

    st.metric("Estimated Total Cost (INR)", f"₹{total_cost:,}")

    cost_df = pd.DataFrame({
        "Category": cost.keys(),
        "Cost (INR)": cost.values()
    })

    st.bar_chart(cost_df.set_index("Category"))

else:
    st.info("👈 Enter trip details and click **Generate Plan**")
