from setuptools import setup, find_packages

setup(
    name='OnlineDatabase',
    version='0.1.0',
    description='Just a normal package to save data online',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    install_requires=[
        'aiohttp>=3.8.1',
        'PyGithub>=2.3.0',
        'huggingface_hub>=0.24.5',
    ],
    test_suite='tests',
    tests_require=[
        'unittest2',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
