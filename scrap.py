import requests
from bs4 import BeautifulSoup
from db import store_articles_in_mongo

def fetch_articles(base_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    articles_data = []
    page = 1

    # while True: # Scrap de tous les articles
    while page <= 5: # Scrap des 5 premières pages
        try:
            url = f"{base_url}/page/{page}/"
            print(f"Fetching articles from: {url}")

            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            main_tag = soup.find('main')
            if not main_tag:
                print(f"No <main> tag found on page {page}. Stopping.")
                break

            articles = main_tag.find_all('article')
            if not articles:
                print(f"No articles found on page {page}. Stopping.")
                break

            for article in articles:
                img_div = article.find(
                    'div',
                    class_='post-thumbnail picture rounded-img'
                )
                img_tag = img_div.find('img') if img_div else None
                img_url = extract_img_url(img_tag)

                meta_div = article.find(
                    'div',
                    class_='entry-meta ms-md-5 pt-md-0 pt-3'
                )
                tag = (meta_div.find('span', class_='favtag color-b')
                       .get_text(strip=True)
                       ) if meta_div else None
                date = (meta_div.find('span', class_='posted-on t-def px-3')
                        .get_text(strip=True)
                        ) if meta_div else None

                header = (meta_div.find('header', class_='entry-header pt-1')
                          ) if meta_div else None
                a_tag = header.find('a') if header else None
                article_url = a_tag['href'] if a_tag and a_tag.has_attr('href') else None
                title = (a_tag.find('h3').get_text(strip=True)
                         ) if a_tag and a_tag.find('h3') else None

                summary_div = (meta_div.find('div', class_='entry-excerpt t-def t-size-def pt-1')
                               ) if meta_div else None
                summary = summary_div.get_text(strip=True) if summary_div else None

                articles_data.append({
                    'title': title,
                    'image': img_url,
                    'tag': tag,
                    'summary': summary,
                    'date': date,
                    'url': article_url,
                    'author': extract_author(article_url) if article_url else None,
                    'content': extract_content(article_url) if article_url else None,
                    'image_dict': extract_image_dict(article_url) if article_url else None
                })

            page += 1

        except requests.exceptions.RequestException as e:
            print(f"Error fetching page {page}: {e}")
            break

    return articles_data

def extract_img_url(img_tag):
    if not img_tag:
        return None
    url_attributes = [
        'data-lazy-src',   
        'data-src',         
        'src'               
    ]
    for attr in url_attributes:
        if img_tag.has_attr(attr):
            url = img_tag[attr]
            if url and url.startswith('https://'):
                return url
    return None


def extract_author(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        byline = soup.find('span', class_='byline')
        if byline:
            author = byline.get_text(strip=True)
            return author
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching author from {url}: {e}")
        return None

def extract_content(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        content_div = soup.find('div', class_='entry-content')
        if content_div:
            elements = content_div.find_all(['h2', 'p', 'a'])
            formatted_content = ""
            for element in elements:
                if element.name == 'h2':
                    formatted_content += f"\n\n{element.get_text(strip=True)}\n"
                elif element.name == 'p':
                    formatted_content += f"{element.get_text(strip=True)}\n"
                elif element.name == 'a':
                    link_text = element.get_text(strip=True)
                    link_url = element.get('href', '')
                    formatted_content += f"[{link_text}]({link_url})\n"
            return formatted_content.strip()
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching content from {url}: {e}")
        return None

def extract_image_dict(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    images_dict = {}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all('img')

        for img_tag in img_tags:
            img_url = extract_img_url(img_tag)
            if img_url:
                alt_text = img_tag.get('alt', '').strip() or None
                images_dict[img_url] = alt_text

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        images_dict[url] = None

    return images_dict

url = "https://www.blogdumoderateur.com/web"
articles = fetch_articles(url)

for i, article in enumerate(articles, 1):
    print(f"\nArticle {i}:")
    for key, value in article.items():
        print(f"{key.capitalize()}: {value}")

store_articles_in_mongo(articles)