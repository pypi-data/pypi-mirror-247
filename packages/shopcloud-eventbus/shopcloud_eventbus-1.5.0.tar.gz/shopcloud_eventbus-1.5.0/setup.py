from setuptools import find_packages, setup

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = {
    "name": 'shopcloud_eventbus',
    "version": '1.5.0',
    "description": 'CLI tool for the Shopcloud EventBus',
    "long_description_content_type": "text/markdown",
    "long_description": README,
    "license": 'MIT',
    "packages": find_packages(),
    "author": 'Konstantin Stoldt',
    "author_email": 'konstantin.stoldt@talk-point.de',
    "keywords": ['CLI'],
    "url": 'https://github.com/Talk-Point/shopcloud-eventbus',
    "scripts": ['./scripts/eventbus'],
}

install_requires = [
    'pyyaml',
    'shopcloud-secrethub>=2.12.0',
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
