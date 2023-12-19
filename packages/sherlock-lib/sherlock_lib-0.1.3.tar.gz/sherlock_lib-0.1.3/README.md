<p align=center>
  <br>
  <img width="70%" height="70%" src="https://raw.githubusercontent.com/PaPaPaulitos/sherlock-lib/master/images/sherlock-lib-logo.svg">
  <br>
  <span>A fork of the <a href="https://github.com/sherlock-project/sherlock">Sherlock Project</a></span>
  <br>
  <a href="https://github.com/sherlock-project/sherlock/blob/master/sites.md">List of social networks</a>
  <br>
</p>

This library was created to use the Sherlock Project in your own personal scripts.


## Installation

```console
# installing using pip
$ pip install sherlock-lib
```

## Usage

```python
def search_target(username,timeout=60,sfw=False)
```

- **Username**: Target's name on social media
- **Timeout**: Maximum search time on each site
- **Safe for Work**: Remove NSFW(Not Safe for Work) sites

> This function returns a dictionary with the name of the sites and the link to the target's profile on the sites.

### Example

```python
from sherlock_lib import search_target

username = "john_doe"

result = search_target(username,sfw=True)

for k, v in result.items():
    print(f"{k}: {v}")

```

## Contributing
We would love to have you help us with the development of Sherlock. Each and every contribution is greatly valued!

Here are some things we would appreciate your help on:
- Addition of new site support ¹
- Bringing back site support of [sites that have been removed](removed_sites.md) in the past due to false positives

[1] Please look at the Wiki entry on [adding new sites](https://github.com/sherlock-project/sherlock/wiki/Adding-Sites-To-Sherlock)
to understand the issues.



## License

- MIT © Sherlock Project<br/>
- Original Creator - [Siddharth Dushantha](https://github.com/sdushantha)
- Lib Creator - [Paulo Ricardo Mesquita](https://github.com/PaPaPaulitos)
