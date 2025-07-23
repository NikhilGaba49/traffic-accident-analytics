from preprocessing_text_feature_words_20 import pd, plt, re, find_most_freq_words, accidents

days = ['Monday', 'Friday', 'Sunday']
times_of_day = ['Morning', 'Afternoon', 'Evening', 'Late Night']

# A function defining the boundaries for each time of day
def categorise_time_of_day(time):
    time_pattern = r"(\d{1,2}):\d\d:\d\d"
    string_match = re.search(time_pattern, time)
    if not string_match:
        return "Invalid"
    hour = int(string_match.group(1))
    if hour < 6:
        return "Late Night"
    elif hour < 12:
        return "Morning"
    elif hour < 18:
        return "Afternoon"
    return "Evening"

# A function to generate a bar chart to show accidents by (categorised) time of day
def accidents_by_time_of_day ():
        # Categorise each accidents' time by the time of day (Morning, Afternoon, etc.)
    time_of_day_col = accidents['ACCIDENT_TIME'].apply(lambda x: categorise_time_of_day(x))
    accidents.insert(len(accidents.columns), "TIME_OF_DAY", time_of_day_col) # insert at the last column index

    # Create bar chart with time of day as x-axis and frequencies for the y-axis
    # NB: reindex is to reorder the groupby output so that bar chart can be in logical order (Morning then Afternoon, etc.)
    plt.bar(times_of_day, accidents.groupby('TIME_OF_DAY')['ACCIDENT_NO'].count().reindex(times_of_day))
    plt.xlabel("Time of Day")
    plt.ylabel("Accident Count")
    plt.title("Frequency of Accidents by Time of Day")
    plt.savefig('task2_2_timeofday.png')
    plt.close()