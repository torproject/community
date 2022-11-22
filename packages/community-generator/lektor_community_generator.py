# -*- coding: utf-8 -*-
import json
import os

from urllib.parse import quote_plus

from lektor.pluginsystem import Plugin
from lektor.utils import slugify


class CommunityGeneratorPlugin(Plugin):
    name = 'community-generator'
    description = u'Generate content files for community training resource page'

    contents_lr_tmpl = '''
section: {section}
---
_model: sortby_resources
---
section_id: {section_id}
---
color: {color}
---
_template: {template}
---
title: {title}
---
subtitle: {subtitle}
---
cta: {cta}
---
key: {key}
---
html: {html}
---
sortby_resources: {sortby_resources}
---
body:

{body}
'''

    def _generate_file_helper(self, url_path: str, content: str) -> None:
        """Generate a contents.lr file from a URL path and content string.

        url_path is relative to the site's base URL. /foo/bar/baz expands to:
            <project root>/content/foo/bar/baz/contents.lr
        """
        content_path = os.path.join(
            self.env.project.tree,
            'content',
            *url_path.strip('/').split('/'),
            'contents.lr',
        )
        os.makedirs(os.path.dirname(content_path), exist_ok=True)
        with open(content_path, 'w') as f:
            f.write(content)

    @classmethod
    def _format_default(cls, to_format: str, **kwargs: str) -> str:
        """Call str.format but with default values."""
        formatting = {
            'section': '',
            'section_id': '',
            'color': '',
            'template': 'empty.html',
            'title': '',
            'subtitle': '',
            'cta': '',
            'key': '',
            'html': '',
            'sortby_resources': '',
            'body': '',
        }

        formatting.update(kwargs)

        return to_format.format(**formatting)

    def _get_resource_topics(self):
        """Return a set of every author used by at least one resource."""
        topics = []
        for resource in self.resources.values():
            topics.extend(resource.get('topics', []))

        # flatten
        return set(topics)

    def _get_resource_langs(self):
        """Return a set of every language used by at least one resource."""
        duplicated_languages = []
        for resource in self.resources.values():
            language_list = resource.get('languages', {})
            duplicated_languages.extend(language_list.items())

        # flatten
        return set(duplicated_languages)

    def _get_authors(self):
        """Return a set of every author used by at least one resource."""
        authors = set()
        for resource in self.resources.values():
            authors.add(resource['author'])

        return authors

    def generate_files(self):
        """Generate contents.lr files for the sortby fields: topics, languages, author."""
        with open(os.path.join(self.env.project.tree, 'databags', 'community-training-materials.json'), 'r') as f:
            self.resources = json.load(f)

        topics = self._get_resource_topics()
        languages = self._get_resource_langs()
        authors = self._get_authors()

        # lektor won't render a page if it doesn't have a parent contents.lr
        self._generate_file_helper(f'training/resources/sortby', self._format_default(self.contents_lr_tmpl))
        
        # generate sortby/topics
        self._generate_file_helper(f'training/resources/sortby/topic', self._format_default(self.contents_lr_tmpl))
        for topic in topics:
            sortby_resources = filter(lambda resource: topic in resource[1].get('topics', []), self.resources.items())
            self._generate_file_helper(
                f'training/resources/sortby/topic/{slugify(topic)}',
                self._format_default(
                    self.contents_lr_tmpl,
                    section='Training',
                    color='primary',
                    template='layout.html',
                    title='Training Resources',
                    html='resources-sortby.html',
                    sortby_resources=json.dumps(dict(sortby_resources)),
                    body='''
Our Community team delivers digital security training about Tor to human rights defenders, journalists, activists and marginalized communities around the world.
To request a Tor training for your organization or community, please contact us and send an email to [training at torproject.org](mailto:training@torproject.org).
Or, if you want to teach your community about Tor, these training materials are for you!
                    '''
                ))

        # generate sortby/language
        self._generate_file_helper(f'training/resources/sortby/language', self._format_default(self.contents_lr_tmpl))
        for language_code, language_name in languages:
            sortby_resources = filter(lambda resource: language_code in resource[1]['languages'], self.resources.items())
            self._generate_file_helper(
                f'training/resources/sortby/language/{language_code}',
                self._format_default(
                    self.contents_lr_tmpl,
                    section='Training',
                    color='primary',
                    template='layout.html',
                    title='Training Resources',
                    html='resources-sortby.html',
                    sortby_resources=json.dumps(dict(sortby_resources)),
                    body='''
Our Community team delivers digital security training about Tor to human rights defenders, journalists, activists and marginalized communities around the world.
To request a Tor training for your organization or community, please contact us and send an email to [training at torproject.org](mailto:training@torproject.org).
Or, if you want to teach your community about Tor, these training materials are for you!
                    '''
                ))

        # generate sortby/author
        self._generate_file_helper(f'training/resources/sortby/author', self._format_default(self.contents_lr_tmpl))
        for author_name in authors:
            sortby_resources = filter(lambda resource: author_name == resource[1]['author'], self.resources.items())
            self._generate_file_helper(
                f'training/resources/sortby/author/{slugify(author_name)}',
                self._format_default(
                    self.contents_lr_tmpl,
                    section='Training',
                    color='primary',
                    template='layout.html',
                    title='Training Resources',
                    html='resources-sortby.html',
                    sortby_resources=json.dumps(dict(sortby_resources)),
                    body='''
Our Community team delivers digital security training about Tor to human rights defenders, journalists, activists and marginalized communities around the world.
To request a Tor training for your organization or community, please contact us and send an email to [training at torproject.org](mailto:training@torproject.org).
Or, if you want to teach your community about Tor, these training materials are for you!
                    '''
                ))

    def on_setup_env(self, **extra):
        """Generate files when the lektor process starts."""
        self.generate_files()
        self.env.jinja_env.globals['json_loads'] = json.loads
        self.env.jinja_env.globals['get_resource_topics'] = self._get_resource_topics
        self.env.jinja_env.globals['get_resource_langs'] = self._get_resource_langs
        self.env.jinja_env.globals['get_authors'] = self._get_authors
        self.env.jinja_env.globals['slugify'] = slugify

    def on_server_spawn(self, **extra):
        """Generate files when the dev server restarts."""
        self.generate_files()
