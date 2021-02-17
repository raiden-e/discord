import json
import time
from datetime import datetime

import config
import feedparser
from github import Github, InputFileContent
from markdownify import markdownify as md


class Entry:
    def __init__(self, title, text, date):
        self.title = title
        self.text = text
        self.date = date

    def __str__(self):
        message = ''

        clean_title = self.title.replace('*', '')
        clean_title = clean_title.replace('_', '')
        clean_title = clean_title + ':'
        bold_title = f'*{clean_title}*'
        full_title = bold_title + '<br /><br />'
        text = self.text
        text = text + '<br />'
        text = text.replace('*', '')
        clean_text = text.replace('_', '')
        date = self.date.strftime('%d. %B %Y - %H:%M:%S')

        message = message + full_title
        message = message + clean_text
        message = message + date
        message = md(message)
        message = message.replace('\n ', '\n')

        return message


def encoder_entry(entry):
    if isinstance(entry, Entry):
        return {
            'title': entry.title,
            'text': entry.text,
            'date': entry.date.strftime("%Y%m%d%H%M%S")
        }

    if isinstance(entry, list):
        encoded_list = []
        for article in entry:
            if not isinstance(article, Entry):
                raise TypeError("Must be Entry")
            encoded_list.append({
                'title': article.title,
                'text': article.text,
                'date': article.date.strftime("%Y%m%d%H%M%S")
            })
        return encoded_list

    raise TypeError("Must be Entry")


def get_latest_read(entrys):
    latest = entrys[0].date
    for entry in entrys[1:]:
        if entry.date > latest:
            latest = entry.date
    return latest


def decoder_entry(entrys):
    return [Entry(
        entry['title'],
        entry['text'],
        datetime.strptime(entry['date'], "%Y%m%d%H%M%S")
    ) for entry in entrys]


def init():
    return Github(config.GIST_TOKEN).get_gist(config.GIST_ID)


def load_read(gist_name):
    x = init().files[gist_name]
    json_content = json.loads(x.content)
    return decoder_entry(json_content)


def update_read(filename: str = "news", content: list = None, description: str = "Added news"):
    if not content:
        raise TypeError("Value must be set")
    if not isinstance(content, list):
        raise ValueError("playlist_name has to be specified")
    for article in content:
        if not isinstance(article, Entry):
            raise ValueError(f"{article} is not {Entry}")

    init().edit(
        description=description,
        files={
            f'{filename}': InputFileContent(
                json.dumps(
                    content,
                    indent=2,
                    default=encoder_entry))})


def read_current():
    url = 'http://www.inf.fh-dortmund.de/rss.php'
    rss_content = feedparser.parse(url)
    entries = rss_content['entries']

    formatted_entries = []
    for entry in entries:
        title = entry['title']
        text = entry['summary']
        timestamp = entry['published_parsed']
        date = datetime.fromtimestamp(time.mktime(timestamp))
        new_entry = Entry(title, text, date)

        formatted_entries.append(new_entry)

    return formatted_entries
