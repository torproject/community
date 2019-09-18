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

## Our Workflows

### Internal Workflow

This is the workflow that Tor Internal people should use when making changes on the Community Portal:

1. When starting work on an issue or content, please assign the issue to yourself and move into the `Doing` column on the [Community Portal Project Board](https://dip.torproject.org/web/community/-/boards). You can follow the process outlined in ["How to send a merge request or propose a change"](https://dip.torproject.org/web/tpo/wikis/Git-flow-and-merge-requests#how-to-send-a-merge-request-or-propose-a-change) to work on your changes.
2. To view your changes on the website, you can either run lektor locally, or push to `develop` branch.
3. Once you are happy with your work, push your changes to `staging` branch and move to `needs-review` column on the [Community Portal Project Board](https://dip.torproject.org/web/community/-/boards)
4. Add a comment to the issue, tagging the reviewer, e.g `@steph`, with:
    - Location of page on lektor staging, e.g https://lektor-staging.torproject.org/community/staging/
    - Contents file, on your branch, containing your changes, e.g https://dip.torproject.org/pili/community/blob/master/content/onion-services/contents.lr
    - For the review workflow, please see
5. Once the work has been reviewed and any necessary changes have been made, reviewer should move the issue to the `reviewed` column and add a comment to the issue with details of where the latest version can be found, e.g https://dip.torproject.org/{user}/community/blob/master/content/onion-services/contents.lr
6. Team members with write access to gitweb master will then push these changes to master, following the workflow outlined in [How to use our git flow](https://dip.torproject.org/web/tpo/wikis/Git-flow-and-merge-requests#how-to-use-our-git-flow)
7. Merger should then move the the ticket to the `Closed` column

### Volunteer Workflow

This is the workflow that external volunteers should use when making changes on the Community Portal:

We recommend that you use our [github mirror](https://github.com/torproject/community) to submit PRs and contributions to our Community repo. Once you have a PR ready you should:

0. Ideally try to run it locally and check that nothing breaks and everything still behaves as before
1. Make a PR and ping the team on #tor-www IRC channel to let us know there's a PR waiting for reviewx

At this point, one of us on the website team will aim to review your PR within 24h during the week (this may take longer on the weekends). Review will involve:

  - Reading the text to make sure it's accurate and there are no spelling errors or grammar mistakes
  - If there are any front end and/or template changes involved, the changes will be pushed to our development branch for functionality review
  - If there are any fixes necessary, we will ask for changes to be made.

Once it all looks good and behaves correctly, we will merge your request to the master branch of the community portal [canonical repo](https://gitweb.torproject.org/project/web/community.git/) on [gitweb](https://gitweb.torproject.org/) master. 

