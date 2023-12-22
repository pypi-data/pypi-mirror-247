from setuptools import setup, find_packages

setup(
    name='testppoo',
    version='0.1.1',
    author='Your Name',
    author_email='your.email@example.com',
    description='A short description of your package',
    packages=find_packages(),
    install_requires=[
        'requests',
        'BeautifulSoup4',
        'lxml',
        'pyc',
        'rsa',
        'urllib3',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
