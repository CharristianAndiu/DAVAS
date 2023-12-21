from search import Searcher

from fastapi import FastAPI, APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Dict
from elasticsearch import Elasticsearch
import json
from fastapi import FastAPI, Body, Request
from fastapi.responses import JSONResponse
from typing import Optional
from fastapi.exceptions import RequestValidationError
import uvicorn
app = FastAPI() # 创建 api 对象
@app.exception_handler(RequestValidationError)  # 重写了RequestValidationError的 exception_handler方法
async def post_validation_exception_handler(request: Request, exc: RequestValidationError):
    print(f'参数不对{request.method},{request.url}')
    return JSONResponse({'code': 400, 'msg': exc.errors()})

es = Elasticsearch()

def convert_quotes(dictionary):
    new_dict = {}
    for key, value in dictionary.items():
        key_str = str(key).replace("'", '"')
        value_str = str(value).replace("'", '"')
        new_dict[key_str] = value_str
    return new_dict


app = FastAPI()
import pymysql
conn = pymysql.connect(host='127.0.0.1',
                       port=3306,
                       user="root",
                       passwd="123456",
                        db="user_data",
                       charset="utf8mb4"
                       )
# 获取游标
cursor = conn.cursor()
#创建表格
sql = "CREATE TABLE users(username TEXT,email TEXT,full_name TEXT,disabled BOOL,password TEXT)"
try:
    cursor.execute(sql)
    conn.commit()
except:
    print("表已存在")
print('成功创建表格')

class User(BaseModel):
    username: str
    email: str
    full_name: str
    disabled: bool
    password:str

class UserSignIn(BaseModel):
    username: str
    email: str
    password: str

users: Dict[str, User] = {}  # Storing user data in a dictionary (in-memory storage)
A = {
    "username":"A",
    "email":"A@goodemail",
    "full_name":"AA",
    "disabled":"true",
    "password":"123456"
}


users[A["email"]] = A
user_router = APIRouter(tags=["User"])
@user_router.get("/") # 根路由
def root():
    return users

@user_router.post("/signup")
async def signup_new_user(data: User) -> dict:
    """Create a new user"""
    if data.email in users:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with supplied email address already exists"
        )
    if data.username in users:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with the same username already exists"
        )
    users[data.email] = data
    print(data)
    return {"message": "User successfully registered!"}

@user_router.post("/signin")
async def signin_new_user(data: UserSignIn) -> dict:
    """User login"""
    if data.email not in users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist"
        )
    if users[data.email].password != data.password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect password"
        )
    return {"message": "User signed in successfully!"}
app.include_router(user_router)
user_router = APIRouter(tags=["search"])
@app.get("/") # 根路由
def root():
    return
@app.get("/search_by_keywords") # 根路由
def search(keywords:str,method : str):

    se = Searcher()
    result = se.search(keywords, method)
    all_data=[]
    for j in result:
        new_str = json.dumps(j["_source"],indent=4).replace("'", '"')
        print(new_str)


        all_data.append(j)
    json.dumps(all_data, indent=2)
    return {all_data}






if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)