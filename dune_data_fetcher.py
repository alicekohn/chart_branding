from dotenv import load_dotenv
import os
from dune_client.client import DuneClient
from dune_client.query import QueryBase
import pandas as pd


load_dotenv()
DUNE_API_KEY = os.getenv("DUNE_API_KEY")
if not DUNE_API_KEY:
    raise ValueError("DUNE_API_KEY not found. Please set it in the .env file.")

dune = DuneClient(DUNE_API_KEY)
#DUNE_API_KEY= "dRcv5ptfGc2NLnbZ1osOqKF2WwTXfPCY"
#dune = DuneClient(DUNE_API_KEY)

query = QueryBase(
    query_id=3910571)


try:
    query_result = dune.get_latest_result_dataframe(query=query)
except Exception as e:
    print(f"An error occurred: {e}")


query_result.to_csv("karak_tvl.csv")