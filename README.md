# Bus factor estimation

Bus factor is a measurement which attempts to estimate the number of key persons a
project would need to lose in order for it to become stalled due to lack of expertise.

This program assumes a project's bus factor is 1 if it's most active developer's 
contributions account fot 75% or more of the total contributions count from the top 25 most active
developers.

### Environment

- python 3.9 
- aiohttp==3.8.1

### Run 

```./bus_factor.py --language rust --project_count 120```
