import configparser

import os

import sys

from shutil import copyfile

import feedparser

from future import Future


def rem_bad_char(string):

    string = ''.join(c for c in string if c not in ' /\\(){}<>\'!')
    return string


def split_url(string):

    newstr = string.split('/')
    return newstr


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
    contents = ''
    try:
        with open(link_file_name, 'r') as file:
            for line in reversed(file.read().splitlines()):
                contents += line
    except OSError:
        print("No file exists for rss backup - is this a new url?")

    return contents


def make_indie_pages(feed):

    contents = get_link_list(rem_bad_char(feed['channel']['title']))
    link_formatted = ''
    link_formatted = link_formatted + '<p> <a href="' + \
        'http://' + split_url(feed['url'])[2] + '">' + \
        feed['channel']['title'] + '</a> </p>' + '\n'
    for entry in feed['items']:
        if entry['link'] not in contents:
            title = entry['title']
            link = entry['link']
            # print('{}, [{}]'.format(entry["title"], entry['link']))
            link_formatted = link_formatted + '<a href="' + \
                link + '">' + ' - ' + title + '</a><br>' + '\n'

    link_formatted = link_formatted + contents
    link_formatted = link_formatted + '<p> <a href="' + \
        rss_server_url + '">' + '<<< BACK' + '</a> </p>' + '\n'
    make_page(rem_bad_char(feed['channel']['title']) + '.html', link_formatted,
              feed['channel']['title'], 'noCol')
    make_link_list(rem_bad_char(feed['channel']['title']), link_formatted)


def get_links(urllist):  # get the urls, feeds, links and link titles

    future_calls = [Future(feedparser.parse, rss_url) for rss_url in urllist]
    # multithread the download of the urls
    feeds = [future_obj() for future_obj in future_calls]
    link_formatted = ''

    for feed in feeds:  # cycle through feeds (each url)
        print(feed["channel"]["title"])
        # create title for each feed
        make_indie_pages(feed)
        link_formatted = link_formatted + '<p> <a href="' + rss_server_url + \
            '/' + rem_bad_char(feed['channel']['title']) + '.html' + '">' + \
            feed['channel']['title'] + '</a> </p>' + '\n'
        count = 0
        for entry in feed['items']:
            if count == 5:
                break
            else:  # create links for top five from each feed
                count = count + 1
                title = entry['title']
                link = entry['link']
                # print('{}, [{}]'.format(entry["title"], entry['link']))
                link_formatted = link_formatted + '<a href="' + \
                    link + '">' + ' - ' + title + '</a><br>' + '\n'
    return link_formatted


def get_url_file_list():

    urllist = []
    url_file = open(os.path.expanduser("~") + '/.config/urlFile.txt', 'r')
    for line in url_file:
        urllist.append(line)

    return urllist


def get_settings():

    try:
        settings = configparser.ConfigParser()
        settings._interpolation = configparser.ExtendedInterpolation()
        settings.read(os.path.expanduser("~") + '/.config/.rss_conf.ini')
        print('Reading settings from: ' +
              os.path.expanduser("~") + '/.config/.rss_conf.ini')
        rss_server_url = settings.get('Dir', 'rss_server_url')
        directory = settings.get('Dir', 'directory')
        template = settings.get('Template', 'template')
        return rss_server_url, directory, template
    except Exception:
        print('Must copy rss_conf.ini to the ~/.config/ and add the directory \
            and url for the rss pages first')
        sys.exit(0)

if __name__ == '__main__':

    cwd = os.getcwd()
    rss_server_url, directory, template = get_settings()
    link_formatted = get_links(get_url_file_list())
    make_page('index.html', link_formatted, 'RSS', 'Col')
    if not os.path.isfile(directory + '/minimal_Col.css'):
        copyfile(cwd + '/minimal_Col.css', directory + '/minimal_Col.css')
    if not os.path.isfile(directory + '/minimal_noCol.css'):
        copyfile(cwd + '/minimal_noCol.css', directory + '/minimal_noCol.css')
