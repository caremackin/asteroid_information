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

# CHECKLIST ITEM #8.2
dates_df = pd.DataFrame(personal_data)
dates_df.to_csv('interest_dates.csv', index=False)

dates = pd.read_csv("interest_dates.csv")
print(dates)

# CHECKLIST ITEM #10.4 and 10.5
api_key = "8rwe6cRZTAU2PJQdI3UnHJFhINTMT6yV7fN1VgfF"
base_url = "https://api.nasa.gov/neo/rest/v1/feed"

for interest_date in dates['Interest dates']:
    print("DATE OF INTEREST:" + interest_date)
    print("")
    response = requests.get(base_url, params={"start_date": interest_date, "end_date": interest_date, "api_key": api_key})
    content = response.content
    asteroid_data = json.loads(content)

    if response.status_code == 200:
        asteroids = asteroid_data.get("near_earth_objects", {}).get(interest_date, [])
        asteroid_list = []

        for i in range(len(asteroids)):
            asteroid_info = asteroids[i]
            table_info = {
                "Name": asteroid_info["name"],
                "Max Estimated Diameter": asteroid_info["estimated_diameter"]["kilometers"]["estimated_diameter_max"],
                "Relative Velocity": asteroid_info["close_approach_data"][0]["relative_velocity"]["kilometers_per_second"],
                "Is Potentially Hazardous": asteroid_info["is_potentially_hazardous_asteroid"]
            }

            asteroid_list.append(table_info)

        df = pd.DataFrame(asteroid_list)
        print(df)
        print("")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
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
    while True:
        diameter_filter_input = input("Enter minimum max diameter you are searching for: ")
        if(diameter_filter_input[0].isdigit):
            diameter_filter = float(diameter_filter_input)
            condition = df['Max Estimated Diameter'] > diameter_filter
            filtered_df = df[condition]
            print("")
            print("")
            print(filtered_df)
            relative_velocity = np.array(filtered_df["Relative Velocity"])
            max_diameter = np.array(filtered_df["Max Estimated Diameter"])

            plt.scatter(relative_velocity, max_diameter)
            plt.title("Filtered Asteroids Scatter Plot")
            plt.xlabel("Relative Velocity (km/s)")
            plt.ylabel("Estimated Diameter (Max) in km")
            plt.show()
            break

