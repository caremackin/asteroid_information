import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json

api_key = "8rwe6cRZTAU2PJQdI3UnHJFhINTMT6yV7fN1VgfF"
base_url = "https://api.nasa.gov/neo/rest/v1/feed"

response = requests.get(base_url, params={"start_date":"2003-07-11","end_date":"2003-07-12","api_key": api_key})
content = response.content
asteroid_data = json.loads(content)

if response.status_code == 200:
    data = response.json()
    # print(data)

    asteroids = asteroid_data["near_earth_objects"]
    asteroid_list = []
    
    for i in range(4):
        asteroid_info = asteroids["2003-07-12"][i]
        table_info = {
            "Name": asteroid_info["name"],
            "Max Estimated Diameter": asteroid_info["estimated_diameter"]["kilometers"]["estimated_diameter_max"],
            "Relative Velocity": asteroid_info["close_approach_data"][0]["relative_velocity"]["kilometers_per_second"],
            "Is Potentially Hazardous": asteroid_info["is_potentially_hazardous_asteroid"]
        }
        
        asteroid_list.append(table_info)
        print(table_info)

    df = pd.DataFrame(asteroid_list)
    print(df)

    plt.scatter(df["Relative Velocity"], df["Max Estimated Diameter"])
    plt.title("Asteroids Scatter Plot")
    plt.xlabel("Relative Velocity (km/s)")
    plt.ylabel("Estimated Diameter (Max) in km")
    plt.show()

else: 
    print(f"Error: {response.status_code}")
    print(response.text) 


