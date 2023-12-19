from setuptools import setup, find_packages

setup(
    name='yelp-scraper-api',
    version='1.0.0',
    packages=find_packages(),
    author='Oxylabs',
    author_email='marketing@oxylabs.io',
    description="Yelp Scraper for hassle-free public Yelp data collection, including search results, comments, profiles, posts, and more.",
    long_description="""# Yelp Scraper
[![Oxylabs promo code](https://user-images.githubusercontent.com/129506779/250792357-8289e25e-9c36-4dc0-a5e2-2706db797bb5.png)](https://oxylabs.go2cloud.org/aff_c?offer_id=7&aff_id=877&url_id=112)


[<u>Yelp Scraper</u>](https://oxylabs.io/products/scraper-api/web/yelp)
enables you to scrape public Yelp data with ease and on any scale. This
guide will show you how to scrape Yelp using Oxylabs’ [<u>Scraper
API</u>](https://oxylabs.io/products/scraper-api).

## How it works

You can extract data from Yelp by sending a request to our API. The
service will send back the HTML of any Yelp page you want to scrape.

### Python code example

This Python code sends a request to the API and retrieves the HTML of
the Yelp search results for the best burgers near Frankfurt am Main,
Hessen:

```python
import requests
from pprint import pprint

# Structure payload.
payload = {
    'source': 'universal_ecommerce',
    'url': 'https://www.yelp.co.uk/search?find_desc=Burgers&find_loc=Frankfurt,%20Hessen,%20Germany'
}

# Get response.
response = requests.request(
    'POST',
    'https://realtime.oxylabs.io/v1/queries',
    auth=('USERNAME', 'PASSWORD'),  # Your credentials go here
    json=payload
)

# Instead of response with job status and results URL, this will return the
# JSON response with results.
pprint(response.json())
```

Head to the
[<u>documentation</u>](https://developers.oxylabs.io/scraper-apis/web-scraper-api)
for information regarding payload parameters.

### Output sample
```json
{
    "results": [
        {
            "content": "<!doctype html>\n<html lang=\"en\">\n<head>
            ... 
            </script></body>\n</html>\n",
            "created_at": "2023-06-06 13:24:56",
            "updated_at": "2023-06-06 13:25:01",
            "page": 1,
            "url": "https://www.yelp.co.uk/search?find_desc=Burgers&find_loc=Frankfurt,%20Hessen,%20Germany",
            "job_id": "7071839378003205121",
            "status_code": 200
        }
    ]
}
```
With Oxylabs’ Yelp Scraper API, you can forget about dealing with
complex anti-bot systems and effortlessly collect public Yelp data,
including search results, comments, profiles, posts, images, and much
more. Don’t hesitate to contact us via [<u>live
chat</u>](https://oxylabs.io/) or
[<u>email</u>](mailto:support@oxylabs.io) in case you have any
questions.
""",
    long_description_content_type='text/markdown',
    url='https://oxylabs.io/products/scraper-api/web/yelp',
    project_urls={
        'Documentation': 'https://developers.oxylabs.io/scraper-apis/web-scraper-api',
        'Source': 'https://github.com/oxylabs/yelp-scraper',
        'Bug Reports': 'https://github.com/oxylabs/yelp-scraper/issues',
    },
    keywords='yelp-scraper,Yelp-scraper,yelp-web-scraper, web-scraper-api, scraping-yelp, yelp-data,',
    license='MIT',

    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.6',
)









