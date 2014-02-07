#!/usr/bin/env python

import argparse
import os
import re
import sys

import whoosh
import whoosh.analysis
import whoosh.index
import whoosh.fields

from whoosh.support.charset import accent_map


def create_index_writer(index_path):
    '''Create a new whoosh index in the given directory path.
    
    Input: directory in which to create the index
    
    Output: `whoosh.index` writer object
    '''
    

    if not os.path.exists(index_path):
        os.mkdir(index_path)


    analyzer = (whoosh.analysis.StemmingAnalyzer() | 
                whoosh.analysis.CharsetFilter(accent_map))

    schema = whoosh.fields.Schema(track_id      = whoosh.fields.TEXT(stored=True),
                                  song_id       = whoosh.fields.TEXT(stored=True),
                                  artist_name   = whoosh.fields.TEXT(stored=True, analyzer=analyzer),
                                  title         = whoosh.fields.TEXT(stored=True, analyzer=analyzer))

    index = whoosh.index.create_in(index_path, schema)

    return index.writer()


def create_track_index(unique_tracks='', index_dir=''):
    '''Create the full-text index using whoosh'''

    writer = create_index_writer(index_dir)

    splitter = re.compile('<SEP>')

    with open(unique_tracks, 'r') as track_file:
        for line in track_file:
            track_id, song_id, artist_name, title = splitter.split(unicode(line.strip(), errors='ignore'), 4)

            writer.add_document(track_id=track_id, 
                                song_id=song_id, 
                                artist_name=artist_name,
                                title=title)

    writer.commit()

def process_arguments(args):
    '''Command-line argument parsing'''
    
    parser = argparse.ArgumentParser(description='''Full-text index of the million song dataset's metadata''')

    parser.add_argument('unique_tracks', action='store',
                        help = 'path to unique_tracks.txt')
    
    parser.add_argument('index_dir', action='store',
                        help = 'path to create the fulltext index')

    return vars(parser.parse_args(args))

if __name__ == '__main__':
    args = process_arguments(sys.argv[1:])

    create_track_index(**args)

