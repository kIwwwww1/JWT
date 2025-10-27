from fastapi import FastAPI, HTTPException, Response, Depends
from authx import AuthX, AuthXConfig
from pydantic import BaseModel

app = FastAPI()

class UserLogin(BaseModel):
    name: str
    password: str

config = AuthXConfig()
config.JWT_SECRET_KEY = 'SECRET_KEY'
config.JWT_ACCESS_COOKIE_NAME = 'my_access_token'
config.JWT_TOKEN_LOCATION = ['cookies']

security = AuthX(config=config)

@app.post('/login')
def login(creds: UserLogin, resp: Response):
    if creds.name == 'test' and creds.password == 'test':
        token = security.create_access_token(uid='12345')
        resp.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {'access_token': token}

    raise HTTPException(status_code=401, detail='Неверне данные для входа')


@app.get('/protected', dependencies=[Depends(security.access_token_required)])
def protected():
    return {'data': 'Очень важные данные'}
    


