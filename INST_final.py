import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json


personal_data = {
    'Interest dates': [],
}

while True:
    interest_dates = input("Enter interest dates in YYYY-MM-DD format or nothing to continue: ")
    if interest_dates == "":
        break
    personal_data['Interest dates'].append(interest_dates)

#CHECKLIST ITEM #8.2
dates_df = pd.DataFrame(personal_data)
dates_df.to_csv('interest_dates.csv', index=False)

dates = pd.read_csv("interest_dates.csv")
print(dates)


#CHECKLIST ITEM #10.4 and 10.5
api_key = "8rwe6cRZTAU2PJQdI3UnHJFhINTMT6yV7fN1VgfF"
base_url = "https://api.nasa.gov/neo/rest/v1/feed"

response = requests.get(base_url, params={"start_date":"2003-07-12","end_date":"2003-07-12","api_key": api_key})
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
        # print(table_info)

    df = pd.DataFrame(asteroid_list)
    print(df)

    #CHECKLIST ITEM #8.4
    csv_file_path = 'asteroid_infomation.csv'
    df.to_csv(csv_file_path, index=False)
    print(f'Data has been written to {csv_file_path}.')


    #CHECKLIST ITEM #8.1
    relative_velocity = np.array(df["Relative Velocity"])
    max_diameter = np.array(df["Max Estimated Diameter"])

    plt.scatter(relative_velocity, max_diameter)
    plt.title("Asteroids Scatter Plot")
    plt.xlabel("Relative Velocity (km/s)")
    plt.ylabel("Estimated Diameter (Max) in km")
    plt.show()

    #CHECKLIST ITEM #8.3
    diameter_filter = float(input("Enter minimum max diameter you are searching for: "))
    condition = df['Max Estimated Diameter'] > diameter_filter
    filtered_df = df[condition]
    print(filtered_df)


else: 
    print(f"Error: {response.status_code}")
    print(response.text) 


