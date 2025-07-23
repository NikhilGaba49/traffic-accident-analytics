import pandas as pd
import matplotlib.pyplot as plt
import re
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import WordCloud

stop_words = set(stopwords.words('english'))

def text_processing(entry):

    # case fold all text into lower case
    entry = entry.lower()

    entry = re.sub(r'\.(?=\w)','. ', entry)  # Add a space after fullstop without a space
    entry = re.sub(r'[^a-z\s\d]', ' ', entry) # remove punctuation (already case folded)
    entry = re.sub(r'\s+', ' ', entry)  # remove extra spaces

    # split the text into words & remove the stopwords
    tokens = nltk.tokenize.word_tokenize(entry)
    tokens = [word for word in tokens if word not in stop_words]
    return tokens

def find_most_freq_words(data):

    # form bag of words for the various descriptions
    vectorizer = CountVectorizer()
    bow = vectorizer.fit_transform(data['DCA_DESC'])

    # find all the terms listed in any of the descriptions
    vocabulary = vectorizer.get_feature_names_out()

    # finding the most common terms in accident descriptions by finding the
    # total frequencies for each term in vocabulary, dealing with sparse matrices
    sum_frequencies = [bow.getcol(i).sum() for i in range(len(vocabulary))]
    sorted_freq = pd.Series(data=sum_frequencies, index = vocabulary).sort_values(ascending=False)

    # the most freq terms appear at the start & at the index (values are frequencies)
    return sorted_freq

accidents = pd.read_csv("/course/accident.csv") 
# For each description, processing text into a list of 'key words'
# Then, converting to a string again
accidents['DCA_DESC'] = accidents['DCA_DESC'].apply(lambda x: ' '.join(text_processing(x)))

def task2_1():

    most_freq = find_most_freq_words(accidents).index[:20] # the 20 most frequent words only

    # form the wordcloud from the most freq terms, adapted from datacamp
    word_cloud = WordCloud(background_color = 'white', normalize_plurals = False).generate(' '.join(most_freq))
    word_cloud.to_file("task2_1_word_cloud.png")

    return accidents
