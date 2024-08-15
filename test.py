from config.config_vectordb import VectorDB
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

vector_db = VectorDB()
finaldocx = []

def get_routes_with_specific_path(base_url, path_contains, page):

    specific_routes = []
    for i in range(1,page + 1):
        url = base_url + '?p='+ str(i)
        try:
            response = requests.get(url,verify=False)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Lỗi khi truy cập {route}: {e}")
            return None
        
        soup = BeautifulSoup(response.text, 'html.parser')

        for link in soup.find_all('a'):
            href = link.get('href')
            if not href:
                continue

            full_url = urljoin(url, href)

            if path_contains in full_url:
                specific_routes.append(full_url)

    return specific_routes

def fetch_data_from_class(route, class_names):
    try:
        response = requests.get(route,verify=False)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        combined_text = ''
        for class_name in class_names:
            elements = soup.find_all(class_=class_name)
            if elements and elements[0]:
                combined_text = combined_text + [element.get_text() for element in elements][0]
        return combined_text
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi truy cập {route}: {e}")
        return None

# base_url = 'https://cafe.net.vn/cong-thuc-pha-che.html'
# page = 4
# path_contains = '/cong-thuc-pha-che/'
# title = 'Công thức pha chế'

base_url = 'https://cafe.net.vn/ca-phe.html'
page = 5
path_contains = '/ca-phe/'
title = 'Cà phê'

class_names = ['product-info-main','description']


filtered_routes = get_routes_with_specific_path(base_url, path_contains, page)

for route in filtered_routes:
    page_content = fetch_data_from_class(route, class_names)
    if page_content != '':
        finaldocx.append(Document(page_content=page_content, metadata={"url": route, "type": title}))

vector_db.add_vectordb(finaldocx,'webcafe')
