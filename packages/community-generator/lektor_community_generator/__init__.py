# -*- coding: utf-8 -*-
import ast
import json
import os
import string

from urllib.parse import quote_plus

from lektor.pluginsystem import Plugin

from .file_templates import contents_lr_tmpl, sortby_resources_ini


_contents_lr_body = '''
Our Community team delivers digital security training about Tor to human rights defenders, journalists, activists and marginalized communities around the world.
To request a Tor training for your organization or community, please contact us and send an email to [training at torproject.org](mailto:training@torproject.org).
Or, if you want to teach your community about Tor, these training materials are for you!'''


def slugify(it: str):
    """Slugify a string for use as a lektor content path.

    lektor's own slugify removes characters that should be url-safe, creating ugly-looking URLs.
    """
    # url-safe characters as defined by RFC 3986
    url_safe = string.ascii_lowercase + string.digits + '-._~'

    result = []
    # we're also collapsing multiple replacements to one dash
    # so we don't end up with strings full of "f--o-ob---a-r
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
    """Lektor plugin that generates pages used for the training resources filter

    The training resources list needs a filter that works without javascript or a backend. We
    achieve this by generating a page for every single combination of filters. This is a bad
    solution, but it's also the *only* solution.

    The final number of pages created is `(3 * len(topics)) * (2* len(lang)) * len(author)`.
    Most of these pages are empty. Lektor requires a contents.lr file at every level of the
    content hierarchy, for example the URL `/foo/bar/baz` will require `/foo/contents.lr`,
    `/foo/bar/contents.lr`, and finally `/foo/bar/baz/contents.lr`.
    """

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

    def _format_default(self, to_format: str, **kwargs: str) -> str:
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
            'sortby_resources_visible': '',
            'current_topic': '',
            'current_lang': '',
            'current_lang_code': '',
            'current_author': '',
            'body': '',
        }

        formatting.update(kwargs)
        if formatting['current_lang'] and not formatting['current_lang_code']:
            try:
                languages = self._get_resource_langs(formatting['sortby_resources'])
                language_code, _ = next(filter(lambda item: item[1] == formatting['current_lang'], languages))
                formatting['current_lang_code'] = language_code
            except StopIteration:
                pass

        return to_format.format(**formatting)

    def _get_new_link(self, current_page, new_topic=None, new_lang=None, new_author=None):
        """Helper method to generate a new from one filter page to another."""
        current_url = current_page.url_path.rstrip('/')
        if current_url == '/training/resources':
            current_url = '/'.join([current_url, 'sortby', 'none', 'none', 'none'])

        split_url = current_url.split('/')[:-3]
        split_url.append(new_topic or 'none')
        split_url.append(new_lang or 'none')
        split_url.append(new_author or 'none')

        return '/'.join(split_url)

    def _get_resource_topics(self, resources):
        """Return a set of every author used by at least one resource."""
        # python can pass a dict to jinja, but jinja can't pass a dict to python. it just passes a
        # string representation of the dict
        if type(resources) is str:
            resources = ast.literal_eval(resources)

        topics = ['none']
        for resource in resources.values():
            topics.extend(resource.get('topics', []))

        # remove duplicates
        # order doesn't matter, so we'll take the easy route and just use a set
        return set(topics)

    def _get_resource_langs(self, resources):
        """Return a set of every language used by at least one resource."""
        if type(resources) is str:
            resources = ast.literal_eval(resources)

        languages = [('none', 'none')]
        for resource in resources.values():
            language_list = resource.get('languages', {})
            languages.extend(language_list.items())

        # remove duplicates
        return set(languages)

    def _get_authors(self, resources):
        """Return a set of every author used by at least one resource."""
        if type(resources) is str:
            resources = ast.literal_eval(resources)

        authors = set(('none',))
        for resource in resources.values():
            authors.add(resource['author'])

        #remove duplicates
        return authors

    def generate_files(self):
        with open(os.path.join(self.env.project.tree, 'databags', 'community-training-materials.json'), 'r') as f:
            training_resources = json.load(f)

        with open(os.path.join(self.env.project.tree, 'databags', 'digital-safety-guides.json'), 'r') as f:
            safety_guide_resources = json.load(f)

        training_topics = self._get_resource_topics(training_resources)
        training_languages = self._get_resource_langs(training_resources)
        training_authors = self._get_authors(training_resources)

        safety_topics = self._get_resource_topics(safety_guide_resources)
        safety_languages = self._get_resource_langs(safety_guide_resources)
        safety_authors = self._get_authors(safety_guide_resources)

        self._generate_files(os.path.join('training', 'resources', 'sortby'), training_topics,
                            training_languages, training_authors, training_resources)
        self._generate_files(os.path.join('training', 'digital-privacy-guides', 'sortby'),
                            safety_topics, safety_languages, safety_authors, safety_guide_resources)

    def _generate_files(self, sortby_root, topics, languages, authors, resources):
        """Generate contents.lr files for the sortby fields: topics, languages, author."""
        with open(os.path.join(self.env.project.tree, 'models', 'sortby_resources.ini'), 'w') as f:
            f.write(sortby_resources_ini)

        # lektor won't render a page if it doesn't have a parent contents.lr
        self._generate_file_helper(sortby_root, self._format_default(contents_lr_tmpl))

        sortby_resources = json.dumps(resources.copy())

        # loop through topics
        for topic in topics:
            topic_resources = resources.copy()

            if topic != 'none':
                topic_resources = dict(filter(lambda resource: topic in resource[1].get('topics', []), topic_resources.items()))

            # generate empty templates to make lektor happy
            self._generate_file_helper(os.path.join(sortby_root, slugify(topic)), self._format_default(contents_lr_tmpl))
            self._generate_file_helper(os.path.join(sortby_root, slugify(topic), 'none'), self._format_default(contents_lr_tmpl))

            # generate the actual "filtered resources" contents file
            self._generate_file_helper(
                os.path.join(sortby_root, slugify(topic), 'none', 'none'),
                self._format_default(
                    contents_lr_tmpl,
                    section='Training',
                    color='primary',
                    template='layout.html',
                    title='Training Resources',
                    html='resources-sortby.html',
                    sortby_resources=sortby_resources,
                    sortby_resources_visible='\n'.join(topic_resources.keys()),
                    current_topic=topic if topic != 'none' else '',
                    current_lang='',
                    current_author='',
                    body=_contents_lr_body
                ))

            for language_code, language_name in languages:
                language_resources = topic_resources.copy()
                if language_code != 'none':
                    language_resources = dict(filter(lambda resource: language_code in resource[1]['languages'], language_resources.items()))

                self._generate_file_helper(os.path.join(sortby_root, slugify(topic), language_code), self._format_default(contents_lr_tmpl))
                self._generate_file_helper(
                    os.path.join(sortby_root, slugify(topic), language_code, 'none'),
                    self._format_default(
                        contents_lr_tmpl,
                        section='Training',
                        color='primary',
                        template='layout.html',
                        title='Training Resources',
                        html='resources-sortby.html',
                        sortby_resources=sortby_resources,
                        sortby_resources_visible='\n'.join(language_resources.keys()),
                        current_topic=topic if topic != 'none' else '',
                        current_lang=language_name if language_name != 'none' else '',
                        current_author='',
                        body=_contents_lr_body
                    ))

                for author_name in authors:
                    author_resources = language_resources.copy()

                    if author_name != 'none':
                        author_resources = dict(filter(lambda resource: author_name == resource[1]['author'], author_resources.items()))

                    self._generate_file_helper(
                        os.path.join(sortby_root, slugify(topic), language_code,
                                     slugify(author_name)),
                        self._format_default(
                            contents_lr_tmpl,
                            section='Training',
                            color='primary',
                            template='layout.html',
                            title='Training Resources',
                            html='resources-sortby.html',
                            sortby_resources=sortby_resources,
                            sortby_resources_visible='\n'.join(author_resources.keys()),
                            current_topic=topic if topic != 'none' else '',
                            current_lang=language_name if language_name != 'none' else '',
                            current_author=author_name if author_name != 'none' else '',
                            body=_contents_lr_body
                    ))

    def on_setup_env(self, **extra):
        """Generate files when the lektor process starts, and initialize jinja globals."""
        self.generate_files()

        # functions used by the sortby templates
        self.env.jinja_env.globals['json_loads'] = json.loads
        self.env.jinja_env.globals['get_new_link'] = self._get_new_link
        self.env.jinja_env.globals['get_resource_topics'] = self._get_resource_topics
        self.env.jinja_env.globals['get_resource_langs'] = self._get_resource_langs
        self.env.jinja_env.globals['get_authors'] = self._get_authors
        self.env.jinja_env.globals['slugify'] = slugify

    def on_server_spawn(self, **extra):
        """Generate files when the dev server restarts."""
        self.generate_files()
