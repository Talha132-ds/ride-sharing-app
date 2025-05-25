import streamlit as st
import requests
import folium
from streamlit_folium import st_folium

# --- Get real driving distance and time using OSRM ---
def get_distance_time_osrm(origin, destination):
    url = f"http://router.project-osrm.org/route/v1/driving/{origin[1]},{origin[0]};{destination[1]},{destination[0]}?overview=false"
    response = requests.get(url)
    data = response.json()
    
    if "routes" in data and data["routes"]:
        route = data["routes"][0]
        distance_km = round(route["distance"] / 1000, 2)
        duration_min = round(route["duration"] / 60, 2)
        return distance_km, duration_min
    return None, None

# --- Create interactive map ---
def generate_map(rider_location, driver_location):
    ride_map = folium.Map(location=rider_location, zoom_start=13)
    folium.Marker(rider_location, popup="Rider", icon=folium.Icon(color="blue")).add_to(ride_map)
    folium.Marker(driver_location, popup="Closest Driver", icon=folium.Icon(color="red")).add_to(ride_map)
    folium.PolyLine([rider_location, driver_location], color="green", weight=3).add_to(ride_map)
    return ride_map

# --- Streamlit App UI ---
st.title("🚗 Uber-Like Ride Sharing System (Shortest Driver Finder)")

st.markdown("Enter the coordinates below:")

st.subheader("📍 Rider Location")
rider_lat = st.number_input("Rider Latitude", format="%.6f")
rider_lon = st.number_input("Rider Longitude", format="%.6f")

st.subheader("🚕 Driver 1 Location")
driver1_lat = st.number_input("Driver 1 Latitude", format="%.6f")
driver1_lon = st.number_input("Driver 1 Longitude", format="%.6f")

st.subheader("🚖 Driver 2 Location")
driver2_lat = st.number_input("Driver 2 Latitude", format="%.6f")
driver2_lon = st.number_input("Driver 2 Longitude", format="%.6f")

if st.button("🔍 Find Closest Driver"):
    rider = (rider_lat, rider_lon)
    driver1 = (driver1_lat, driver1_lon)
    driver2 = (driver2_lat, driver2_lon)

    drivers = [driver1, driver2]
    closest_driver = None
    min_distance = float("inf")
    min_time = None

    for driver in drivers:
        distance, time = get_distance_time_osrm(rider, driver)
        if distance and distance < min_distance:
            min_distance = distance
            min_time = time
            closest_driver = driver

    if closest_driver:
        st.success(f"✅ Closest Driver: {closest_driver}")
        st.info(f"📏 Distance: {min_distance} km | ⏱️ Time: {min_time} minutes")
        ride_map = generate_map(rider, closest_driver)
        st_folium(ride_map, width=700, height=500)
    else:
        st.error("❌ Could not find a route to any driver.")
