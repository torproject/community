# Community portal

This is the repository of Community portal. The current online version of this portal can be found at [https://community.torproject.org](https://community.torproject.org) or [Community Onion Service](http://3gldbgtv5e4god56.onion/).

To clone the code use either of 

```git clone https://git.torproject.org/project/web/community.git/```

```torify git clone http://dccbbv6cooddgcrq.onion/project/web/community.git/``` 

or browse it [online](http://gitweb.torproject.org/project/web/community.git).

## How to report bugs or feedback 

First check if your issue wasn't already opened in [dip.torproject.org](https://dip.torproject.org/web/community/issues), then file a [trac ticket](https://trac.torproject.org/projects/tor/newticket) and choose the component: Webpages/Community. 


## What is Lektor

[Lektor](https://www.getlektor.com/) is a framework to generate and serve websites from Markdown files.

Its code can be found at [GitHub](https://github.com/lektor/lektor).

## How to contribute

### (Easy) Edit this page button

You can click ```Edit this page``` and submit your content changes in a [Pull Request in GitHub](https://github.com/torproject/community/pulls).

### (Advanced) Compiling a local version of the website

1. Download and install Lektor: https://www.getlektor.com/downloads/

2. Install the lektor-i18n plugin and its [dependencies](https://github.com/numericube/lektor-i18n-plugin#prerequisites).

3. Clone the repository:

```git clone https://git.torproject.org/project/web/community.git```

4. Init the building blocks submodule: 

```$ cd lego && git submodule update --init --recursive```

5. Translations for the website are imported by Jenkins when bulding the page, but if you want to test them, download the correct branch of the translations repo to the ./i18n/ folder.

6. Finally

To run a local continuous builder: ```$ lektor server```

To just build the website once: ```$ lektor build -O <folder>```

#### How to develop on the website

Check our [wiki pages](https://dip.torproject.org/web/community/wikis/How-to-develop-on-the-website).

### Translations

To help us to translate, please join the Tor Project team in [Transifex](https://www.transifex.com/).


### Getting help

If you want to contribute to the Community portal, we will be happy to help you. Join us at #tor-www in [irc.oftc.net](https://www.oftc.net).
