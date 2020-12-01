import pandas as pd
import os
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from matplotlib.ticker import FuncFormatter
import matplotlib.colors as mcolors
from collections import Counter
import pyLDAvis.gensim

import constants as cst
import data_cleaning


def plot_occ_over_time(df_reviews, title):
    df_reviews = df_reviews.apply(data_cleaning.create_months, axis=1)
    df_occ = df_reviews[['month_year', 'date']]
    xaxis = "Month-Year"
    df_occ = df_occ.rename(columns={"month_year": xaxis})
    df_occ_count_class = df_occ[xaxis].value_counts().to_frame().reset_index(level=0)
    df_occ_count_class['index'] = pd.to_datetime(df_occ_count_class['index'])
    df_occ_count_class = df_occ_count_class.sort_values(by='index')
    fig = px.bar(x=df_occ_count_class["index"], y=df_occ_count_class[xaxis], labels={'x': str(xaxis), 'y':'Occurence'},
                 title=title,
                 opacity=0.75, width=1000, height=500)
    fig.show(renderer="notebook")


def plot_occ(df, xaxis, title, c='company'):
    if c == "company":
        occs = df['url'].to_numpy()
    else:
        occs = df['stars'].to_numpy()
    df_occ = pd.DataFrame(occs)
    df_occ = df_occ.rename(columns={0: xaxis})
    df_occ_count_class = df_occ[xaxis].value_counts().to_frame().reset_index(level=0)
    fig = px.bar(x=df_occ_count_class["index"], y=df_occ_count_class[xaxis],
                 labels={'x': str(xaxis), 'y': 'Occurence'},
                 title=title,
                 opacity=0.75, width=1000, height=500)
    fig.show()


def plot_ratings_per_company(df):
    fig = px.box(df, x="url", y="stars", width=1000, height=500)
    fig.show()


def wordcloud_topics_viz(model):
    cols = [color for name, color in mcolors.TABLEAU_COLORS.items()]  # more colors: 'mcolors.XKCD_COLORS'

    cloud = WordCloud(stopwords=cst.en_stop,
                      background_color='white',
                      width=2500,
                      height=1800,
                      max_words=15,
                      colormap='tab10',
                      color_func=lambda *args, **kwargs: cols[i],
                      prefer_horizontal=1.0)

    topics = model.show_topics(formatted=False, num_words=15)

    fig, axes = plt.subplots(int(len(topics)/2), 2, figsize=(10,10), sharex=True, sharey=True)

    for i, ax in enumerate(axes.flatten()):
        fig.add_subplot(ax)
        topic_words = dict(topics[i][1])
        cloud.generate_from_frequencies(topic_words, max_font_size=300)
        plt.gca().imshow(cloud)
        plt.gca().set_title('Topic ' + str(i), fontdict=dict(size=16))
        plt.gca().axis('off')

    plt.subplots_adjust(wspace=0, hspace=0)
    plt.axis('off')
    plt.margins(x=0, y=0)
    plt.tight_layout()
    plt.show()


def viz_evolution_wordclouds(time_periods, models):
    for i in range(len(models)):
        print("Between " + time_periods[i] + " and " + time_periods[i+1])
        wordcloud_topics_viz(models[i])


def viz_wordcount_importance_keywords(model, reviews):
    topics = model.show_topics(formatted=False)
    data_flat = [w for w_list in reviews for w in w_list]
    counter = Counter(data_flat)

    out = []
    for i, topic in topics:
        for word, weight in topic:
            out.append([word, i , weight, counter[word]])

    df = pd.DataFrame(out, columns=['word', 'topic_id', 'importance', 'word_count'])

    # Plot Word Count and Weights of Topic Keywords
    fig, axes = plt.subplots(int(len(topics)/2), 2, figsize=(16,10), sharey=True, dpi=160)
    cols = [color for name, color in mcolors.TABLEAU_COLORS.items()]
    for i, ax in enumerate(axes.flatten()):
        ax.bar(x='word', height="word_count", data=df.loc[df.topic_id==i, :], color=cols[i], width=0.5, alpha=0.3, label='Word Count')
        ax_twin = ax.twinx()
        ax_twin.bar(x='word', height="importance", data=df.loc[df.topic_id==i, :], color=cols[i], width=0.2, label='Weights')
        ax.set_ylabel('Word Count', color=cols[i])
        ax_twin.set_ylim(0, 0.030); ax.set_ylim(0, max(df['word_count']+150))
        ax.set_title('Topic: ' + str(i), color=cols[i], fontsize=16)
        ax.tick_params(axis='y', left=False)
        ax.set_xticklabels(df.loc[df.topic_id==i, 'word'], rotation=30, horizontalalignment= 'right')
        ax.legend(loc='upper left'); ax_twin.legend(loc='upper right')

    fig.tight_layout(w_pad=2)
    fig.suptitle('Word Count and Importance of Topic Keywords', fontsize=22, y=1.05)
    plt.show()


