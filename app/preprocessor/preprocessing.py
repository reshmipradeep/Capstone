# -*- coding: utf-8 -*-
import pandas as pd
from emoji import UNICODE_EMOJI
import emoji
import re
import nltk
from ekphrasis.classes.segmenter import Segmenter
from nltk.corpus import stopwords
import string #load punctuation charachers

df=pd.read_csv(r'data\threads_data\new.csv')

"""**Preprocessing**"""

df["clean"] = df["Caption"].apply(lambda x: emoji.demojize(str(x).encode('utf-8').decode('utf-8', 'ignore')) if pd.notna(x) and isinstance(x, str) else '')
#remove underscores(for emojis)
df["clean"]=df["clean"].apply(lambda x: re.sub(r"_",' ',x))

# Remove unwanted characters
df["clean"] = df["clean"].apply(lambda x: re.sub(r"\d+", '', str(x)))
df["clean"] = df["clean"].apply(lambda x: re.sub(r"[^a-zA-Z\s]", '', str(x)))
df["clean"] = df["clean"].apply(lambda x: re.sub(r"[^\w\s]", '', str(x)))  # Remove non-word characters (including ðŸ’Ž)

#remove urls in data
df["clean"]=df["clean"].apply(lambda x: re.sub(r"\bhttp\w*\b",'',x))

#removing @tags
df["clean"]=df["clean"].apply(lambda x: re.sub(r"@(\w+)",'',x))

#removing hashtags
df["clean"]=df["clean"].apply(lambda x: re.sub(r"#(\w+)",'',x))

"""
#segmenting hashtags
df.insert(7, 'Segmented#', None)
#segmenter using the word statistics from Twitter
seg_tw = Segmenter(corpus="twitter")

a = []
for i in range(len(df)):
 if df['hashtags'][i] != a:
  listToStr1 = ' '.join([str(elem) for elem in df['hashtags'][i]])
  df.loc[i,'Segmented#'] = seg_tw.segment(listToStr1)"""

#tokenize data Caption 
df["clean"]=df["clean"].apply(lambda x: nltk.word_tokenize(str(x).lower()))

#remove stopwords and punctuations
stopwrds = set(stopwords.words('english'))

df["clean"]=df["clean"].apply(lambda x: [y for y in x if (y not in stopwrds)])
df["clean"]=df["clean"].apply(lambda x: [re.sub(r'['+string.punctuation+']','',y) for y in x])
df["clean"]=df["clean"].apply(lambda x: [re.sub('\\n','',y) for y in x])

#replacing nan values with empty string
df['clean'] = df['clean'].fillna('')
#clean unneeded spaces or empty columns or non sense words
df=df[["Username","clean"]]

#convert tokenize threads to sentences
df["clean"]=df["clean"].apply(lambda x: ' '.join(x).replace('\\n',''))
"""
#adding segmented hastags
df['Segmented#'] = df['Segmented#']. fillna('')
df["clean"] = df[["clean", "Segmented#"]].apply(" ".join, axis=1)"""
print(df)
#save clean threads
#data
df.to_csv(r"data\preprocessed_data.csv",index=False,encoding="utf-8")
