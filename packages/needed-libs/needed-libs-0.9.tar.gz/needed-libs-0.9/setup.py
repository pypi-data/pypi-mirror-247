from setuptools import setup
setup(
    name = 'needed-libs',
    packages = ['needed_libs'],
    version = '0.9',
    install_requires = [
        # cc
        'websocket',
        'httpx',
        'requests',
        'python_ghost_cursor',
        'price_parser',
        
        # Mine
        'python-timeout',
        'python-printr',
        'error_alerts',
        'python-objectifier',
        
        # Socials     
        'tweepy',
        'python-twitter',     
        'praw',
        'instagrapi',
        'moviepy',
        'telethon',
        'yt-dlp',
        
        # Scraping
        'requestium',
        'feedparser',
        'bs4',
        'selenium_shortcuts',
        'python-slugify',

        # Google
        'gspread',
        'googleapiclient',
        'google_auth_oauthlib',
        'google',

        # Server
        'flask',
        'waitress',
        'requests_futures',
        
        # Misc
        'schedule',
        'demoji',
        'ffprobe-python',
        'python-dateutil',
        ]
    )