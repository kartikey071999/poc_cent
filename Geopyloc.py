from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut


def calculate_distance(location1, location2):
    return geodesic(location1, location2).kilometers

def get_lat_long(location_name):
    geolocator = Nominatim(user_agent="kartikey")
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            location = geolocator.geocode(location_name)
            if location:
                return location.latitude, location.longitude
        except GeocoderTimedOut:
            if attempt < max_retries - 1:
                print(f"Geocoding request timed out. Retrying (attempt {attempt + 2}/{max_retries}).")
                continue
            else:
                print("Max retry attempts reached. Unable to geocode the location.")
                break

    return None

locations_data = [
    {"location_id": 1, "location_name": "New York City, USA", "zipcode": "10001"},
    {"location_id": 2, "location_name": "Los Angeles, USA", "zipcode": "90001"},
    {"location_id": 3, "location_name": "Chicago, USA", "zipcode": "60601"},
    {"location_id": 4, "location_name": "Houston, USA", "zipcode": "77001"},
    {"location_id": 5, "location_name": "San Francisco, USA", "zipcode": "94105"},
    {"location_id": 6, "location_name": "Toronto, Canada", "zipcode": "M5A 0A1"},
    {"location_id": 7, "location_name": "London, UK", "zipcode": "SW1A 1AA"},
    {"location_id": 8, "location_name": "Tokyo, Japan", "zipcode": "100-0001"},
    {"location_id": 9, "location_name": "Sydney, Australia", "zipcode": "2000"},
    {"location_id": 10, "location_name": "Cape Town, South Africa", "zipcode": "8001"},
]

locations_data = [
    {"location_name": "Location 1", "zipcode": "75227"},
    {"location_name": "Location 2", "zipcode": "75210"},
    {"location_name": "Location 3", "zipcode": "75228"},
    {"location_name": "Location 4", "zipcode": "75149"},
    {"location_name": "Location 5", "zipcode": "75223"},
    {"location_name": "Location 6", "zipcode": "75150"},
    {"location_name": "Location 7", "zipcode": "75218"},
    {"location_name": "Location 8", "zipcode": "75215"},
    {"location_name": "Location 9", "zipcode": "75217"},
]

def main():
    input_location_id = int(input("Enter a location_id: "))

    selected_location = next((location for location in locations_data if location["location_id"] == input_location_id), None)

    if selected_location:
        selected_lat_long = get_lat_long(selected_location["zipcode"])

        if selected_lat_long:
            distances = []
            for location in locations_data:
                if location["location_id"] != input_location_id: 
                    location_lat_long = get_lat_long(input_location_id)

                    geopy_dist = calculate_distance(selected_lat_long, location_lat_long)

                    distances.append({
                        "location_name": location["location_name"],
                        "geopy_distance": geopy_dist
                    })

            sorted_distances = sorted(distances, key=lambda x: x["geopy_distance"])

            print(f"\nDistances from {selected_location['location_name']} ({selected_location['zipcode']}):")
            for item in sorted_distances:
                print(f"{item['location_name']} - Geopy: {item['geopy_distance']:.2f} km")
        else:
            print("Latitude and longitude not found for the selected location.")
    else:
        print("Location not found.")

if __name__ == "__main__":
    main()