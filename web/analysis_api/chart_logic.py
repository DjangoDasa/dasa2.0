import bokeh as bk
import nltk
import numpy as np
import pandas as pd
import json
from collections import Counter
from bokeh.core.properties import value
from bokeh.embed import file_html
from bokeh.io import curdoc, show
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource, DataRange1d, Plot, LinearAxis, Grid
from bokeh.models.glyphs import VBar
from bokeh.plotting import figure
from bokeh.palettes import Category20c
from bokeh.resources import CDN
from bokeh.transform import cumsum
from math import pi
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s -  %(message)s')
logging.disable(logging.CRITICAL)

class Chart():

    def __init__(self, chart_type, data=None, aggregate=False):
        self.chart_type = chart_type
        self.data = data
        self.sentence_counter = 0
        self.analysis_df = pd.DataFrame()
        self.aggregate = aggregate


    def data_parser(self, data):
        logging.debug(data)
        record_obj = data
        logging.debug(record_obj['Sentences'].keys())
        for sentence in record_obj['Sentences'].keys():
            logging.debug(self.analysis_df)
            # key_list.append(sentence)
            ss = record_obj['Sentences'][sentence][1]
            logging.debug(ss)
            ss['sentence'] = sentence
            columns = ['neg', 'neu', 'pos', 'compound', 'sentence']
            self.sentence_counter += 1
            index = [self.sentence_counter]
            temp = pd.DataFrame(ss, columns=columns, index=index)
            self.analysis_df = pd.concat([self.analysis_df, temp], sort=True)
            print("Sentence is Parsed")


    def set_df_parameters(self):
        output_file(str(self.chart_type) + ".html")
        self.emotions = ['Negative', 'Neutral', 'Positive']
        self.data = {'Sentences': self.analysis_df.index,
                'Negative': self.analysis_df.neg,
                'Neutral': self.analysis_df.neu,
                'Positive': self.analysis_df.pos}
        self.colors = ["#e84d60", "#c9d9d3", "#718dbf"]


    def stacked_bar(self):
        if self.data == {} or self.data == None:
            return 'There is not data for this user'
        for record in self.data.keys():
            self.data_parser(self.data[record])
        self.set_df_parameters()
        p = figure(y_range=(0, 1.2), plot_height=500, title=str(self.aggregate) + "Sentiment Analysis",
            toolbar_location=None, tools="")
        p.vbar_stack(self.emotions, x='Sentences', width=0.9, color=self.colors, source=self.data,
                    legend=[value(x) for x in self.emotions])
        p.y_range.start = 0
        p.x_range.range_padding = 0.2
        p.xaxis.axis_label = 'Sentences'
        p.yaxis.axis_label = 'Percentage (%)'
        p.xgrid.grid_line_color = None
        p.axis.minor_tick_line_color = None
        p.outline_line_color = None
        p.legend.location = "top_left"
        p.legend.orientation = "horizontal"
        # return p
        html = file_html(p, CDN, "Stacked Bar")
        return html


    def compound_bar(self):
        if self.data == {} or self.data == None:
            return 'There is not data for this user'
        for record in self.data.keys():
            self.data_parser(self.data[record])
        output_file(str(self.chart_type) + ".html")
        source_bar = figure(plot_width=1000, plot_height=400, title="Overall Sentiment")
        source_bar.vbar(x=self.analysis_df.index, width=1, bottom=0, top=self.analysis_df['compound'], color="#718dbf")
        source_bar.xaxis.axis_label = 'Sentences'
        source_bar.yaxis.axis_label = 'Percentage'
        source_bar2 = figure(plot_width=1000, plot_height=400, title="Negative Sentiment")
        source_bar2.vbar(x=self.analysis_df.index, width=1, bottom=0, top=self.analysis_df['neg'], color="#e84d60")
        source_bar2.xaxis.axis_label = 'Sentences'
        source_bar2.yaxis.axis_label = 'Percentage'
        source_bar3 = figure(plot_width=1000, plot_height=400, title="Positive Sentiment")
        source_bar3.vbar(x=self.analysis_df.index, width=1, bottom=0, top=self.analysis_df['pos'], color="#64b479")
        source_bar3.xaxis.axis_label = 'Sentences'
        source_bar3.yaxis.axis_label = 'Percentage'
        graphs = [source_bar, source_bar2, source_bar3]
        html = file_html(graphs, CDN, "Compound bar for all")
        return html

