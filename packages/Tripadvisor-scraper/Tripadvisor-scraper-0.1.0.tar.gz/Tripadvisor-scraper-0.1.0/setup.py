from setuptools import setup, find_packages

setup(
    name='Tripadvisor-scraper',
    version='0.1.0',
    packages=find_packages(),
    author='Oxylabs',
    author_email='marketing@oxylabs.io',
    description="The basics of forming an input code for scraping travel industry pages with Tripadvisor Scraper API + an example of results.",
    long_description="""# Tripadvisor Scraper

[![Oxylabs promo code](https://user-images.githubusercontent.com/129506779/250792357-8289e25e-9c36-4dc0-a5e2-2706db797bb5.png)](https://oxylabs.go2cloud.org/aff_c?offer_id=7&aff_id=877&url_id=112)

[<u>Tripadvisor Scraper API</u>](https://oxylabs.io/products/scraper-api/web/tripadvisor) is an advanced web data extraction solution with an emphasis on scale, saved time, and instant results. The following introduces the basics of getting started with Tripadvisor Scraper API.

## How it works

You can provide us with any Tripadvisor URL, and we will return the results right away.

### Python input code example

The code example below shows an input code to be provided to the API.

```python
import requests
from pprint import pprint

# Structure payload.
payload = {
    'source': 'universal',
    'url': 'https://www.tripadvisor.com/Restaurants-g60763-New_York_City_New_York.html',
    'user_agent_type': 'desktop',
    'geo_location': 'United States'
}

# Get a response.
response = requests.request(
    'POST',
    'https://realtime.oxylabs.io/v1/queries',
    auth=('USERNAME', 'PASSWORD'),
    json=payload
)

# Instead of response with job status and results url, this will return the
# JSON response with results.
pprint(response.json())
```
### Output example

```json
{
    "results": [
        {
            "content": "<!doctype html>\n<html lang=\"en\">\n<head>...</script></body>\n</html>\n",
            "created_at": "2023-07-26 12:07:08",
            "job_id": "7089939195182992385",
            "page": 1,
            "status_code": 200,
            "updated_at": "2023-07-26 12:07:41",
            "url": "https://www.tripadvisor.com/Restaurants-g60763-New_York_City_New_York.html"
        }
    ]
}
```

Tripadvisor Scraper API automates the bulk of the underlying processes and ensures a block-free experience. 

If you have any questions, please [email us](mailto:support@oxylabs.io) or drop a message via the live chat on our homepage.

```
""",
    long_description_content_type='text/markdown',
    url='https://oxylabs.io/products/scraper-api/web/tripadvisor',
    project_urls={
        'Documentation': 'https://developers.oxylabs.io/scraper-apis/web-scraper-api',
        'Source': 'https://github.com/oxylabs/tripadvisor-scraper',
        'Bug Reports': 'https://github.com/oxylabs/tripadvisor-scraper/issues',
    },
    keywords='tripadvisor-scraper, tripadvisor-scrape, scrape-tripadvisor,',
    license='MIT',

    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.6',
)









