#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from __future__ import division, print_function, unicode_literals
import time
import datetime

import get_credential

__author__ = 'www.kentaro.wada@gmail.com (Kentaro Wada)'


def summarize_spent(period_start):
    """Summarize spent time with given period start"""
    period_end = period_start + datetime.timedelta(days=1)

    service = get_credential.credential('')

    page_token = None
    event_ids, data = [], []
    while True:
        events = service.events().list(
            calendarId='primary',
            pageToken=page_token,
            timeMin=period_start.strftime('%Y-%m-%dT00:00:00+09:00'),
            timeMax=period_end.strftime('%Y-%m-%dT00:00:00+09:00'),
            ).execute()
        for event in events['items']:
            event_id = event['id'].split('_', 2)[0]
            if event_id in event_ids:
                continue
            elif 'start' not in event:
                continue
            elif 'dateTime' in event['start']:
                event_ids.append(event_id)
                start = datetime.datetime.strptime(
                    event['start']['dateTime'][0:19], '%Y-%m-%dT%H:%M:%S')
                start = float(time.mktime(start.timetuple()))
                end = datetime.datetime.strptime(
                    event['end']['dateTime'][0:19], '%Y-%m-%dT%H:%M:%S')
                end = float(time.mktime(end.timetuple()))
                data.append({
                    'summary': event['summary'].lower(),
                    'spent': (end-start) / (60*60),
                    })
        page_token = events.get('nextPageToken')
        if not page_token:
            break

    summary = []
    spent = {}
    for d in data:
        if d['summary'] not in summary:
            summary.append(d['summary'])
            spent[d['summary']] = 0.0
        spent[d['summary']] += d['spent']
    print('[Summarize Spent Time]')
    print('** spent on ' + period_start.strftime('%Y-%m-%d') + ' **')
    for (sm, sp) in sorted(spent.items(), key=lambda x:x[1], reverse=True):
        print('{0:12}:\t{1:4}h'.format(sm, sp))
    print('---------------------')
    spsum = sum(t for (_, t) in spent.items())
    print('sum         :\t{0:4}h'.format(spsum))
    print('left        :\t{0:4}h'.format(24-spsum))


if __name__ == '__main__':
    summarize_spent(period_start=datetime.date.today())
