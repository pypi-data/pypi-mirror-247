from setuptools import setup

with open('README.md', 'r') as arq:
    readme = arq.read()

setup(name='zapsign-sdk-python',
    version='0.0.1',
    license='MIT License',
    author='Thayssa Bernardo',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='thayssa@zapsign.com.br',
    keywords='zapsign sdk python',
    description=u'Sdk python para usuários zapsign',
    packages=['zapsign_sdk_python'])