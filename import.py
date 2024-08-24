import pandas as pd
from config.config_vectordb import VectorDB
from langchain.schema import Document

data = pd.read_excel('gift.xlsx')
vector_db = VectorDB()
finaldocx = []
for index, row in data.iterrows():
    content = row.content
    finaldocx.append(Document(page_content=content, metadata={"url": row.url, "type": row.type, "image": row.image}))

vector_db.add_vectordb(finaldocx,'webcafe')