# def stacked_bar_for_one(data):
#     """ Chart display for one analysis/one user.
#     """
#     if data == {}:
#         return 'There is not data for this user'
#     analysis_df = pd.DataFrame()
#     user_id = data.keys()
#     sentence_counter = 0
#     key_list = []
#     for key in user_id:
#         for one_record in data[key]:
#             record_obj = json.loads(one_record)
#             for sentence in record_obj['Sentences']:
#                 ss = record_obj['Sentences'][sentence]
#                 ss['sentence'] = sentence
#                 columns = ['neg', 'neu', 'pos', 'compound', 'sentence']
#                 sentence_counter += 1
#                 key_list.append(str(sentence_counter))
#                 index = [sentence_counter]
#                 temp = pd.DataFrame(ss, columns=columns, index=index)
#                 analysis_df = pd.concat([analysis_df, temp], sort=True)
#     output_file("stacked.html")
#     emotions = ['Negative', 'Neutral', 'Positive']
#     data = {'Sentences': analysis_df.index,
#             'Negative': analysis_df.neg,
#             'Neutral': analysis_df.neu,
#             'Positive': analysis_df.pos}
#     colors = ["#e84d60", "#c9d9d3", "#718dbf"]
#     p = figure(y_range=(0, 1.2), plot_height=500, title="Sentiment Analysis",
#             toolbar_location=None, tools="")
#     p.vbar_stack(emotions, x='Sentences', width=0.9, color=colors, source=data,
#                 legend=[value(x) for x in emotions])
#     p.y_range.start = 0
#     p.x_range.range_padding = 0.2
#     p.xaxis.axis_label = 'Sentences'
#     p.yaxis.axis_label = 'Percentage (%)'
#     p.xgrid.grid_line_color = None
#     p.axis.minor_tick_line_color = None
#     p.outline_line_color = None
#     p.legend.location = "top_left"
#     p.legend.orientation = "horizontal"
#     html = file_html(p, CDN, "Single User Stacked Bar")



#     print('The Stacked Bar Logic Hits')
#     return html

# def stacked_bar_for_all(data):
#     """ Chart display for get analysis for all users combined.
#     This is for the admin to view a collection of user's analysis  """
#     if data == {}:
#         return 'There is no data in the database'

#     analysis_df = pd.DataFrame()
#     user_id = data.keys()
#     sentence_counter = 0
#     key_list = []
#     for key in user_id:
#         for one_record in data[key]:
#             record_obj = json.loads(one_record)
#             for sentence in record_obj['Sentences']:
#                 # key_list.append(sentence)
#                 ss = record_obj['Sentences'][sentence]
#                 ss['sentence'] = sentence
#                 columns = ['neg', 'neu', 'pos', 'compound', 'sentence']
#                 sentence_counter += 1
#                 key_list.append(str(sentence_counter))
#                 index = [sentence_counter]
#                 temp = pd.DataFrame(ss, columns=columns, index=index)
#                 analysis_df = pd.concat([analysis_df, temp], sort=True)
#     output_file("pie.html")
#     emotions = ['Negative', 'Neutral', 'Positive']
#     data = {'Sentences': analysis_df.index,
#             'Negative': analysis_df.neg,
#             'Neutral': analysis_df.neu,
#             'Positive': analysis_df.pos}
#     colors = ["#e84d60", "#c9d9d3", "#718dbf"]
#     p = figure(y_range=(0, 1.2), plot_height=500, title="Aggregate Sentiment Analysis",
#             toolbar_location=None, tools="")
#     p.vbar_stack(emotions, x='Sentences', width=0.9, color=colors, source=data,
#                 legend=[value(x) for x in emotions])
#     p.y_range.start = 0
#     p.x_range.range_padding = 0.2
#     # p.xaxis.visible = False
#     p.xaxis.axis_label = 'Sentences'
#     p.yaxis.axis_label = 'Percentage (%)'
#     p.xgrid.grid_line_color = None
#     p.axis.minor_tick_line_color = None
#     p.outline_line_color = None
#     p.legend.location = "top_left"
#     p.legend.orientation = "horizontal"
#     html = file_html(p, CDN, "Single User Stacked Bar")
#     return html


