import heapq
import numpy as np
import plotly.graph_objects as go
from gensim import corpora
from gensim.models.ldamulticore import LdaMulticore
from gensim.models import CoherenceModel

import constants as cst
import data_cleaning
import visualizations


# Defining a function to get coherence score
def my_coherence_vals(dictionary, corpus, texts, limit, start, step):
    coherence_values = []
    model_list = []
    for num_topics in range(start, limit, step):
        model = LdaMulticore(corpus=corpus, num_topics=num_topics, id2word=dictionary,
                             chunksize=2000, passes=50, per_word_topics=True)
        model_list.append(model)
        coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
        coherence_values.append(coherencemodel.get_coherence())

    return model_list, coherence_values


# Function to return and visualize best model in term of coherence
def viz_best_coherence(id2word, corpus, texts, start=4, limit=9, step=2):
    model_list, coherence_values = my_coherence_vals(id2word, corpus,
                                                     texts, limit, start, step)
    colors = ['lightslategray', ] * (limit - start)
    index_of_best = coherence_values.index(max(coherence_values))
    best_indexes = heapq.nlargest(2, range(len(coherence_values)), key=coherence_values.__getitem__)
    if (abs(coherence_values[best_indexes[0]] - coherence_values[best_indexes[1]]) < 0.01) and (
            best_indexes[0] < best_indexes[1]):
        index_of_best = best_indexes[1]
    colors[index_of_best] = 'crimson'
    fig = go.Figure(data=[go.Bar(
        x=np.arange(start, limit, step),
        y=coherence_values,
        marker_color=colors,
    )])
    fig.update_layout(title_text='Model coherence with different number of topics', width=1000, height=500)
    fig.show()
    return model_list[index_of_best]


def create_dict_corpus(df):
    reviews = df['review']
    # Create Dictionary
    id2word = corpora.Dictionary(reviews)
    # Create Corpus: Term Document Frequency
    corpus = [id2word.doc2bow(review) for review in reviews]
    return reviews, id2word, corpus


def create_dicts(time_periods, df_pos_reviews, df_neg_reviews):
    """
    time_periods : List of sorted dates which includes start and end dates, for example ["2015", "2017", "02-2020", "12-2020"]
    """
    df_dicts = {}
    df_dicts['pos'] = {}
    df_dicts['neg'] = {}
    for i in range(len(time_periods)):
        if i < len(time_periods) - 1:
            # Positive reviews
            df_dicts['pos'][time_periods[i] + '_' + time_periods[i + 1]] = {}
            df_dicts['pos'][time_periods[i] + '_' + time_periods[i + 1]]['df'] = df_pos_reviews[
                (df_pos_reviews['date'] >= time_periods[i])
                & (df_pos_reviews['date'] < time_periods[i + 1])]
            reviews_pos, id2word_pos, corpus_pos = \
                create_dict_corpus(df_dicts['pos'][time_periods[i] + '_' + time_periods[i + 1]]['df'])
            df_dicts['pos'][time_periods[i] + '_' + time_periods[i + 1]]['reviews'] = reviews_pos
            df_dicts['pos'][time_periods[i] + '_' + time_periods[i + 1]]['id2word'] = id2word_pos
            df_dicts['pos'][time_periods[i] + '_' + time_periods[i + 1]]['corpus'] = corpus_pos

            # Negative Reviews
            df_dicts['neg'][time_periods[i] + '_' + time_periods[i + 1]] = {}
            df_dicts['neg'][time_periods[i] + '_' + time_periods[i + 1]]['df'] = df_neg_reviews[
                (df_neg_reviews['date'] >= time_periods[i])
                & (df_neg_reviews['date'] < time_periods[i + 1])]
            reviews_neg, id2word_neg, corpus_neg = \
                create_dict_corpus(df_dicts['neg'][time_periods[i] + '_' + time_periods[i + 1]]['df'])
            df_dicts['neg'][time_periods[i] + '_' + time_periods[i + 1]]['reviews'] = reviews_neg
            df_dicts['neg'][time_periods[i] + '_' + time_periods[i + 1]]['id2word'] = id2word_neg
            df_dicts['neg'][time_periods[i] + '_' + time_periods[i + 1]]['corpus'] = corpus_neg
    return df_dicts


def train_ldas(time_periods, df_pos_reviews, df_neg_reviews):
    df_dicts = create_dicts(time_periods, df_pos_reviews, df_neg_reviews)
    for i in range(len(time_periods)):
        if i < len(time_periods) - 1:
            # Positive reviews
            print("Training LDA for positive reviews of " + time_periods[i] + '_' + time_periods[i + 1] + " period")
            df_dicts['pos'][time_periods[i] + '_' + time_periods[i + 1]]['model'] = viz_best_coherence(
                df_dicts['pos'][time_periods[i] + '_' + time_periods[i + 1]]['id2word'],
                corpus=df_dicts['pos'][time_periods[i] + '_' + time_periods[i + 1]]['corpus'],
                texts=df_dicts['pos'][time_periods[i] + '_' + time_periods[i + 1]]['reviews'])

            # Negative reviews
            print("Training LDA for negative reviews of " + time_periods[i] + '_' + time_periods[i + 1] + " period")
            df_dicts['neg'][time_periods[i] + '_' + time_periods[i + 1]]['model'] = viz_best_coherence(
                df_dicts['neg'][time_periods[i] + '_' + time_periods[i + 1]]['id2word'],
                corpus=df_dicts['neg'][time_periods[i] + '_' + time_periods[i + 1]]['corpus'],
                texts=df_dicts['neg'][time_periods[i] + '_' + time_periods[i + 1]]['reviews'])
    return df_dicts


def get_models_corpus_reviewslists(dict_models_over_time, pos=True):
    models = []
    corpus = []
    id2words = []
    reviews_lists = []
    if pos:
        for key in dict_models_over_time['pos']:
            models.append(dict_models_over_time['pos'][key]['model'])
            corpus.append(dict_models_over_time['pos'][key]['corpus'])
            id2words.append(dict_models_over_time['pos'][key]['id2word'])
            reviews_lists.append(dict_models_over_time['pos'][key]['reviews'])
    else:
        for key in dict_models_over_time['neg']:
            models.append(dict_models_over_time['neg'][key]['model'])
            corpus.append(dict_models_over_time['neg'][key]['corpus'])
            id2words.append(dict_models_over_time['neg'][key]['id2word'])
            reviews_lists.append(dict_models_over_time['neg'][key]['reviews'])
    return models, corpus, id2words, reviews_lists
