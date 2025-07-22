import pandas as pd
import re
person = "/course/person.csv"

def task1_1():
    df = pd.read_csv(person)

    #find most frequently occurring category in 'HELMET_BELT_WORN' column
    most_frequent_category = df['HELMET_BELT_WORN'].mode()[0]
    #replace missing values with mode
    df['HELMET_BELT_WORN'] = df['HELMET_BELT_WORN'].fillna(most_frequent_category)

    #convert 'SEX' and 'ROAD_USER_TYPE_DESC' from categorical to numerical (binary) format
    df = pd.get_dummies(df, columns=['SEX', 'ROAD_USER_TYPE_DESC'], drop_first=True, dtype=int)

    #helper function to categorise values in 'AGE_GROUP' into broader ranges
    def categorise_age_group(age_group):
        #extract numbers from age_group string using regex
        match = re.findall(r'\d+', str(age_group))
        if not match:
            #return original value if no viable value found
            return age_group
        #convert lower bound of age range to an integer
        lower = int(match[0])
        #implement set of conditional statements to assign specific age group based on lower bound
        if lower < 16:
            return 'Under 16'
        elif lower < 26:
            return '17-25'
        elif lower < 40:
            return '26-39'
        elif lower < 65:
            return '40-64'
        else:
            return '65+'
    #apply helper function 'categorise_age_group' to 'AGE_GROUP' column
    df['AGE_GROUP'] = df['AGE_GROUP'].apply(categorise_age_group)
    print(df)
    return df
