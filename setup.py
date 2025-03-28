from os import path
from setuptools import setup


here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
    long_description = long_description.replace('./docs/', 'https://github.com/IBM/gauge-web-app-steps/tree/master/docs/')

setup(
    name='gauge-web-app-steps',
    version='0.66',
    description='Provides basic steps for a Gauge project, that runs tests with Selenium and Appium',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/IBM/gauge-web-app-steps',
    author='Tobias Lehmann',
    author_email='derdualist1@gmail.com',
    license='MIT',
    packages=['gauge_web_app_steps', 'gauge_web_app_steps.config', 'gauge_web_app_steps.driver'],
    install_requires=[
        'Appium-Python-Client==4.5.1',
        'getgauge>=0.4.8',
        'numexpr==2.10.2',
        'numpy==2.2.4',
        'scikit-image==0.25.2',
        'selenium==4.30.0',
        'webcolors==24.11.1',
        'webdriver-manager==4.0.2',
    ],
    zip_safe=False
)
