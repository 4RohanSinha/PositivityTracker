import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from statistics import mean
nltk.download([
    "names",
    "stopwords",
    "state_union",
    "twitter_samples",
    "movie_reviews",
    "averaged_perceptron_tagger",
    "vader_lexicon",
    "punkt"
])

sia = SentimentIntensityAnalyzer()

def highest_val(sentence: str) -> float:
    negative = sia.polarity_scores(sentence)["neg"]
    neutral = sia.polarity_scores(sentence)["neu"]
    positive = sia.polarity_scores(sentence)["pos"]
    compound = sia.polarity_scores(sentence)["compound"]
    max_val = 0
    min_val = 0
    lst = sentence.split()
    if len(lst) <= 4:
        if compound < 0:
            return (neutral+compound)/2
        elif compound > 0:
            return (neutral+compound)/2
        elif compound == 0:
            return compound
    if compound < 0:
        if abs(negative) > abs(compound):
            max_val = -negative
        else:
            max_val = compound
    elif compound > 0:
        if positive > compound:
            max_val = positive
        else:
            max_val = compound
    elif compound == 0:
        max_val = compound
    return max_val

stopwords = nltk.corpus.stopwords.words("english")[:131]
def sentiment_analysis(entry: str) -> float:
    entry = nltk.word_tokenize(entry)
    entry = [word for word in entry if not word.lower() in stopwords]
    entry = [word.lower() for word in entry]
    entry = [word for word in entry if not word.isnumeric()]
    dear_diary = ["dear", "diary"]
    entry = [word for word in entry if word.lower() not in dear_diary]
    entry = (" ").join(entry)
    entry = nltk.sent_tokenize(entry)
    scores = [
        highest_val(sentence) for sentence in entry
    ]
    return mean(scores)
