# Bus factor estimation

Bus factor is a measurement which attempts to estimate the number of key persons a
project would need to lose in order for it to become stalled due to lack of expertise.

This program assumes a project's bus factor is 1 if it's most active developer's 
contributions account for 75% or more of the total contributions count from the top 25 most active
developers.

### Environment

```python3 -m pip install pipenv```

```pipenv shell```

```pipenv install -d```


### Run 

```GIT_TOKEN=your_private_github_token python3 bus_factor.py --language golang --project_count 120```

Generate your_private_github_token:

https://github.com/settings/tokens

Docs: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic

![Screenshot 2021-12-19 224453](https://user-images.githubusercontent.com/40454834/146691899-a5dd062e-4749-4254-89d3-2e27045c4585.jpg)

### Run tests

```python3 -m pytest tests/```
