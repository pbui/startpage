#!/usr/bin/python3

import collections
import sys

import yaml

# Configuration

RECENT_LIMIT  = 20
ARTICLE_LIMIT = 10000
SITE_LIMIT    = 20
LOG_PATH      = '/home/pbui/.weechat/logs/irc.bx612.#paperboy.weechatlog'

# Main Execution

LOG_DATA = [l.strip().split('\t', 2)[-1] for l in open(LOG_PATH) if 'bobbit' in l and '@' in l]
RECENT   = []
ARTICLES = collections.defaultdict(list)
AUTHORS  = collections.defaultdict(list)

for index, article in enumerate(reversed(LOG_DATA)):
    if '#' in article.split('by')[-1]:
        article_author = article.split(':', 1)[0].strip()
        article_title  = article.split(':', 1)[1].rsplit('@', 1)[0].strip().replace('\t', ' ')
        article_link   = article.rsplit('@', 1)[-1].split('#')[0].strip()
        article_site   = article.rsplit('#', 1)[-1].strip()
    else:
        article_site   = article.split(':', 1)[0].strip()
        article_title  = article.split(':', 1)[1].rsplit('@', 1)[0].strip().replace('\t', ' ')
        article_link   = article.rsplit('@', 1)[-1].strip()
        article_title, article_author = article_title.rsplit(' by ', 1)
        article_author = article_author.split('(')[0].strip()

    if index >= ARTICLE_LIMIT:
        break

    if index < RECENT_LIMIT:
        RECENT.append({
            'site'  : article_site,
            'title' : article_title,
            'link'  : article_link,
            'author': article_author,
        })

    if len(ARTICLES[article_site]) < SITE_LIMIT:
        ARTICLES[article_site].append({
            'title' : article_title,
            'link'  : article_link,
            'author': article_author,
        })

    if len(AUTHORS[article_author]) < SITE_LIMIT:
        AUTHORS[article_author].append({
            'title' : article_title,
            'link'  : article_link,
        })

yaml.dump(
    {'recent': RECENT, 'articles': dict(ARTICLES), 'authors': dict(AUTHORS)},
    sys.stdout,
    default_flow_style=False
)
