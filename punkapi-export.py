#!/usr/bin/env python3

import argparse
import logging
import requests
import json
import re

def beers(payload = {}):
    if not payload:
        return request('beers/random')
    else:
        return request('beers', payload)

def request(endpoint, payload = {}):
    r = requests.get('https://api.punkapi.com/v2/' + endpoint, params=payload) 
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
    return re.sub('\s+', '_', s.strip())

def main():
    parser = argparse.ArgumentParser(
        description='Exports beers from the Punk API - https://punkapi.com')
    parser.add_argument('beer_name',
        metavar='beer_name',
        help='Beer name, e.g., Punk IPA')
    parser.add_argument("-f", "--format",
        default="json",
        metavar="format",
        help="Export format (default: %(default)s)")
    args = parser.parse_args()

    print()
    print('Punk API Export!')
    print('================')
    print('Searching: ' + args.beer_name)
    print()
    
    payload = {
        'beer_name': format(args.beer_name)
    }

    result = beers(payload)
    if not result['beers']:
        print('No beer found.')
        exit(1)

    for beer in result['beers']:
        export(beer)

    print()
    print('Requests remaining: ' + result['remaining'])


main()

