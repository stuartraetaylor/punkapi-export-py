#!/usr/bin/env python3

import argparse
import logging
import requests
import json
import re

def beers(payload):
    if not payload:
        return request('beers/random')
    else:
        return request('beers', payload)

def request(endpoint, payload = {}):
    r = requests.get('https://api.punkapi.com/v2/' + endpoint, params=payload) 
    logging.info('Request: %s', r.url)

    json = r.json()

    if (r.status_code != 200):
        print('Error: ' + json['error'])
        print(json['message'])
        return {}

    return {
        'beers': json,
        'remaining': r.headers['X-RateLimit-Remaining']
    }

def export(beer, format = 'json'):
    print('Found: ' + beer['name'])

def format(s):
    if s is None:
        return s
    return re.sub('\s+', '_', s.strip())

def main():
    parser = argparse.ArgumentParser(
        description='Exports beers from the Punk API - https://punkapi.com')
    parser.add_argument('beer_name',
        nargs='?',
        metavar='beer_name',
        help='Name of the beer, e.g., Punk IPA')
    parser.add_argument("-f", "--format",
        default="json",
        metavar="format",
        help="Export format (default: %(default)s)")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    print()
    print('Punk API Export!')
    print('================')
   
    searching = '*random*'
    payload = {}

    if args.beer_name is not None:
        searching = '"'+args.beer_name+'"'
        payload['beer_name'] = format(args.beer_name)
        
    print('Searching: ' + searching)
    print()
    
    result = beers(payload)
    if not result['beers']:
        print('No beer found.')
        exit(1)

    for beer in result['beers']:
        export(beer)

    print()
    print('Remaining requests: ' + result['remaining'])


main()

