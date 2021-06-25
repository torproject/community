# Community portal

This is the repository of Community portal. The current online version of this portal can be found at https://community.torproject.org or [Community Onion Service](http://xmrhfasfg5suueegrnc4gsgyi2tyclcy5oz7f5drnrodmdtob6t2ioyd.onion/).

To clone the code use either of 

```git clone https://git.torproject.org/project/web/community.git/```

```torify git clone http://xtlfhaspqtkeeqxk6umggfbr3gyfznvf4jhrge2fujz53433i2fcs3id.onion/project/web/community.git/``` 

or browse it [online](http://gzgme7ov25seqjbphab4fkcph3jkobfwwpivt5kzbv3kqx2y2qttl4yd.onion/project/web/community).

## How to report bugs or feedback 

First, check if the bug is already known. You can search and read all the issues at https://gitlab.torproject.org/. To create a new issue, please [request a new account](https://gitlab.onionize.space/) to access Tor Project's GitLab instance and [find the right repository](https://gitlab.torproject.org/tpo) to report your issue. Issues related to our websites should be filed under the [Web issue tracker](https://gitlab.torproject.org/groups/tpo/web/-/issues).

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

```$ cd community/lego && git submodule update --init --recursive```

5. Translations for the website are imported by Jenkins when building the page, but if you want to test them, download the correct branch of the translations repo to the ./i18n/ folder.

6. Finally:

To run a local continuous builder: ```$ lektor server```

To just build the website once: ```$ lektor build -O <folder>```

#### How to develop on the website

Check our [wiki pages](https://gitlab.torproject.org/web/community/wikis/How-to-develop-on-the-website).

### Translations

To help us to translate, please join the Tor Project team in [Transifex](https://www.transifex.com/).

### Getting help

If you want to contribute to the Community portal, we will be happy to help you. Join us at #tor-www in [irc.oftc.net](https://www.oftc.net).

## Our Workflows

### Tor Internal Workflow

This is the workflow that Tor Internal people should use when making changes on the Community Portal:

1. When starting work on an issue or content, please assign the issue to yourself and move into the `Doing` column on the [Community Portal Project Board](https://dip.torproject.org/web/community/-/boards). You can follow the process outlined in ["How to send a merge request or propose a change"](https://gitlab.torproject.org/web/tpo/wikis/Git-flow-and-merge-requests#how-to-send-a-merge-request-or-propose-a-change) to work on your changes.
2. To view your changes on the website, you can [run lektor locally](https://gitlab.torproject.org/web/tpo/wikis/Compiling-a-local-version-of-the-website).
3. Once you are happy with your work, push your changes to `develop` branch and move to `needs-review` column on the [Community Portal Project Board](https://gitlab.torproject.org/web/community/-/boards).
4. Add a comment to the issue, tagging the reviewer, e.g. `@steph`, with:
    - Location of page on lektor-staging `develop` branch, e.g. https://lektor-staging.torproject.org/community/develop/.
    - Contents file, containing your changes where it would be located on the **reviewer's repo**, e.g. `https://gitlab.torproject.org/steph/community/blob/develop/content/onion-services/contents.lr`.
    - For the review workflow, please see (Reviewer Workflow).
5. Once the work has been reviewed and any necessary changes and merge request has been made, a repo maintainer or team members with write access to gitweb master will then merge or cherry-pick these changes to master, following the workflow outlined in [How to use our git flow](https://gitlab.torproject.org/web/tpo/wikis/Git-flow-and-merge-requests#how-to-use-our-git-flow).
6. Merger should then move the ticket to the `Closed` column.

### Reviewer Workflow

1. Review the page on lektor-staging.
2. Review the content on your repo's develop branch and use the gitlab edit button to make any changes.
3. When you are happy with your changes:
    - Update the "Commit message" to explain why you have made your changes.
    - Update the "Target Branch".
    - Make sure that the "Start a new merge request with these changes" checkbox is checked.
    - Click on "Commit changes".
4. You will be sent to a new page to create your merge request:
    - Update "Title" with a short title to explain your changes.
    - Update "Description", you can use the commit message you entered before additionally referencing the original issue you have reviewed, e.g. `https://gitlab.torproject.org/web/community/issues/3`, and tagging one of the repo maintainers, e.g. `@pili`, so they know the change can be merged.
    - Make sure that both "Delete source branch when merge request is accepted" and "Squash commits when merge request is accepted" are checked.
    - Click "Submit merge request".
5. Reviewer should comment on the original issue with a link to the merge request created, e.g. `https://gitlab.torproject.org/steph/community/merge_requests/2`.

### Volunteer Workflow

This is the workflow that external volunteers should use when making changes on the Community Portal:

We recommend that you use our [github mirror](https://github.com/torproject/community) to submit PRs and contributions to our Community repo. Once you have a PR ready you should:

0. Ideally try to run it locally and check that nothing breaks and everything still behaves as before.
1. Make a PR and ping the team on #tor-www IRC channel to let us know there's a PR waiting for review.

At this point, one of us on the website team will aim to review your PR within 24h during the week (this may take longer on the weekends). Review will involve:

  - Reading the text to make sure it's accurate and there are no spelling errors or grammar mistakes.
  - If there are any front end and/or template changes involved, the changes will be pushed to our `develop` branch for functionality review.
  - If there are any fixes necessary, we will ask for changes to be made.

Once it all looks good and behaves correctly, we will merge your request to the master branch of the community portal [canonical repo](https://gitweb.torproject.org/project/web/community.git/) on [gitweb](https://gitweb.torproject.org/) master. 

