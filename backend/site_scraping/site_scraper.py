import time
from crawler import find_recipe_links, extract_recipe_data


def download_recipes(category_url, domain):
    urls = find_recipe_links(category_url, domain)
    scraped_recipes = []

    for url in urls:
        try:
            print(f"Downloading: {url}")
            recipe_data = extract_recipe_data(url)
            if recipe_data is None:
                raise Exception("Scraper returned 'Nic' (None). Recipe not foundd.")
            scraped_recipes.append(recipe_data)
            print(f"Successfully downloaded: {recipe_data['title']}")

            time.sleep(2)

        except Exception as e:
            print(f"Failed to download {url}. Error: {e}")

    return scraped_recipes