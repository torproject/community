# -*- coding: utf-8 -*-
import json
import os

from urllib.parse import quote_plus

from lektor.pluginsystem import Plugin


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

    def _get_resource_langs(self):
        """Return a set of every language used by at least one resource."""
        duplicated_languages = []
        for resource in self.resources.values():
            language_list = resource.get('languages', [])
            duplicated_languages.extend(language_list)

        # flatten
        return set(duplicated_languages)

    def generate_files(self):
        """Generate contents.lr files for the sortby fields: topics, languages, author."""
        with open(os.path.join(self.env.project.tree, 'databags', 'community-training-materials.json'), 'r') as f:
            self.resources = json.load(f)

        # TODO: topics aren't in the databag yet. the below line won't work if the "topic" key is a list, only string
        # gather all the different resources' topics, filter out the `None`s, use a set for uniqueness
        # topics = set(filter(map(lambda resource: resource.get('topic'))))
        languages = self._get_resource_langs()

        authors = set(filter(None, map(lambda resource: resource.get('author'), self.resources.values())))


        # lektor won't render a page if it doesn't have a parent contents.lr
        self._generate_file_helper(f'training/resources/sortby', self._format_default(self.contents_lr_tmpl))
        
        # TODO: generate sortby/topics

            
        # generate sortby/language
        self._generate_file_helper(f'training/resources/sortby/language', self._format_default(self.contents_lr_tmpl))
        for language in languages:
            sortby_resources = filter(lambda resource: language.lower() in [lang.lower() for lang in resource[1].get('languages')], self.resources.items())
            self._generate_file_helper(
                f'training/resources/sortby/language/{quote_plus(language).lower()}',
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
        self.env.jinja_env.globals['get_resource_langs'] = self._get_resource_langs
        self.env.jinja_env.globals['quote_plus'] = quote_plus

    def on_server_spawn(self, **extra):
        """Generate files when the dev server restarts."""
        self.generate_files()
