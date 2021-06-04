#!/usr/bin/python3

import collections
import sys

import yaml

# Configuration

RECENT_LIMIT  = 20
ARTICLE_LIMIT = 2000
SITE_LIMIT    = 10
LOG_PATH      = '/home/pbui/.weechat/logs/irc.bx612.#paperboy.weechatlog'

# Main Execution

LOG_DATA = [l.strip().split('\t', 2)[-1] for l in open(LOG_PATH) if 'bobbit' in l and '@' in l]
RECENT   = []
ARTICLES = collections.defaultdict(list)

for index, article in enumerate(reversed(LOG_DATA)):
    article_site  = article.split(':', 1)[0].strip()
    article_title = article.split(':', 1)[1].rsplit('@', 1)[0].strip().replace('\t', ' ')
    article_link  = article.rsplit('@', 1)[-1].strip()

    if index >= ARTICLE_LIMIT:
        break

    if index < RECENT_LIMIT:
        RECENT.append({
            'site' : article_site,
            'title': article_title,
            'link' : article_link,
        })

    if len(ARTICLES[article_site]) < SITE_LIMIT:
        ARTICLES[article_site].append({
            'title': article_title,
            'link' : article_link,
        })

yaml.dump({'recent': RECENT, 'articles': dict(ARTICLES)}, sys.stdout, default_flow_style=False)
