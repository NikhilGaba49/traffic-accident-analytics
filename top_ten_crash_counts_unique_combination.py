import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler

def complete_task():

    # Load Dataset
    df = pd.read_csv("/course/filtered_vehicle.csv")

    # Convert each of the needed columns to numeric
    df['NO_OF_WHEELS'] = pd.to_numeric(df['NO_OF_WHEELS'], errors='coerce')
    df['NO_OF_CYLINDERS'] = pd.to_numeric(df['NO_OF_CYLINDERS'], errors='coerce')
    df['SEATING_CAPACITY'] = pd.to_numeric(df['SEATING_CAPACITY'], errors='coerce')
    df['TARE_WEIGHT'] = pd.to_numeric(df['TARE_WEIGHT'], errors='coerce')
    df['TOTAL_NO_OCCUPANTS'] = pd.to_numeric(df['TOTAL_NO_OCCUPANTS'], errors='coerce')

    # Group the DataFrame
    grouped = df.groupby(['VEHICLE_YEAR_MANUF', 'VEHICLE_BODY_STYLE', 'VEHICLE_MAKE'])

    # Find the mean for each of the needed columns
    wheels_mean = grouped['NO_OF_WHEELS'].mean()
    cylinders_mean = grouped['NO_OF_CYLINDERS'].mean()
    seating_mean = grouped['SEATING_CAPACITY'].mean()
    tare_weight_mean = grouped['TARE_WEIGHT'].mean()
    occupants_mean = grouped['TOTAL_NO_OCCUPANTS'].mean()

    # Combine all of the individual means into one DataFrame
    crash_means = pd.DataFrame({
        'NO_OF_WHEELS': wheels_mean,
        'NO_OF_CYLINDERS': cylinders_mean,
        'SEATING_CAPACITY': seating_mean,
        'TARE_WEIGHT': tare_weight_mean,
        'TOTAL_NO_OCCUPANTS': occupants_mean
    })

    crash_means = crash_means.reset_index()

    # Normalise each of the features using Min-Max Scaling
    features = ['NO_OF_WHEELS', 'NO_OF_CYLINDERS', 'SEATING_CAPACITY', 'TARE_WEIGHT', 'TOTAL_NO_OCCUPANTS']

    scaler = MinMaxScaler()
    crash_means[features] = scaler.fit_transform(crash_means[features])

    # Run k-means with optimal K found in Task 3.2
    optimal_k = 3
    kmeans = KMeans(n_clusters=optimal_k)
    crash_means['CLUSTER'] = kmeans.fit_predict(crash_means[features])


    # Count number of crashes or each unique group
    crash_counts = df.groupby(['VEHICLE_YEAR_MANUF', 'VEHICLE_BODY_STYLE', 'VEHICLE_MAKE']).size().reset_index(name='CRASH_COUNT')

    # Merge crash counts with Cluster and Summary Statistics
    merged = pd.merge(crash_means, crash_counts, on=['VEHICLE_YEAR_MANUF', 'VEHICLE_BODY_STYLE', 'VEHICLE_MAKE'])

    # Plot the Scatter with Cluster Colours
    scatter = plt.scatter(
        merged['VEHICLE_YEAR_MANUF'],
        merged['CRASH_COUNT'],
        c=merged['CLUSTER']
    )

    plt.xlabel('Year of Vehicle Manufacture')
    plt.ylabel('Number of Crashes')
    plt.title('Crash Counts Coloured by Cluster')
    plt.colorbar(scatter, label='Cluster')
    plt.savefig('task3_3_scattercolour.png')
    plt.show()

    # Output top 10 crash counts per cluster
    for cluster_id in range(optimal_k):
        top_10 = merged[merged['CLUSTER'] == cluster_id] \
            .sort_values(by='CRASH_COUNT', ascending=False) \
            .head(10)
        output_file = f'task3_3_cluster{cluster_id}.csv'
        top_10.to_csv(output_file, index=False)

    return merged
