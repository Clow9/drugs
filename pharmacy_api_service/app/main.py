import uvicorn
from fastapi import FastAPI, status, Form, Header, HTTPException, Depends
import requests
from keycloak import KeycloakOpenID

app = FastAPI()

API_KEY = "KDQdydwA8aTXrLif8o1ublmBRKbwxa5WT9IGRZug"

KEYCLOAK_URL = "http://keycloak:8080/"
KEYCLOAK_CLIENT_ID = "testClient"
KEYCLOAK_REALM = "testRealm"
KEYCLOAK_CLIENT_SECRET = "**********"

keycloak_openid = KeycloakOpenID(server_url=KEYCLOAK_URL,
                                 client_id=KEYCLOAK_CLIENT_ID,
                                 realm_name=KEYCLOAK_REALM,
                                 client_secret_key=KEYCLOAK_CLIENT_SECRET)


@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    try:
        token = keycloak_openid.token(grant_type=["password"],
                                      username=username,
                                      password=password)
        return token
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Не удалось получить токен")


def chech_for_role_test(token):
    try:
        token_info = keycloak_openid.introspect(token)
        if "test" not in token_info["realm_access"]["roles"]:
            raise HTTPException(status_code=403, detail="Access denied")
        return token_info
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token or access denied")


@app.get("/health", status_code=status.HTTP_200_OK)
async def service_alive(token: str = Header()):
    if (chech_for_role_test(token)):
        return {'message': 'service alive'}
    else:
        return "Wrong JWT Token"


@app.get("/drug_labels")
async def get_drug_labels(search_query: str, token: str = Header()):
    if (chech_for_role_test(token)):
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
    else:
        return "Wrong JWT Token"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
