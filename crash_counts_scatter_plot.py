import pandas as pd
import matplotlib.pyplot as plt

def task3_1():

    # Loading in the Dataset
    df = pd.read_csv("/course/filtered_vehicle.csv")

    print(df.head())

    # Group by Year, Body Style, and Make, and count the number of crashes
    crash_counts = df.groupby(['VEHICLE_YEAR_MANUF', 'VEHICLE_BODY_STYLE', 'VEHICLE_MAKE']).size().reset_index(name='CRASH_COUNT')

    # Sorting the DataFrame by the Year of Manufacturing
    crash_counts = crash_counts.sort_values(by='VEHICLE_YEAR_MANUF')

    # Creating the Scatterplot
    plt.scatter(crash_counts['VEHICLE_YEAR_MANUF'], crash_counts['CRASH_COUNT'], alpha=0.6)

    plt.xlabel('Year of Vehicle Manufacture')
    plt.ylabel('Number of Crashes')
    plt.title('Crash Counts per Manufacturer-Body Style-Year Combination')

    # Saving the Scatterplot
    plt.savefig('task3_1_scatter.png')

    return crash_counts
