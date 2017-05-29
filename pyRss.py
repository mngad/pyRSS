import os

from shutil import copyfile

import feedparser

from future import Future


cwd = os.getcwd()
rssURL = 'http://fraun.space/rss'
directory = '/srv/http/rss'  # directory where the index file will be
# created and where the urlList and css files are found.

template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width" />
    <link rel="icon" type="image/png" href="/favicon.png" />
    <link rel="stylesheet" type="text/css" href="minimal_{}.css" />
    <title>{}</title>
</head>
<body>
    <div id="content">

        {links}

    </div>
</body>
</html>
"""


def rem_bad_char(string):

    string = ''.join(c for c in string if c not in ' /\\(){}<>\'!')
    return string


def make_page(page_title, link_formatted, html_title, css_type):

    context = {  # context for the tmplate - bits to change - filname etc.
        "links": link_formatted
    }
    index_file = open(directory + '/' + page_title, 'w')
    index_file.write(template.format(css_type, html_title, **context))
    index_file.close()


def make_link_list(page_title, links):

    link_file_name = directory + '/' + page_title + '.txt'
    try:
        with open(link_file_name, 'r') as file:
            contents = file.read()
            file_exists = True
    except OSError:
        contents = ''
        file_exists = False
    link_file = open(directory + '/' + page_title + '.txt', 'a')
    if file_exists:
        for link in reversed(links.splitlines()):
            if link not in contents and '<p>' not in link:
                link_file.write(link + '\n')
    else:
        for link in reversed(links.splitlines()):
            if '<p>' not in link:
                link_file.write(link + '\n')

    link_file.close()

def get_link_list(page_title):

    link_file_name = directory + '/' + page_title + '.txt'
    print(link_file_name)
    contents = ''
    try:
        with open(link_file_name, 'r') as file:
            for line in reversed(file.read().splitlines()):
                contents += line
    except OSError:
        print('ERROROROROR')

    return contents

def make_indie_pages(feed):

    contents = get_link_list(rem_bad_char(feed['channel']['title']))
    link_formatted = ''
    link_formatted = link_formatted + '<p> <a href="' + \
        feed['url'] + '">' + feed['channel']['title'] + '</a> </p>' + '\n'
    for entry in feed['items']:
        if entry['link'] not in contents:
            title = entry['title']
            link = entry['link']
            # print('{}, [{}]'.format(entry["title"], entry['link']))
            link_formatted = link_formatted + '<a href="' + \
                link + '">' + ' - ' + title + '</a><br>' + '\n'

    link_formatted = link_formatted + contents
    link_formatted = link_formatted + '<p> <a href="' + \
        rssURL + '">' + '<<< BACK' + '</a> </p>' + '\n'
    make_page(rem_bad_char(feed['channel']['title']) + '.html', link_formatted,
              feed['channel']['title'], 'noCol')
    make_link_list(rem_bad_char(feed['channel']['title']), link_formatted)


def get_links():  # get the urls, feeds, links and link titles

    urllist = []
    url_file = open(directory + '/urlFile.txt', 'r')
    for line in url_file:
        urllist.append(line)
    future_calls = [Future(feedparser.parse, rss_url) for rss_url in urllist]
    # multithread the download of the urls
    feeds = [future_obj() for future_obj in future_calls]
    link_formatted = ''

    for feed in feeds:  # cycle through feeds (each url)
        print(feed["channel"]["title"])
        # create title for each feed
        make_indie_pages(feed)
        link_formatted = link_formatted + '<p> <a href="' + rssURL + '/' + \
            rem_bad_char(feed['channel']['title']) + '.html' + '">' + \
            feed['channel']['title'] + '</a> </p>' + '\n'
        count = 0
        for entry in feed['items']:
            if count == 5:
                print('\n')
                break
            else:  # create links for top five from each feed
                count = count + 1
                title = entry['title']
                link = entry['link']
                # print('{}, [{}]'.format(entry["title"], entry['link']))
                link_formatted = link_formatted + '<a href="' + \
                    link + '">' + ' - ' + title + '</a><br>' + '\n'
    return link_formatted


if __name__ == '__main__':

    link_formatted = get_links()
    make_page('index.html', link_formatted, 'RSS', 'Col')
    if not os.path.isfile(directory + '/minimal_Col.css'):
        copyfile(cwd + '/minimal_Col.css', directory + '/minimal_Col.css')
    if not os.path.isfile(directory + '/minimal_noCol.css'):
        copyfile(cwd + '/minimal_noCol.css', directory + '/minimal_noCol.css')
