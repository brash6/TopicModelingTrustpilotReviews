import re
import pandas as pd
import nltk
from nltk.corpus import wordnet
from nltk.stem import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from spacy.lang.en import English

import constants as cst
parser = English()
porter = PorterStemmer()


def date_field(df):
    df['date'] = pd.to_datetime(df.date)
    df.sort_values(by='date', inplace=True)


def create_months(row):
    row['month_year'] = str(row['date'].month) + '-' + str(row['date'].year)
    return row


def remove_prefix(text, prefixes):
    for prefix in prefixes:
        if text.startswith(prefix):
            text = text[len(prefix):]
            return text
    return text


def extract_train_company(row, prefixes):
    row['url'] = remove_prefix(row['url'], prefixes).split('.')[0]
    return row


def clean_review(df):
    df['review'] = df['title'].map(str) + " " + df['text']
    df.drop(['title', 'text'], axis=1, inplace=True)
    # Delete punctuations and upper letters
    df['review'] = df['review'].apply(lambda x: re.sub(r'[^A-Za-z\s]', '', x))
    df['review'] = df['review'].map(lambda x: x.lower())


# A function to tokenize reviews
def tokenize(text):
    lda_tokens = []
    tokens = parser(text)
    for token in tokens:
        if token.orth_.isspace():
            continue
        elif token.like_url:
            lda_tokens.append('URL')
        elif token.orth_.startswith('@'):
            lda_tokens.append('SCREEN_NAME')
        else:
            lda_tokens.append(token.lower_)
    return lda_tokens


# A function to stem a word
def get_stem(word):
    return porter.stem(word)


def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)


# A function to lemmatize a word using POS tag
def get_lemma(word):
    return WordNetLemmatizer().lemmatize(word, get_wordnet_pos(word))


# Prepare reviews for LDA
def prepare_text_for_lda(text, en_stop):
    tokens = tokenize(text)
    tokens = [token for token in tokens if len(token) > 4]
    #tokens = [get_stem(token) for token in tokens]
    tokens = [get_lemma(token) for token in tokens]
    tokens = [token for token in tokens if token not in en_stop]
    return tokens


def apply_prepare_text_for_lda(row, en_stop):
    row['review'] = prepare_text_for_lda(row['review'], en_stop)
    return row


def full_cleaning(df):
    date_field(df)
    df = df.apply(extract_train_company, prefixes=cst.prefixes, axis=1)
    clean_review(df)
    df = df.apply(apply_prepare_text_for_lda, en_stop=cst.en_stop, axis=1)
    return df

