Requirements
---
Copy [client_secrets.json.sample](https://github.com/wkentaro/google-calendar-manager/blob/master/client_secrets.json.sample)
as `./client_secrets.json` and edit it.  
(Fill the `YOUR_CLIENT_SECRET` and `YOUR_CLIENT_ID`)

Usage
---

### summarize spent time
```sh
# summarize your spent time in a day.
$ python summarize_spent.py
```

### change events attributes
You can change events attributes with your preferences.
First, copy [events_config.yml.sample](https://github.com/wkentaro/google-calendar-manager/blob/master/events_config.yml.sample)
as `~/.events_config.yml` and edit it. See documentation [here](#events-config) to more information.

```sh
# change events config (colors & summary) 
$ python change_events.py 
```

Events config
---
### Prerequisites
The name of each events should meet rules below.

```
# title only like "TITLE"
work  # example
```

```
# title & detail like "TITLE: DETAIL"
work: meeting with Eliza # example
```

### color_rules
`color_rules` is for user who likes colored events.
You can set summaries as list with each color.

```yml
color_rules:
  COLOR_NAME1: [SUMMARY_NAME1, SUMMARY_NAME2]
  COLOR_NAME2: [SUMMARY_NAME3]

# example
color_rules:
  purple: [work, study]
  green: [pastime]
```

### alias
`alias` is for user who likes quick input of each events.
You can set short name and its original name.

```yml
alias:
  SHORT_NAME1: ORIGINAL_NAME1
  SHORT_NAME2: ORIGINAL_NAME2
  
# example
alias:
  wk: work
  sd: study
  pm: pastime
```
