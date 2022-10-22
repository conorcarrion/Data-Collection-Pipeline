from setuptools import setup, find_packages

setup(name='my_webscraper',
      version='1.0',
      packages=find_packages(),
      install_requires=[
        'selenium'
        'webdriver_manager',
        'requests',
        'uuid',
        'Path',
        'boto3',
        'hypothesis'
        
      ])