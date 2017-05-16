import feedparser
from future import Future

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

        <ul id="index">
            {links}
        </ul>

    </div>
</body>
</html>
"""


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
        linkFormatted = linkFormatted + '<p> <a href="' + \
            feed['url'] + '">' + feed['channel']['title'] + '</a> </p>' + '\n'
        count = 0
        for entry in feed['items']:
            if count == 5:
                print('\n')
                break
            else:  # create links for top five from each feed
                count = count + 1
                title = entry['title']
                link = entry['link']
                print('{}, [{}]'.format(entry["title"], entry['link']))
                linkFormatted = linkFormatted + '<a href="' + \
                    link + '">' + ' - ' + title + '</a><br>' + '\n'
    return linkFormatted


if __name__ == '__main__':
    linkFormatted = ''
    linkFormatted = getLinks()
    context = {  # context for the tmplate - bits to change - filname etc.
        "links": linkFormatted
    }
    indexFile = open(directory + '/index.html', 'w')
    indexFile.write(template.format(**context))
    indexFile.close()
