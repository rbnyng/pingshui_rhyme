import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='pingshui_rhyme',
    version='0.14',
    packages=setuptools.find_packages(),
    include_package_data=True,
    description='A Python package for classifying Chinese characters phonologically based on the Middle Chinese Pingshui rhyme scheme',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='rbnyng',
    author_email='',
    url='https://github.com/rbnyng/pingshui_rhyme',
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
            'scrape-pingze=pingshui_rhyme.scraper:scrape_ping_ze_rhyme',
        ],
    },
    package_data={
        'pingshui_rhyme': ['data/organized_ping_ze_rhyme_dict.json'],
    },
)
