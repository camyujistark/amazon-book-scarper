from setuptools import find_packages, setup

setup(
    name='amznscraper',
    packages=find_packages(),
    version='1.0.0',
    description='Scrape Amazon and get meta data',
    author="Cameron Stark",
    author_email="cam@cystark.com.au",
    license='MIT',
    url='https://github.com/cystark/amznscraper',
    keywords='amazon scraper',
    classifiers=[],
    entry_points={
        'console_scripts': [
            'amznscraper = amznscraper.cli.cli:run',
        ],
    },
    install_requires=[
        'lxml==4.6.5',
    ],
)
