#!/usr/bin/env python

import argparse
import sys
import whoosh
import whoosh.index
import whoosh.query
import whoosh.qparser

from pprint import pprint

def search_tracks(index, title=None, artist=None, num_results=None):
    '''Search an MSD track index'''

    
    if artist:
        q_artist = whoosh.qparser.QueryParser('artist_name', index.schema).parse(artist)

    if title:
        q_title  = whoosh.qparser.QueryParser('title', index.schema).parse(title)

    # Merge the queries
    if title and artist:
        q = whoosh.query.And([q_artist, q_title])
    elif title:
        q = q_title
    elif artist:
        q = q_artist
    else:
        raise ValueError('Invalid query')

    with index.searcher() as search:
        return [dict(item) for item in search.search(q, limit=num_results)]

    # No results
    return []


def process_arguments(args):

    parser = argparse.ArgumentParser(description='''Search the MSD track metadata index''')

    parser.add_argument('index_dir', 
                        action='store',
                        help='path to the fulltext index')

    parser.add_argument('-a', '--artist', 
                        action='store', 
                        dest='artist', 
                        type=unicode, 
                        help='artist search string', 
                        default=None,
                        required=False)

    parser.add_argument('-t', '--title', 
                        action='store', 
                        dest='title', 
                        type=unicode, 
                        help='title search string', 
                        default=None,
                        required=False)

    parser.add_argument('-n', '--num_results', 
                        action='store', 
                        dest='num_results', 
                        type=int, 
                        help='maximum number of results', 
                        default=None,
                        required=False)

    return vars(parser.parse_args(args))

if __name__ == '__main__':
    
    args = process_arguments(sys.argv[1:])

    index = whoosh.index.open_dir(args['index_dir'])

    results = search_tracks(index, 
                            artist=args['artist'], 
                            title=args['title'], 
                            num_results=args['num_results'])

    pprint(results)

