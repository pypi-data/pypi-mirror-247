from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='CERMatch',
    version='0.420.69',
    packages=find_packages(),
    install_requires=[
        'fastwer==0.1.3',
        'unidecode==1.3.7',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Diego Bonilla',
    author_email='diegobonila@gmail.com',
    url='https://github.com/diegobonilla98/CERMatch'
)
