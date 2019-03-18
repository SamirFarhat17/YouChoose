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
import pandas as pd
from math import pi
import plotly.plotly as py
import plotly.graph_objs as go
import plotly
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from retrieverComments import get_comment_threads

plotly.tools.set_credentials_file(username='SamirFarhat', api_key='OEv9RN9Pj5WkWrTZw9yT')


train = pd.read_csv('train.csv')

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

########################################################


comments = get_comment_threads('x1KubHyawQY')

clean_comments = clean_text(comments, 'comment')


def check_hateful(comments):
    x = 0
    global x
    count_very_offensive = 0
    count_probably_offensive = 0
    count_unclear = 0
    count_benign = 0

    count_hateful = 0
    count_good = 0

    global count_hateful
    global count_good
    global count_very_offensive
    global count_probably_offensive
    global count_unclear
    global count_benign

    for index, row in clean_comments.iterrows():
        toPredict = [row['comment']]
        y_predict = model.predict_proba(toPredict)
        print(y_predict)
        if y_predict[0][1] > .90:
            count_very_offensive += 1
        elif y_predict[0][1] <= .90 and y_predict[0][1] > .65:
            count_hateful += 1
            count_probably_offensive += 1
        elif y_predict[0][1] <= .65 and y_predict[0][1] > .40:
            count_unclear += 1
            count_good += 1
        else:
            count_benign += 1
            count_good += 1
        x += 1

check_hateful(comments)

print("[" + str(count_very_offensive) + ',' + str(count_probably_offensive) + ',' + str(count_unclear) + ',' + str(count_benign) + "]")
# Data to plot
labels = 'Hateful', 'Benign'
sizes = [count_hateful, count_good]
colors = ['gold', 'lightskyblue']
explode = (0, 0)  # explode 1st slice

# Plot
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=140)
plt.axis('equal')
plt.show()


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
plotly.offline.plot(fig, filename = "multiple.jpg")
