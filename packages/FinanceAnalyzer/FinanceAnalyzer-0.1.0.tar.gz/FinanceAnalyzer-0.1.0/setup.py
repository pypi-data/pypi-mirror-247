from setuptools import setup, find_packages

setup(
    name='FinanceAnalyzer',
    version='0.1.0',
    author='Antonin Siska',
    author_email='siska.antonin.mail@gmail.com',
    description='Package that can analyze you tradings',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3'
    ],
    python_requires='>=3.6',
)