# def pie_for_all(data):
#     if data == {}:
#         return 'There is no data in the database'
#     user_id = data.keys()
#     sentence_counter = 0
#     key_list = []

#     neg_agg, pos_agg, neu_agg = 0, 0, 0
#     for key in user_id:
#         for one_record in data[key]:
#             record_obj = json.loads(one_record)
#             for sentence in record_obj['Sentences']:
#                 ss = record_obj['Sentences'][sentence]
#                 neg_agg += ss['neg']
#                 pos_agg += ss['pos']
#                 neu_agg += ss['neu']
#     data_analysis = {'Negative': neg_agg, 'Positive': pos_agg, 'Neutral': neu_agg}
#     x = Counter(data_analysis)

#     df_analysis = pd.DataFrame.from_dict(dict(x), orient='index').reset_index().rename(index=str, columns={0:'value', 'index':'sentiment'})
#     df_analysis['angle'] = df_analysis['value']/sum(x.values()) * 2*pi
#     df_analysis['color'] = Category20c[len(x)]

#     p = figure(plot_height=350, title="Aggregate Sentiment Analysis", toolbar_location=None)
#     p.wedge(x=0, y=1, radius=0.4,
#             start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
#             line_color="white", fill_color='color', legend='sentiment', source=df_analysis)

#     p.axis.axis_label=None
#     p.axis.visible=False
#     p.grid.grid_line_color = None

#     html = file_html(p, CDN, "All Users Pie")
#     return html


# def compound_for_all(data):
#     if data == {}:
#         return 'There is not data for this user'
#     analysis_df = pd.DataFrame()
#     user_id = data.keys()
#     sentence_counter = 0
#     key_list = []
#     for key in user_id:
#         for one_record in data[key]:
#             record_obj = json.loads(one_record)
#             for sentence in record_obj['Sentences']:
#                 # key_list.append(sentence)
#                 ss = record_obj['Sentences'][sentence]
#                 ss['sentence'] = sentence
#                 columns = ['neg', 'neu', 'pos', 'compound', 'sentence']
#                 sentence_counter += 1
#                 key_list.append(str(sentence_counter))
#                 index = [sentence_counter]
#                 temp = pd.DataFrame(ss, columns=columns, index=index)
#                 analysis_df = pd.concat([analysis_df, temp], sort=True)
#     output_file("stacked.html")

#     source_bar = figure(plot_width=1000, plot_height=400, title="Compound Bar for All Users")
#     source_bar.vbar(x=analysis_df.index, width=1, bottom=0, top=analysis_df['compound'], color="#718dbf")
#     source_bar.xaxis.axis_label = 'Sentences'
#     source_bar.yaxis.axis_label = 'Percentage'
#     source_bar2 = figure(plot_width=1000, plot_height=400, title="Negative Bar for All Users")
#     source_bar2.vbar(x=analysis_df.index, width=1, bottom=0, top=analysis_df['neg'], color="#e84d60")
#     source_bar2.xaxis.axis_label = 'Sentences'
#     source_bar2.yaxis.axis_label = 'Percentage'
#     source_bar3 = figure(plot_width=1000, plot_height=400, title="Positive Bar for All Users")
#     source_bar3.vbar(x=analysis_df.index, width=1, bottom=0, top=analysis_df['pos'], color="#64b479")
#     source_bar3.xaxis.axis_label = 'Sentences'
#     source_bar3.yaxis.axis_label = 'Percentage'
#     graphs = [source_bar, source_bar2, source_bar3]
#     html = file_html(graphs, CDN, "Compound bar for all")
#     return html

