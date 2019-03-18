import pandas as pd
import re
from sklearn.utils import resample
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
import numpy as np
from math import pi
import plotly.plotly as py
import plotly.graph_objs as go
import plotly
import matplotlib
import matplotlib.pyplot as plt
from .retrieve_comments import get_comment_threads

def train():
    train = pd.read_csv('\\Users\\User\\dev\\YTAnalysis\\channel\\lib\\train.csv', encoding = "ISO-8859-1")

    #clean text by removing characters
    def  clean_text(df, text_field):
        df[text_field] = df[text_field].str.lower()
        df[text_field] = df[text_field].apply(lambda elem: re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", elem))
        return df


    train_clean = clean_text(train, "tweet")

    #upsample, meaning you use the minority set multiple times
    train_majority = train_clean[train_clean.label==0]
    train_minority = train_clean[train_clean.label==1]

    train_minority_upsampled = resample(train_minority, n_samples = len(train_majority), random_state = 123)

    train_upsampled = pd.concat([train_minority_upsampled, train_majority])
    train_upsampled['label'].value_counts()

    train_majority_downsampled = resample(train_majority, replace=True, n_samples=len(train_minority), random_state=123)
    train_downsampled = pd.concat([train_majority_downsampled, train_minority])
    train_downsampled['label'].value_counts()

    train_all = pd.concat([train_upsampled, train_downsampled])
    train_all['label'].value_counts()

    pipeline_sgd = Pipeline([('vect', CountVectorizer()), ('tfidf',  TfidfTransformer()), ('nb', SGDClassifier(loss = 'log'))])

    #X_train, X_test, y_train, y_test = train_test_split(train_upsampled['tweet'], train_upsampled['label'],random_state = 0)

    model = pipeline_sgd.fit(train_all['tweet'], train_all['label'])
    return model
########################################################
