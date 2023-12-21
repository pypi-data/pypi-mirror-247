# bertopic_viz.py
#    
# WordTM: Show a network graph of topic-word from a BERTopic model
#
# Copyright (C) 2022-2023 WordTM Project
# Author: Johnny Cheng <johnnywfc@gmail.com>
# Updated: 15 October 2023
#
# URL:  nil
# For license information, see LICENSE.TXT

import warnings
warnings.filterwarnings("ignore")

from bertopic import BERTopic
import networkx as nx
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import math

ntopic = 5   # no of topics
nword = 7   # no of words from each topic

# A rainbow color mapping using matplotlib's tableau colors
color_list = ["red", "orange", "yellow", "green", "lime", "blue", "purple"]

def get_topic_word(model_path):
    """Build a topic-word dictionary from the topics and their relevant words
       of a BERTopic model"""

    topic_model = BERTopic.load(model_path)
    topics = topic_model.get_topics()

    topic_words = [[words for words, _ in topics[topic]] 
                   for topic in range(ntopic)]

    topic_word_dict = {}
    for i, words in enumerate(topic_words):
        topic_word_dict['Topic'+str(i)] = words[:nword]

    return topic_word_dict


def plot_graph(topic_word_dict):
    """Plot a network graph with NetworkX from a topic-word dictionary
       through a circular layout"""

    topic_list = []
    word_list = []
    for topic, words in topic_word_dict.items():
        topic_list.append(topic)
        word_list += words[:nword]

    word_list = list(set(word_list))

    # Create a graph object
    G = nx.Graph()

    # Add nodes to the graph
    for word in word_list:
        G.add_node(word, label=word, type="word", color='springgreen')
    for topic in topic_list:
        G.add_node(topic, label=topic, type="topic", color='orange')

    # Calculate the positions of the nodes
    inner_pos = nx.circular_layout(word_list)

    # Calculate the positions of the outer nodes in a circular layout
    outer_pos = {}
    angle = 2 * math.pi / len(topic_list)
    radius = 1.5

    for i, word in enumerate(topic_list):
        theta = i * angle
        x = radius * math.cos(theta)
        y = radius * math.sin(theta)
        outer_pos[word] = (x, y)

    # Add edges connecting inner and outer nodes
    for i, topic in enumerate(topic_list):
        for word in topic_word_dict[topic]:
            G.add_edge(topic, word, color=color_list[i])

    ncolors = [G.nodes[node]['color'] for node in G.nodes]

    edges = G.edges()
    ecolors = [G[u][v]['color'] for u, v in edges]

    pos = inner_pos
    pos.update(outer_pos)

    plt.figure(figsize=(12,10))
    labels = nx.get_node_attributes(G, 'label')
    nx.draw_networkx(G, pos, labels=labels, node_size=400, \
                     node_color=ncolors, edge_color=ecolors, \
                     font_size=8, font_family='Microsoft JhengHei', \
                     font_weight='normal')

    # Set the aspect ratio to equal and show the plot
    plt.axis('equal')

    return plt


def plot_igraph(topic_word_dict):
    """Plot a network graph with Plotly from a topic-word dictionary
       through a circular layout"""

    topic_list = []
    word_list = []
    for topic, words in topic_word_dict.items():
        topic_list.append(topic)
        word_list += words[:nword]

    word_list = list(set(word_list))

    # Build word-topic dictionary
    word_topic_dict = {}
    for topic, words in topic_word_dict.items():
        for word in words:
            if word in word_topic_dict:
                word_topic_dict[word].append(topic)
            else:
                word_topic_dict[word] = [topic]

    total_nodes = len(word_list) + len(topic_list)
    inner_nodes = len(word_list)
    outer_nodes = len(topic_list)

    inner_angles = [i * 2 * math.pi / inner_nodes for i in range(inner_nodes)]
    outer_angles = [i * 2 * math.pi / outer_nodes for i in range(outer_nodes)]

    inner_x = [math.cos(angle) for angle in inner_angles]
    inner_y = [math.sin(angle) for angle in inner_angles]
    outer_x = [1.5 * math.cos(angle) for angle in outer_angles]
    outer_y = [1.5 * math.sin(angle) for angle in outer_angles]

    fig = go.Figure()

    for i in range(inner_nodes):
        fig.add_trace(go.Scatter(
            x=[inner_x[i]],
            y=[inner_y[i]],
            mode='markers+text',
            text=word_list[i],
            textposition='middle center',  # Set the position of the labels
            hoverinfo='text',
            marker=dict(
                size=30,
                color='lime'
            ),
            hovertemplate=f"{word_list[i]} : {word_topic_dict[word_list[i]]}",
        ))

    for i in range(outer_nodes):
        fig.add_trace(go.Scatter(
            x=[outer_x[i]],
            y=[outer_y[i]],
            mode='markers+text',
            text=topic_list[i],
            hoverinfo='text',
            marker=dict(
                size=40,
                color='cyan'
            ),
            hovertemplate=f"{'Topic'+str(i)} : {topic_word_dict['Topic'+str(i)]}",
        ))

    for i in range(outer_nodes):
        for word in topic_word_dict[topic_list[i]]:
            j = word_list.index(word)
            fig.add_trace(go.Scatter(
                x=[outer_x[i], inner_x[j]],
                y=[outer_y[i], inner_y[j]],
                mode='lines',
                hoverinfo='none',
                line=dict(
                    color=color_list[i],
                    width=1
                )
            ))

    fig.update_layout(
        showlegend=False,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        plot_bgcolor='white',
        width=800,
        height=800
    )

    return fig
