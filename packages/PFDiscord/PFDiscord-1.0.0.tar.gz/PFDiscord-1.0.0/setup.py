from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='PFDiscord',
    version='1.0.0',
    packages=find_packages(),
    license='AGPL-3.0',
    author='Digital Heretic',
    author_email='agiheretic@proton.me',
    description='OpenAI GPT, driven by Discord',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Digital-Heresy/PFDiscord',
    install_requires=[
        'openai',
        'PyYAML',
        'typing',
        'validators',
        'discord.py',
        'tiktoken'
    ],
    python_requires='>=3.10',
)