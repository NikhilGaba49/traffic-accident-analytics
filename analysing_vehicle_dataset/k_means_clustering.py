import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler

def clustering_kmeans_elbow_plot():

    # Loading the Dataset
    df = pd.read_csv("/course/filtered_vehicle.csv")

    # Concert each of the needed columns to numeric
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

    # Run K-Means for k=1 to k=10 and calculate the distortions
    distortions = []
    for k in range(1, 11):
      kmeans = KMeans(n_clusters=k)
      kmeans.fit(crash_means[features]) # Fits the KMeans model on the features
      distortions.append(kmeans.inertia_)

    # Plotting the Elbow Curve
    plt.plot(range(1, 11), distortions, 'bx-')
    plt.title('Elbow Method for Optimal k')
    plt.xlabel('Number of Clusters (k)')
    plt.ylabel('Distortions')
    plt.grid(True)
    plt.xticks(range(1, 11))

    # Saving the Plot
    plt.savefig('task3_2_elbow.png')

    return crash_means
