import random

import pandas as pd
import markovify
import spacy
import re
import os
import pandas
import numpy
import warnings
warnings.filterwarnings('ignore')
from time import time
import gc
import json


class text_generation():
    def open_csv(self, path):
        path_to_csv = path
        if os.path.isfile(path_to_csv):
            comments = pd.read_csv(path_to_csv)
            comments.columns = ["commentBody"]
        return comments

    def preprocess(self, comments):
        commentBody = comments['commentBody']
        commentBody = commentBody.str.replace("(<br/>)", "")
        commentBody = commentBody.str.replace('(<a).*(>).*(</a>)', '')
        commentBody = commentBody.str.replace('(&amp)', '')
        commentBody = commentBody.str.replace('(&gt)', '')
        commentBody = commentBody.str.replace('(&lt)', '')
        commentBody = commentBody.str.replace('.', '. ')
        commentBody = commentBody.str.replace('(\xa0)', ' ')
        return commentBody

    def train_me(self, comments):
        commentBody = self.preprocess(comments)
        text_from_df = ''
        for item in commentBody:
            text_from_df += str(item)

        comments_generator = markovify.Text(text_from_df, state_size=2)
        return comments_generator

    def get_files(self, path_to_summary):
        with open(path_to_summary) as file:
            summary = file.read()

        summary = summary.split("\n")
        filenames = {}
        for i in summary:
            t = i.split(', ')
            filenames[t[0]+".json"] = t[1]
        return filenames

    def count_rooms(self, filenames):
        rooms = {}
        for i in set(filenames.values()):
            c = 0
            for j in list(filenames.values()):
                if i == j:
                    c = c + 1
            rooms[i] = c
        return rooms

    def get_jroom(self, rooms):
        jrooms = []
        for i in range(len(list(rooms.keys()))):
            room = str(list(rooms.values())[i]) + ' ' + list(rooms.keys())[i]
            room = room.replace('_', ' ')
            jrooms.append(room)
        return jrooms


    def get_number_rooms(self, rooms):
        numbers = list(rooms.values())
        rooms = list(rooms.keys())
        return numbers, rooms

    def do_sth(self, numbers, rooms):
        # Sorry for the naming the time was limited...
        begin = []
        for i in range(len(rooms)):
            room = str(numbers[i]) + ' ' + rooms[i]
            room = room.replace('_room', '')
            room = room.replace('1 b', 'one b')
            room = room.replace('1 ', '')
            room = room.replace('one', '1')
            begin.append(room)
        return begin

    def do_sth_2(self, comments_generator, begin):
        description = []
        description.append(comments_generator.make_sentence_with_start('Located'))
        for i in begin:
            try:
                description.append(comments_generator.make_sentence_with_start(i))
            except KeyError:
                continue

        description.append(comments_generator.make_sentence_with_start('Close'))

        description = [sent for sent in description if sent is not None]
        description = ' '.join(description)
        return description
