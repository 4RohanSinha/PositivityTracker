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

def compound_val(sentence: str) -> float:
    return sia.polarity_scores(sentence)["compound"]

stopwords = nltk.corpus.stopwords.words("english")
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
        compound_val(sentence) for sentence in entry
    ]
    return mean(scores)