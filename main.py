import requests

url = "https://opensky-network.org/api/states/all"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    states = data.get("states", [])
    
    for aircraft in states:  # Displaying only 5 aircraft for brevity
        icao24 = aircraft[0]
        callsign = aircraft[1].strip()
        country = aircraft[2]
        latitude = aircraft[6]
        longitude = aircraft[5]
        
        print(f"Aircraft {icao24} ({callsign}) from {country} at coordinates ({latitude}, {longitude})")
else:
    print(f"Failed to retrieve data: {response.status_code}")
