#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from __future__ import print_function

import os
import datetime
import yaml
import collections

import get_credential


def get_title_from_summary(summary):
    contents = summary.split(',')
    titles = [c.split(':')[0].lower() for c in contents]
    return collections.Counter(titles).keys()[0]


def change_events():
    # get colors data
    fpath = os.path.expanduser('~')
    with open(fpath + '/.events_config.yml', 'rb') as f:
        config = yaml.load(f)

    service = get_credential.credential("")
    page_token = None
    today = datetime.date.today()
    change_start = today - datetime.timedelta(days=2)
    change_end = today + datetime.timedelta(days=2)
    while True:
        events = service.events().list(
                calendarId='primary',
                pageToken=page_token,
                timeMin=change_start.strftime('%Y-%m-%dT00:00:00+09:00'),
                timeMax=change_end.strftime('%Y-%m-%dT00:00:00+09:00'),
                ).execute()
        for event in events['items']:
            if 'summary' not in event:
                continue
            summary = event['summary'].lower()
            title = get_title_from_summary(summary)
            summary = summary.replace(title,
                config['alias'].get(title, title))
            for color, rules in config['color_rules'].items():
                if title in rules:
                    # change color
                    event['colorId'] = config['colors'][color]
                    break
            # change summary
            event['summary'] = summary.capitalize()
            service.events().update(
                calendarId='primary',
                eventId=event['id'],
                body=event,
                ).execute()
        page_token = events.get('nextPageToken')
        if not page_token:
            break


if __name__ == '__main__':
    change_events()
