# Online Python Database

## Description

Push and get json files to huggingface, github with Python

**Requirement:** Python 3.10

## Install

```python
pip install git+https://github.com/phuvinhnguyen/OnlineDatabase.git
```

## How to use
```python
from OnlineDatabase.OnlineDatabase import GitHubManager

manager = GitHubManager('YOUR_GITHUB_TOKEN')
manager.push(
    'YOUR_GITHUB/YOUR_PROJECT',
    'examples/test.txt',
    'This is an example content of how to use the project\nThis is the second line in the file\n\nNow is the end of this file.'
    )
content = manager.pull('YOUR_GITHUB/YOUR_PROJECT', 'examples/test.txt')

print(content)
```