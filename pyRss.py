import feedparser
from future import Future

rssURL = 'http://fraun.space/rss'
directory = '/home/fraun/start/rss'  # directory where the index file will be
# created and where the urlList and css files are found.
template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width" />
    <link rel="icon" type="image/png" href="/favicon.png" />
    <link rel="stylesheet" type="text/css" href="minimal.css" />
    <title>RSS</title>
</head>
<body>
    <div id="content">

        {links}

    </div>
</body>
</html>
"""
def remBadChar(string):
    string= ''.join(c for c in string if c not in ' /\\(){}<>\'!')
    return string

def makePage(pageTitle, linkFormatted):

    context = {  # context for the tmplate - bits to change - filname etc.
        "links": linkFormatted
    }
    indexFile = open(directory + '/'+pageTitle, 'w')
    indexFile.write(template.format(**context))
    indexFile.close()

def makeIndiePages(feed):
    linkFormatted = ''
    linkFormatted = linkFormatted + '<p> <a href="' + \
        feed['url'] + '">' + feed['channel']['title'] + '</a> </p>' + '\n'
    count = 0
    for entry in feed['items']:
        if count == 100:
           #  print('\n')
            break
        else:  # create links for top five from each feed
            count = count + 1
            title = entry['title']
            link = entry['link']
            # print('{}, [{}]'.format(entry["title"], entry['link']))
            linkFormatted = linkFormatted + '<a href="' + \
                link + '">' + ' - ' + title + '</a><br>' + '\n'

    linkFormatted = linkFormatted + '<p> <a href="' + \
            rssURL + '">' + '<<< BACK' + '</a> </p>' + '\n'
    makePage(remBadChar(feed['channel']['title'])+'.html', linkFormatted)

def getLinks():  # get the urls, feeds, links and link titles

    urllist = []
    urlFile = open(directory + '/urlFile.txt', 'r')
    for line in urlFile:
        urllist.append(line)
    future_calls = [Future(feedparser.parse, rss_url) for rss_url in urllist]
    # multithread the download of the urls
    feeds = [future_obj() for future_obj in future_calls]
    linkFormatted = ''

    for feed in feeds:  # cycle through feeds (each url)
        print(feed["channel"]["title"])
        # create title for each feed
        makeIndiePages(feed)
        linkFormatted = linkFormatted + '<p> <a href="' + rssURL + '/' + remBadChar(feed['channel']['title'])+'.html' + '">' + feed['channel']['title'] + '</a> </p>' + '\n'
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
                linkFormatted = linkFormatted + '<a href="' + \
                    link + '">' + ' - ' + title + '</a><br>' + '\n'
    return linkFormatted


if __name__ == '__main__':

    linkFormatted = getLinks()
    makePage('index.html',linkFormatted)
