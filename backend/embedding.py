from models import ContentEmbedding, Title, session
import openai
import os

openai.api_key = os.getenv("OPEN_API_KEY")
db = session()

titles = db.query(Title).all()

for law in titles:
    print(f"Embedding {law.id}: {law.title[:30]}...")
    response = openai.embeddings.create(model="text-embedding-3-small", input = law.content)
    vector = response.data[0].embedding

    embed = ContentEmbedding(law_id = law.id, embedding = vector)
    db.merge(embed)
    db.commit()
    print(f"Finished Embedding {law.id}")

db.close()

