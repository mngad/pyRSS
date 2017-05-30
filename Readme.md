pyRSS
=====

A RSS reader that generates web pages with links to the articles from the selected rss urls.

Setup
-----

.rss_conf.ini needs to be setup and copied to ~/.config/ in the users home directory:

```
[Dir]
rss_server_url: 
directory: 

[Template]
template: """<!DOCTYPE html>
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
```

This contains the template for the webpages and more importantly the `rssurl` which points to the webpage where the pages will be displayed and `directory` which should be set to the directory on the server where the pages will be kept - ideally in a `RSS` or similar folder.

css files
-------

These are automatically copied to the correct directory assuming that the conf file is setup correctly. These can edited - taking care with the column / no column (`columns: 500px;`) versions.

