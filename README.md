# Community portal

This is the repository of Community portal. The current online version of this portal can be found at https://community.torproject.org or [Community Onion Service](http://xmrhfasfg5suueegrnc4gsgyi2tyclcy5oz7f5drnrodmdtob6t2ioyd.onion/).

To clone the code use either of 

```git clone https://gitlab.torproject.org/tpo/web/community.git```

```torify git clone http://eweiibe6tdjsdprb4px6rqrzzcsi22m4koia44kc5pcjr7nec2rlxyad.onion/tpo/web/community.git/``` 

or browse it [online](https://gitlab.torproject.org/tpo/web/community).

## How to report bugs or feedback 

First, check if the bug is already known. You can search and read all the issues at https://gitlab.torproject.org/. To create a new issue, please [request a new account](https://gitlab.onionize.space/) to access Tor Project's GitLab instance and [find the right repository](https://gitlab.torproject.org/tpo) to report your issue. Issues related to our websites should be filed under the [Web issue tracker](https://gitlab.torproject.org/groups/tpo/web/-/issues).

## What is Lektor

[Lektor](https://www.getlektor.com/) is a framework to generate and serve websites from Markdown files.

Its code can be found at [GitHub](https://github.com/lektor/lektor).

## How to contribute

### (Easy) Edit this page button

You can click ```Edit this page``` and submit your content changes in a [Pull Request in GitLab](https://gitlab.torproject.org/tpo/web/community/-/merge_requests/).

### (Advanced) Compiling a local version of the website

1. Download and install Lektor: https://www.getlektor.com/downloads/

2. Install the lektor-i18n plugin and its [dependencies](https://github.com/numericube/lektor-i18n-plugin#prerequisites).

3. Clone the repository:

```git clone https://gitlab.torproject.org/tpo/web/community.git```

4. Init the building blocks submodule: 

```$ cd community/lego && git submodule update --init --recursive```

5. Translations for the website are imported by Jenkins when building the page, but if you want to test them, download the correct branch of the translations repo to the ./i18n/ folder.

6. Finally:

To run a local continuous builder: ```$ lektor server```

To just build the website once: ```$ lektor build -O <folder>```

#### How to develop on the website

Check our [wiki pages](https://gitlab.torproject.org/tpo/web/wiki/-/wikis/How-to-develop-on-the-website).

### Translations

To help us to translate, please join the Tor Project team in [Transifex](https://www.transifex.com/).

### Getting help

If you want to contribute to the Community portal, we will be happy to help you. Join us at #tor-www in [irc.oftc.net](https://www.oftc.net).

### The community-generator plugin

This lektor site uses a special plugin called `community-generator`, you can find it in the `packages` directory. This plugin generates a special set of lektor contents files used for a js-free filtering system on the training resources page.

You shouldn't need to do anything or know anything about this plugin in order to use it. If you want to develop on this plugin, see the plugin's [README](packages/community-generator/README.md).
