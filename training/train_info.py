from bs4 import BeautifulSoup
import requests
from config.config_vectordb import VectorDB
from langchain.schema import Document

vector_db = VectorDB()
finaldocx = []
routes = [
    # "https://trungnguyenlegend.com/thong-diep-nha-sang-lap/",
    # "https://trungnguyenlegend.com/lich-su-phat-trien/",
    # "https://trungnguyenlegend.com/hanh-trinh-lap-chi-vi-dai-khoi-nghiep-kien-quoc-cho-thanh-nien-viet/",
    # "https://trungnguyenlegend.com/loi-song-tinh-thuc/",
    "https://trungnguyenlegend.com/trungnguyenecoffee/",
    # "https://trungnguyenlegend.com/trung-nguyen-legend/",
    # "https://trungnguyenlegend.com/lien-he/",
    # "https://trungnguyenlegend.com/tam-nhin-su-mang-gia-tri-cot-loi/"
]

for route in routes:
    response = requests.get(route,verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')

    elements = soup.find_all(class_='wpb_content_element')
    contents = [element.get_text(strip=True) for element in elements]
    fullcontent = ''
    for content in contents:
        fullcontent += content

    finaldocx.append(Document(page_content=fullcontent, metadata={"url": route}))

vector_db.add_vectordb(finaldocx,'webcafe')
