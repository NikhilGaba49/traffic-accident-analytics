from task1_1 import task1_1
import pandas as pd
import matplotlib.pyplot as plt
import re

def task1_2():
    df = task1_1()
    #map seatbelt-use values to readable labels
    seatbelt_mapping = {1.0: "Seatbelt Worn",
                        8.0: "Seatbelt Not Worn"}
    df["Seatbelt Use"] = df["HELMET_BELT_WORN"].map(seatbelt_mapping)
    #delete any missing values from 'Seatbelt Use'
    df = df.dropna(subset=["Seatbelt Use"])
    #filter for passengers AFTER Task1_1's one-hot encoding
    passengers = df[
        (df["ROAD_USER_TYPE_DESC_Passengers"] == 1) |
        (df["ROAD_USER_TYPE_DESC_Pillion Passengers"] == 1)
    ]
    #create a bar chart showing seatbelt use across broader age groups
    #define order for age groups (for bar chart output)
    age_order = ["Under 16", "17-25", "26-39", "40-64", "65+", "Unknown"]
    seatbelt_counts = passengers.groupby(["AGE_GROUP", "Seatbelt Use"]).size().unstack().reindex(age_order)
    #create figure and axes for bar chart
    fig, ax = plt.subplots(figsize=(12, 6))
    #plot seatbelt counts as a bar chart
    seatbelt_counts.plot(kind="bar", ax=ax)
    plt.xlabel("Age Group")
    plt.ylabel("Seatbelt Use Distribution")
    plt.title("Seatbelt Use across Age Groups")
    plt.savefig("task1_2_age.png")

    #create a plot of pie charts comparing seatbelt use between Drivers and Passengers
    #filter for drivers AFTER Task1_1's one-hot encoding
    drivers = df[df["ROAD_USER_TYPE_DESC_Drivers"] == 1]
    #count 'Seatbelt Use' for drivers and passengers
    driver_counts = drivers.groupby("Seatbelt Use").size()
    passenger_counts = passengers.groupby("Seatbelt Use").size()

    #create subplots for pie charts
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    #plot pie chart for drivers
    axes[0].pie(driver_counts, labels=driver_counts.index, autopct="%1.2f%%")
    axes[0].set_title("Seatbelt Use of Drivers")
    #plot pie chart for passengers
    axes[1].pie(passenger_counts, labels=passenger_counts.index, autopct="%1.2f%%")
    axes[1].set_title("Seatbelt Use of Passengers")
    plt.savefig("task1_2_driver.png")

    #create a plot of pie charts comparing seatbelt use between front-seat and rear-seat passengers
    #define seating positions
    front_seat_positions = ['LF', 'CF', 'PL']
    rear_seat_positions = ['RR', 'CR', 'LR', 'OR']

    #filter data for front-seat and rear-seat passengers using regex
    front_seat_data = df[df['SEATING_POSITION'].str.contains('|'.join(front_seat_positions), na=False)]
    rear_seat_data = df[df['SEATING_POSITION'].str.contains('|'.join(rear_seat_positions), na=False)]

    #count 'Seatbelt Use' for front-seat and rear-seat passengers
    front_counts = front_seat_data.groupby("Seatbelt Use").size()
    rear_counts = rear_seat_data.groupby("Seatbelt Use").size()

    #create subplots for pie charts
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    #plot pie chart for front-seat passengers
    axes[0].pie(front_counts, labels=front_counts.index, autopct="%1.2f%%")
    axes[0].set_title("Seatbelt Use of front-seat passengers")
    #plot pie chart for rear-seat passengers
    axes[1].pie(rear_counts, labels=rear_counts.index, autopct="%1.2f%%")
    axes[1].set_title("Seatbelt Use of rear-seat passengers")
    plt.savefig("task1_2_seat.png")
    
