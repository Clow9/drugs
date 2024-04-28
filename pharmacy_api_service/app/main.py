import uvicorn
from fastapi import FastAPI, HTTPException, status
import requests

app = FastAPI()

API_KEY = "KDQdydwA8aTXrLif8o1ublmBRKbwxa5WT9IGRZug"


@app.get("/health", status_code=status.HTTP_200_OK)
async def service_alive():
    return {'message': 'service alive'}


@app.get("/drug_labels")
async def get_drug_labels(search_query: str):
    url = f"https://api.fda.gov/drug/label.json"
    params = {
        "search": search_query,
        "api_key": API_KEY,
        "limit": 1
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Error retrieving data from OpenFDA API")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
