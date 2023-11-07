import ast
import io
import re

from setuptools import setup, find_packages

with io.open('README.md', 'rt', encoding="utf8") as f:
    readme = f.read()

_description_re = re.compile(r'description\s+=\s+(?P<description>.*)')

with open('lektor_community_good_bad_isps.py', 'rb') as f:
    description = str(ast.literal_eval(_description_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
    author='bauruine',
    description=description,
    keywords='Lektor plugin',
    long_description=readme,
    long_description_content_type='text/markdown',
    name='lektor-community-good-bad-isps',
    packages=find_packages(),
    py_modules=['lektor_community_good_bad_isps'],
    # url='[link to your repository]',
    version='0.4.3',
    classifiers=[
        'Framework :: Lektor',
        'Environment :: Plugins',
    ],
    entry_points={
        'lektor.plugins': [
            'community-good-bad-isps = lektor_community_good_bad_isps:CommunityGoodBadIspsPlugin',
        ]
    }
)
