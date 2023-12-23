from search import Searcher
from search_all import  Searcher_all
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
    result_all= Searcher_all.search(keywords, method)

    s =[]
    for j in result:
        new_str = j["_source"]
        # print(type(new_str))
        s.append(new_str)
        # print(new_str)
    for j in result_all:
        new_str = j["_source"]
        # print(type(new_str))
        s.append(new_str)
    s = json.dumps(s,indent=4,ensure_ascii=False).replace("'", '"')

    file_path = './output.json'
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(s)

    # print(s)

    return {s}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)