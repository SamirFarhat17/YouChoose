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
plotly.tools.set_credentials_file(username='SamirFarhat', api_key='OEv9RN9Pj5WkWrTZw9yT')

x = 0
count_very_offensive = 0
count_probably_offensive = 0
count_unclear = 0
count_benign = 0
count_hateful = 0
count_good = 0

def analyze(video_id, model):

    def  clean_text(df, text_field):
        df[text_field] = df[text_field].str.lower()
        df[text_field] = df[text_field].apply(lambda elem: re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", elem))
        return df

    to_return = []

    comments = get_comment_threads(video_id)

    clean_comments = clean_text(comments, 'comment')

    top_worst_comments = []
    worst_comment_pictures = []
    worst_comment_names = []


    def check_hateful(comments):

        global x
        global count_good
        global count_benign
        global count_hateful
        global count_probably_offensive
        global count_very_offensive
        global count_unclear

        for index, row in clean_comments.iterrows():
            toPredict = [row['comment']]
            y_predict = model.predict_proba(toPredict)
            if y_predict[0][1] > .90:
                count_very_offensive += 1

            elif y_predict[0][1] <= .90 and y_predict[0][1] > .83:
                top_worst_comments.append(row['comment'])
                worst_comment_names.append(row['authors'])
                worst_comment_pictures.append(row['pictures'])
                count_hateful += 1
                count_probably_offensive += 1
            elif y_predict[0][1] <= .83 and y_predict[0][1] > .40:
                count_unclear += 1
                count_good += 1
            else:
                count_benign += 1
                count_good += 1
            x += 1

    check_hateful(comments)


    ####################################################################

    data = [
        go.Scatterpolar(
          r = [count_very_offensive*10, count_probably_offensive*10, count_unclear*10, count_benign*10],
          theta = ['Very Offensive','Probably Offensive','Unclear', 'Benign'],
          fill = 'toself',
          name = 'Group A'
        )
    ]

    layout = go.Layout(
      polar = dict(
        radialaxis = dict(
          visible = True,
          range = [0, x*10]
        )
      ),
      showlegend = False
    )

    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename = "\\Users\\User\\dev\\YTAnalysis\\channel\\templates\\channel\\multiple", )
    if len(top_worst_comments) == 0:
        top_worst_comments.append("")
        worst_comment_names.append("No negative comments")
    to_return = zip(top_worst_comments,  worst_comment_names, worst_comment_pictures)

    return to_return