def viz_evolution_wordcounts_importance(time_periods, models, reviews_list):
    for i in range(len(models)):
        print("Between " + time_periods[i] + " and " + time_periods[i+1])
        viz_wordcount_importance_keywords(models[i], reviews_list[i])


def topics_per_document(model, corpus, start=0, end=1):
    corpus_sel = corpus[start:end]
    dominant_topics = []
    topic_percentages = []
    for i, corp in enumerate(corpus_sel):
        topic_percs, wordid_topics, wordid_phivalues = model[corp]
        dominant_topic = sorted(topic_percs, key = lambda x: x[1], reverse=True)[0][0]
        dominant_topics.append((i, dominant_topic))
        topic_percentages.append(topic_percs)
    return(dominant_topics, topic_percentages)


def viz_most_discussed_topics(model, corpus, max_occ=2500):
    dominant_topics, topic_percentages = topics_per_document(model=model, corpus=corpus, end=-1)

    # Distribution of Dominant Topics in Each Document
    df = pd.DataFrame(dominant_topics, columns=['Document_Id', 'Dominant_Topic'])
    dominant_topic_in_each_doc = df.groupby('Dominant_Topic').size()
    df_dominant_topic_in_each_doc = dominant_topic_in_each_doc.to_frame(name='count').reset_index()
    max_occ = max(df_dominant_topic_in_each_doc['count']) + 100

    # Total Topic Distribution by actual weight
    topic_weightage_by_doc = pd.DataFrame([dict(t) for t in topic_percentages])
    df_topic_weightage_by_doc = topic_weightage_by_doc.sum().to_frame(name='count').reset_index()

    # Top 3 Keywords for each Topic
    topic_top3words = [(i, topic) for i, topics in model.show_topics(formatted=False)
                       for j, (topic, wt) in enumerate(topics) if j < 3]

    df_top3words_stacked = pd.DataFrame(topic_top3words, columns=['topic_id', 'words'])
    df_top3words = df_top3words_stacked.groupby('topic_id').agg(', \n'.join)
    df_top3words.reset_index(level=0, inplace=True)

    # Plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6), dpi=120, sharey=True)

    # Topic Distribution by Dominant Topics
    ax1.bar(x='Dominant_Topic', height='count', data=df_dominant_topic_in_each_doc, width=.5, color='firebrick')
    ax1.set_xticks(range(df_dominant_topic_in_each_doc.Dominant_Topic.unique().__len__()))
    tick_formatter = FuncFormatter(
        lambda x, pos: 'Topic ' + str(x) + '\n' + df_top3words.loc[df_top3words.topic_id == x, 'words'].values[0])
    ax1.xaxis.set_major_formatter(tick_formatter)
    ax1.set_title('Number of Documents by Dominant Topic', fontdict=dict(size=10))
    ax1.set_ylabel('Number of Documents')
    ax1.set_ylim(0, max_occ)

    # Topic Distribution by Topic Weights
    ax2.bar(x='index', height='count', data=df_topic_weightage_by_doc, width=.5, color='steelblue')
    ax2.set_xticks(range(df_topic_weightage_by_doc.index.unique().__len__()))
    ax2.xaxis.set_major_formatter(tick_formatter)
    ax2.set_title('Number of Documents by Topic Weightage', fontdict=dict(size=10))

    plt.show()



def viz_evolution_discussed_topics(time_periods, models, corpus):
    for i in range(len(models)):
        print("Between " + time_periods[i] + " and " + time_periods[i+1])
        viz_most_discussed_topics(models[i], corpus[i])


def export_LDAvis_html(ldamodel, corpus, id2word, title):
    LDAvis_prepared = pyLDAvis.gensim.prepare(ldamodel, corpus=corpus, dictionary=id2word,
                                              sort_topics=False)
    # Save the visualization to html
    pyLDAvis.save_html(LDAvis_prepared, os.path.join(cst.VIZ, title))


def export_evolution_LDAvis_html(time_periods, models, corpus, id2words, pos=True):
    for i in range(len(models)):
        if pos:
            title = 'pos_lda_' + time_periods[i] + '.html'
        else:
            title = 'neg_lda_' + time_periods[i] + '.html'
        export_LDAvis_html(models[i], corpus[i], id2words[i], title)

