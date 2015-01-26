#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from __future__ import print_function
import datetime

import get_credential


def main():
    service = get_credential.credential("")
    page_token = None
    ids = []
    today = datetime.date.today()
    change_start = today - datetime.timedelta(days=3)
    change_end = today + datetime.timedelta(days=3)
    while True:
        events = service.events().list(calendarId="primary",
                pageToken=page_token,
                timeMin=change_start.strftime("%Y-%m-%dT00:00:00+09:00"),
                timeMax=change_end.strftime("%Y-%m-%dT00:00:00+09:00")).execute()
        for event in events["items"]:
            try:
                summary = event['summary'].lower()
                if (summary.startswith('study') or 
                    summary.startswith('english') or
                    summary.startswith('work')):
                    event['colorId'] = 9
                elif summary.startswith('run'):
                    event['colorId'] = 10
                elif summary.startswith('pastime'):
                    event['colorId'] = 3
                elif summary.startswith('univ'):
                    event['colorId'] = 6
                event['summary'] = summary.capitalize()
                service.events().update(calendarId='primary',
                    eventId=event['id'], body=event).execute()
            except KeyError:
                pass
        page_token = events.get('nextPageToken')
        if not page_token:
            break


if __name__ == '__main__':
    main()
