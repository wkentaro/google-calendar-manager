#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from __future__ import division, print_function, with_statement
import time
import datetime

from clint.textui import indent, colored, puts

from change_events import get_title_from_summary
import get_credential

__author__ = 'www.kentaro.wada@gmail.com (Kentaro Wada)'


def is_ascii(s):
    return all(ord(c) < 128 for c in s)


def summarize_spent(period_start):
    """Summarize spent time with given period start"""

    service = get_credential.credential('')

    page_token = None
    event_ids, data = [], []
    while True:
        events = service.events().list(
            calendarId='primary',
            pageToken=page_token,
            timeMin=period_start.strftime('%Y-%m-%dT00:00:00+09:00'),
            timeMax=period_start.strftime('%Y-%m-%dT23:59:59+09:00'),
            ).execute()
        event_items = [event for event in events['items'] if 'updated' in event]
        event_ids += [event['id'].split('_', 2)[0] for event in events['items'] if event['status'] == 'cancelled']
        for event in sorted(event_items, key=lambda x:x['updated'], reverse=True):
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
                title = get_title_from_summary(event['summary'])
                data.append({
                    'title': title,
                    'spent': (end-start) / (60*60),
                    })
        page_token = events.get('nextPageToken')
        if not page_token:
            break

    title = []
    spent = {}
    for d in data:
        if d['title'] not in title:
            title.append(d['title'])
            spent[d['title']] = 0.0
        spent[d['title']] += d['spent']

    print(colored.cyan('==> summarize of spent time'))
    puts('spent on {}'.format(period_start.strftime('%Y-%m-%d')))
    with indent(3, quote=colored.blue('.')):
        puts('------------------------------------')
        for (c1, c2) in sorted(spent.items(), key=lambda x:x[1], reverse=True):
            width = 30
            if is_ascii(c1):
                c1 += ' ' * (width - len(c1))
            else:
                c1 += ' ' * (width - int(len(c1) * 2.))
            puts(colored.green("{0} {1:4}h".format(c1.encode('utf-8'), c2)))
        puts('------------------------------------')
        spsum = sum(t for (_, t) in spent.items())
        puts('sum' + ' '*(width-3) + ' {0:4}h'.format(spsum))
        puts('left' + ' '*(width-4) + ' {0:4}h'.format(24-spsum))


if __name__ == '__main__':
    summarize_spent(period_start=datetime.date.today()-datetime.timedelta(days=1))
    summarize_spent(period_start=datetime.date.today())
