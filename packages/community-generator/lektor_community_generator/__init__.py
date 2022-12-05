# -*- coding: utf-8 -*-
import json
import os
import string

from urllib.parse import quote_plus

from lektor.pluginsystem import Plugin

from .file_templates import contents_lr_tmpl, sortby_resources_ini


# lektor's slugify removes characters that *should* be url-safe, so let's make our own
def slugify(it: str):
    # url-safe characters as defined by RFC 3986
    url_safe = string.ascii_lowercase + string.digits + '-._~'

    result = []
    last_char_was_dash = False
    for char in it.lower().encode('ascii', 'replace').decode():
        if char in url_safe:
            result.append(char)
            last_char_was_dash = False
        elif last_char_was_dash:
            continue
        else:
            result.append('-')
            last_char_was_dash = True
    
    return ''.join(result)


class CommunityGeneratorPlugin(Plugin):
    name = 'community-generator'
    description = u'Generate content files for community training resource page'

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
            'html': '',
            'sortby_resources': '',
            'current_topic': '',
            'current_lang': '',
            'current_author': '',
            'body': '',
        }

        formatting.update(kwargs)

        return to_format.format(**formatting)

    def _get_new_link(self, current_page, new_topic=None, new_lang=None, new_author=None):
        current_url = current_page.url_path.rstrip('/')
        if current_url == '/training/resources':
            current_url = '/'.join([current_url, 'sortby', 'none', 'none', 'none'])

        split_url = current_url.split('/')
        if new_topic:
            split_url[-3] = new_topic
        if new_lang:
            split_url[-2] = new_lang
        if new_author:
            split_url[-1] = new_author

        return '/'.join(split_url)

    def _get_resource_topics(self):
        """Return a set of every author used by at least one resource."""
        topics = ['none']
        for resource in self.resources.values():
            topics.extend(resource.get('topics', []))

        # flatten
        return set(topics)

    def _get_resource_langs(self):  # type: set[tuple[str, str]]
        """Return a set of every language used by at least one resource."""
        languages = [('none', 'none')]
        for resource in self.resources.values():
            language_list = resource.get('languages', {})
            languages.extend(language_list.items())

        # flatten
        return set(languages)

    def _get_authors(self):
        """Return a set of every author used by at least one resource."""
        authors = set(('none',))
        for resource in self.resources.values():
            authors.add(resource['author'])

        return authors

    def generate_files(self):
        """Generate contents.lr files for the sortby fields: topics, languages, author."""
        with open(os.path.join(self.env.project.tree, 'models', 'sortby_resources.ini'), 'w') as f:
            f.write(sortby_resources_ini)

        with open(os.path.join(self.env.project.tree, 'databags', 'community-training-materials.json'), 'r') as f:
            self.resources = json.load(f)

        topics = self._get_resource_topics()
        languages = self._get_resource_langs()
        authors = self._get_authors()

        # lektor won't render a page if it doesn't have a parent contents.lr
        self._generate_file_helper(f'training/resources/sortby', self._format_default(contents_lr_tmpl))

        # loop through topics
        for topic in topics:
            topic_resources = self.resources.copy()

            if topic != 'none':
                topic_resources = dict(filter(lambda resource: topic in resource[1].get('topics', []), topic_resources.items()))

            self._generate_file_helper(f'training/resources/sortby/{slugify(topic)}', self._format_default(contents_lr_tmpl))
            self._generate_file_helper(f'training/resources/sortby/{slugify(topic)}/none', self._format_default(contents_lr_tmpl))
            self._generate_file_helper(
                f'training/resources/sortby/{slugify(topic)}/none/none',
                self._format_default(
                    contents_lr_tmpl,
                    section='Training',
                    color='primary',
                    template='layout.html',
                    title='Training Resources',
                    html='resources-sortby.html',
                    sortby_resources=json.dumps(topic_resources),
                    current_topic=topic if topic != 'none' else '',
                    body='''
Our Community team delivers digital security training about Tor to human rights defenders, journalists, activists and marginalized communities around the world.
To request a Tor training for your organization or community, please contact us and send an email to [training at torproject.org](mailto:training@torproject.org).
Or, if you want to teach your community about Tor, these training materials are for you!
'''
                ))

            for language_code, language_name in languages:
                language_resources = topic_resources.copy()
                if language_code != 'none':
                    language_resources = dict(filter(lambda resource: language_code in resource[1]['languages'], language_resources.items()))
            
                self._generate_file_helper(f'training/resources/sortby/{slugify(topic)}/{language_code}', self._format_default(contents_lr_tmpl))
                self._generate_file_helper(
                    f'training/resources/sortby/{slugify(topic)}/{language_code}/none',
                    self._format_default(
                        contents_lr_tmpl,
                        section='Training',
                        color='primary',
                        template='layout.html',
                        title='Training Resources',
                        html='resources-sortby.html',
                        sortby_resources=json.dumps(language_resources),
                        current_topic=topic if topic != 'none' else '',
                        current_lang=language_name if language_name != 'none' else '',
                        body='''
Our Community team delivers digital security training about Tor to human rights defenders, journalists, activists and marginalized communities around the world.
To request a Tor training for your organization or community, please contact us and send an email to [training at torproject.org](mailto:training@torproject.org).
Or, if you want to teach your community about Tor, these training materials are for you!'''
                    ))

                for author_name in authors:
                    author_resources = language_resources.copy()

                    if author_name != 'none':
                        author_resources = dict(filter(lambda resource: author_name == resource[1]['author'], author_resources.items()))

                    self._generate_file_helper(
                        f'training/resources/sortby/{slugify(topic)}/{language_code}/{slugify(author_name)}',
                        self._format_default(
                            contents_lr_tmpl,
                            section='Training',
                            color='primary',
                            template='layout.html',
                            title='Training Resources',
                            html='resources-sortby.html',
                            sortby_resources=json.dumps(author_resources),
                            current_topic=topic if topic != 'none' else '',
                            current_lang=language_name if language_name != 'none' else '',
                            current_author=author_name if author_name != 'none' else '',
                            body='''
Our Community team delivers digital security training about Tor to human rights defenders, journalists, activists and marginalized communities around the world.
To request a Tor training for your organization or community, please contact us and send an email to [training at torproject.org](mailto:training@torproject.org).
Or, if you want to teach your community about Tor, these training materials are for you!'''
                    ))

    def on_setup_env(self, **extra):
        """Generate files when the lektor process starts."""
        self.generate_files()
        self.env.jinja_env.globals['json_loads'] = json.loads
        self.env.jinja_env.globals['get_new_link'] = self._get_new_link
        self.env.jinja_env.globals['get_resource_topics'] = self._get_resource_topics
        self.env.jinja_env.globals['get_resource_langs'] = self._get_resource_langs
        self.env.jinja_env.globals['get_authors'] = self._get_authors
        self.env.jinja_env.globals['slugify'] = slugify

    def on_server_spawn(self, **extra):
        """Generate files when the dev server restarts."""
        self.generate_files()
