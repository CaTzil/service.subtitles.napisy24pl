# -*- coding: utf-8 -*-
import test_helpers
from NapisyUtils import NapisyHelper

item = {'episode': '1', 'temp': False, 'title': 'Chapter 40', 'file_original_name': u'house.of.cards.s04e01.720p.mp4',
        'season': '4', 'year': '2013', 'preferredlanguage': 'eng', 'rar': False, 'tvshow': 'House of Cards (US)',
        'file_original_path': u'/Users/felixm/Desktop/tv-shows/house.of.cards/Season 4/house.of.cards.4x01.720p.webrip.x264.deflate.mp4',
        '3let_language': ['eng', 'heb', 'pol'], 'file_original_size': 913645240.32}

# item = {'episode': '', 'temp': False, 'title': 'Arrival',
#         'file_original_name': u'Arrival.2016.720p.BluRay.x264-SPARKS.mp4', 'season': '', 'year': '2016',
#         'preferredlanguage': 'eng', 'rar': False, 'tvshow': '',
#         'file_original_path': u'/Users/felixm/Desktop/movies/Arrival 2016/Arrival.2016.720p.BluRay.x264-SPARKS.mp4',
#         '3let_language': ['eng', 'heb', 'pol'], 'file_original_size': 9469434L}

# item = {'episode': '', 'temp': False, 'title': 'Avengers: Age of Ultron',
#         'file_original_name': u'The.Avengers.Age.of.Ultron.1080p.BluRay.x264-SPARKS.mp4', 'season': '', 'year': '2015',
#         'preferredlanguage': 'eng', 'rar': False, 'tvshow': '',
#         'file_original_path': u'/Users/felixm/Desktop/movies/The Avengers Age of Ultron/The.Avengers.Age.of.Ultron.1080p.BluRay.x264-SPARKS.mp4',
#         '3let_language': ['eng', 'heb', 'pol'], 'file_original_size': 9469434L}

helper = NapisyHelper()
print(helper.get_subtitle_list(item))
# print(helper.login())
