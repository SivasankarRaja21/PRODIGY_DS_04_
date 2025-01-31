# -*- coding: utf-8 -*-
"""Prodigy4

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1oZrhMtMJDGUIJwshiFTDA80dUCumhaYw
"""

import pandas as pd
import matplotlib.pyplot as plt
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('cader_lexicon')

df=pd.read_csv(r'/content/twitter_training.csv')

df.head()

df.drop(df.columns[0], axis=1, inplace=True)
df.head()

df.columns = ["media","sentiment", "response"]
df.head()

df.columns

df.describe(include='all')

df.shape

df=df[df['sentiment']!='Neutral']
df=df[df['sentiment']!='Irrelevant']

df = df.groupby(['media','sentiment','response']).size().reset_index(name='count')

df.shape

senti=df.sentiment.factorize()

df.head()

print(df['sentiment'].unique())

from tensorflow.keras.preprocessing.text import Tokenizer

tweet = df.response.values

tok=Tokenizer(num_words=5000)
tok.fit_on_texts(tweet)

enco=tok.texts_to_sequences(tweet)

from tensorflow.keras.preprocessing.sequence import pad_sequences

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM,Dense, Dropout, SpatialDropout1D
from tensorflow.keras.layers import Embedding

embedding_vector_length = 32
model = Sequential()
model.add(Embedding(len(tok.word_index) + 1, embedding_vector_length, input_length=100))
model.add(SpatialDropout1D(0.25))
model.add(LSTM(50, dropout=0.5, recurrent_dropout=0.5))
model.add(Dropout(0.2))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='binary_crossentropy',optimizer='adam', metrics=['accuracy'])

print(model.summary())

padded_sequence = pad_sequences(enco,maxlen=100)
sentiment_label = senti[0]
history = model.fit(padded_sequence,sentiment_label,validation_split=0.2, epochs=5, batch_size=32)

plt.plot(history.history['accuracy'], label='acc')
plt.plot(history.history['val_accuracy'], label='val_acc')
plt.legend()
plt.show()
plt.savefig("Accuracy plot.jpg")

plt.plot(history.history['loss'], label='loss')
plt.plot(history.history['val_loss'], label='val_loss')
plt.legend()
plt.show()
plt.savefig("Loss plt.jpg")

df_patterns = df.groupby(['media','sentiment']).size().reset_index(name='count')
df_patterns = df_patterns.pivot(index='media', columns='sentiment', values='count')
ax = df_patterns.plot(kind='bar', figsize=(10, 6), rot=0)
plt.title("Sentiment Analysis by Media")
plt.xlabel("Media")
plt.ylabel("Count")
plt.show()



