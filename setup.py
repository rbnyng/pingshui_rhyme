import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='pingze_classifier',
    version='0.11',
    packages=setuptools.find_packages(),
    include_package_data=True,
    description='A Python package for classifying Chinese characters based on the Pingshui rhyme scheme',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='rbnyng',
    author_email='',
    url='https://github.com/rbnyng/pingze_classifier',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'beautifulsoup4',
        'requests',
    ],
    extras_require={
        'dev': [
            'pytest',
            'coverage',
        ],
    },
    entry_points={
        'console_scripts': [
            'scrape-pingze=pingze_classifier.scraper:scrape_ping_ze_rhyme',
        ],
    },
    package_data={
        'pingze_classifier': ['data/organized_ping_ze_rhyme_dict.json'],
    },
)
