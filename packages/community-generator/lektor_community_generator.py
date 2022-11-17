# -*- coding: utf-8 -*-
import json
import os

from lektor.pluginsystem import Plugin


class CommunityGeneratorPlugin(Plugin):
    name = 'community-generator'
    description = u'Generate content files for community training resource page'

    contents_lr_tmpl = '''
section: {section}
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
            'body': '',
        }

        formatting.update(kwargs)

        return to_format.format(**formatting)

    def generate_files(self):
        """Generate contents.lr files for the sortby fields: topics, languages, author."""
        with open(os.path.join(self.env.project.tree, 'databags', 'community-training-materials.json'), 'r') as f:
            resources = json.load(f)

        # TODO: topics aren't in the databag yet. the below line won't work if the "topic" key is a list, only string
        # gather all the different resources' topics, filter out the `None`s, use a set for uniqueness
        # topics = set(filter(map(lambda resource: resource.get('topic'))))
        duplicated_languages = []
        for resource in resources.values():
            language_list = resource.get('languages')

            if not language_list:
                continue

            duplicated_languages.extend(duplicated_languages)

        # flatten
        languages = set(duplicated_languages)

        authors = set(filter(None, map(lambda resource: resource.get('author'), resources.values())))


        # lektor won't render a page if it doesn't have a parent contents.lr
        self._generate_file_helper(f'training/resources/sortby', self._format_default(self.contents_lr_tmpl))
        
        # TODO: generate sortby/topics

            
        # generate sortby/language
        self._generate_file_helper(f'training/resources/sortby/language', self._format_default(self.contents_lr_tmpl))
        for language in languages:
            self._generate_file_helper(f'training/resources/sortby/language/{language.lower()}', self._format_default(self.contents_lr_tmpl, template='layout.html', html='empty.html', body='# test'))

    def on_setup_env(self, **extra):
        """Generate files when the lektor process starts."""
        self.generate_files()

    def on_server_spawn(self, **extra):
        """Generate files when the dev server restarts."""
        self.generate_files()
