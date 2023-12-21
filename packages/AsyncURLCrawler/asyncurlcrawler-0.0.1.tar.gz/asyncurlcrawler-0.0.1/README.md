# AsyncURLCrawler
AsyncURLCrawler navigates through web pages concurrently by following hyperlinks to collect URLs.
AsyncURLCrawler uses BFS algorithm. To make use of it check `robots.txt` of the domain.

### Install Pacakge

```commandline 
   pip install 
   ```
👉 The official [page]() of the project in PyPi.

---

### Usage Example

Here is a simple python script to show how to use the package:

```python
import asyncio
import os
from AsyncURLCrawler.parser import Parser
from AsyncURLCrawler.crawler import Crawler
import yaml


async def main():
    parser = Parser(
        delay_start=0.1,  # Delay between consecutive requests when the request is failed. 
        max_retries=5,  # Maximum number of retries on a URL
        request_timeout=1, # Request timeout to fetch a URL
        user_agent="Mozilla", # User agent in HTTP request
    )
    # Check the table in the bottom of readme
    crawler = Crawler( 
        seed_urls=["https://pouyae.ir"],
        parser=parser,
        exact=True,
        deep=False,
        delay=0.1,
    )
    result = await crawler.crawl()
    with open(
            os.path.join(output_path, 'result.yaml'), 'w') as file:
        for key in result:
            result[key] = list(result[key])
        yaml.dump(result, file)


if __name__ == "__main__":
    asyncio.run(main())
```

---

### Build and Publish to Python Package Index(PyPi)

👉 For more details check [Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/).

```commandline 
   1. python3 -m build
   ```

```commandline
    2. python3 -m twine upload --repository pypi dist/*
   ```
---

### Run with Docker 🐳

```commandline 
   1. docker build -t crawler .
   ```

```commandline
    2. docker run -v my_dir:/src/output --name crawler crawler
   ```

After execution of the image, 
the resulting output file will be accessible in the directory named "my_dir" as defined in 2.
To change the output path check the volume in Dockerfile.

To customize the script as your needs, there is `cmd.py` file, which accepts various arguments for configuring the crawler:

| argument  | description                                                                                                                        | 
|-----------|------------------------------------------------------------------------------------------------------------------------------------| 
| `--url`   | Specify a list of URLs to be crawled. Ensure at least one URL is provided.                                                         | 
| `--exact` | Optional flag; if enabled, the crawler focuses exclusively on the specified subdomain/domain. Default is false.                    | 
| `--deep`  | Optional flag; when activated, the crawler explores all visited URLs (not recommended). If --deep is true, --exact is disregarded. | 
| `--delay` | Define the delay between consecutive HTTP requests (in seconds).                                                                   |
| `--output`| Specify the path for the output file, formatted as a YAML file.                                                                                        |

---

### TODO List

- Add unit tests.
- Make documentation better

### Disclaimer

**⚠️ Use at your own risk. The author and contributors are not responsible for any misuse or consequences resulting from the use of this project.**