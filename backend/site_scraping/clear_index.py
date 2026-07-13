import os
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
index = pc.Index("recipes-index")

index.delete(delete_all=True)
print("Usunieto wszystkie rekordy.")
print(index.describe_index_stats())