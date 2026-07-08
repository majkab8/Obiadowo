import requests
import json
from bs4 import BeautifulSoup
already_scraped = set()

def find_recipe_links(category_url, domain, pages=3):
    global already_scraped
    found_links = set()

    for page in range(1, pages + 1):
        url = f"{category_url}?page={page}" if page > 1 else category_url
        print(f"Searching for recipes on page {page}: {url}")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7'
        }

        response = requests.get(category_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        for link in soup.find_all('a', href=True):
            href = link['href']
            if '/przepis/' in href or 'przepis/' in href:
                if '#' in href:
                    continue
                if href.startswith('/'):
                    href = f"{domain}{href}"
                if domain in href and href not in already_scraped:
                    found_links.add(href)

        print(f"Found {len(found_links)} links to recipes!")

    new_links = list(found_links)[:5]
    already_scraped.update(new_links)
    return new_links


def find_recipe_in_json(node):
    if isinstance(node, dict):
        t = node.get('@type', '')
        if (isinstance(t, str) and 'Recipe' in t) or (isinstance(t, list) and 'Recipe' in t):
            return node
        for v in node.values():
            res = find_recipe_in_json(v)
            if res: return res
    elif isinstance(node, list):
        for item in node:
            res = find_recipe_in_json(item)
            if res: return res
    return None


def extract_recipe_data(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.find('h1').text.strip() if soup.find('h1') else "No title"

    for script in soup.find_all('script', type='application/ld+json'):
        try:
            data = json.loads(script.text)
            recipe_data = find_recipe_in_json(data)

            if recipe_data:
                ingredients = recipe_data.get('recipeIngredient', [])
                ing_str = "\n".join(ingredients) if isinstance(ingredients, list) else str(ingredients)

                instr = recipe_data.get('recipeInstructions', [])
                instr_str = ""
                if isinstance(instr, list):
                    for step in instr:
                        if isinstance(step, dict) and 'text' in step:
                            instr_str += step['text'] + "\n"
                        elif isinstance(step, str):
                            instr_str += step + "\n"
                else:
                    instr_str = str(instr)

                return {"title": title, "ingredients": ing_str, "instructions": instr_str, "url": url}
        except:
            continue

    ingredients_list = []

    headers_tags = soup.find_all(lambda tag: tag.name in ['h2', 'h3', 'h4', 'div', 'strong', 'p']
                                             and 'składniki' in tag.text.lower()
                                             and 'krok' not in tag.text.lower()
                                             and 'sposób' not in tag.text.lower()
                                             and len(tag.text) < 60)

    for header in headers_tags:
        if 'kopiuj' in header.text.lower() or 'więcej' in header.text.lower():
            continue

        clean_header = header.text.replace('[', '').replace(']', '').replace('więcej', '').strip()
        items = []

        # Skipping ads and other unnecessary stuff
        curr = header.next_sibling
        for _ in range(5):
            if curr is None: break
            if hasattr(curr, 'find_all'):
                found = curr.find_all(['li', 'label'])
                if found:
                    items = found
                    break
            curr = curr.next_sibling

        if not items and header.parent:
            curr = header.parent.next_sibling
            for _ in range(5):
                if curr is None: break
                if hasattr(curr, 'find_all'):
                    found = curr.find_all(['li', 'label'])
                    if found:
                        items = found
                        break
                curr = curr.next_sibling

        temp_ingredients = []
        if items:
            for item in items:
                text = item.text.strip()
                if text and text.lower() != 'składniki' and text not in ingredients_list:
                    temp_ingredients.append(text)

        # Saving if found anything
        if temp_ingredients:
            header_text = f"\n--- {clean_header} ---"
            if header_text not in ingredients_list:
                ingredients_list.append(header_text)
            ingredients_list.extend(temp_ingredients)

    ingredients_list = [i for i in ingredients_list if i]

    if len(ingredients_list) > 1:
        final_ingredients = "\n".join(ingredients_list).strip()

        instructions_list = []
        seen_steps = set()

        for tag in soup.find_all('div'):
            text = tag.get_text(strip=True)
            if text.lower().startswith('krok ') and ':' in text and len(text) > 20:
                if text not in seen_steps:
                    seen_steps.add(text)
                    instructions_list.append(text)

        if not instructions_list:
            for tag in soup.find_all(['h2', 'h3']):
                if 'przepis' in tag.get_text(strip=True).lower():
                    for sibling in tag.find_next_siblings():
                        if sibling.name in ['h2', 'h3']:
                            break
                        if sibling.name == 'p':
                            text = sibling.get_text(strip=True)
                            if text and len(text) > 30:  # pomijaj krótkie teksty
                                instructions_list.append(text)
                    if instructions_list:
                        break

        instr_str = "\n".join(instructions_list) if instructions_list else "Brak."

        return {
            "title": title,
            "ingredients": final_ingredients,
            "instructions": instr_str,
            "url": url
        }

    raise Exception("No standard, couldn't find any recipes!")
