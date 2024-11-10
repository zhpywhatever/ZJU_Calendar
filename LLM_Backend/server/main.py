import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_process import preprocess

app = FastAPI()

# 添加CORS中间件
origins = [
    "http://localhost:8081",  # 前端地址
    "http://127.0.0.1:8081",
    "http://localhost:8082"
    # 其他允许的源
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 允许的来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许的HTTP方法
    allow_headers=["*"],  # 允许的HTTP头
)

class FieldData(BaseModel):
    text: str

class Fields(BaseModel):
    ID: FieldData
    text: FieldData

class InputData(BaseModel):
    fields: Fields

# 存储数据的文件路径
FILE_PATH = "../output.json"

@app.post("/append_to_file")
async def append_to_file(input_data: InputData):
    try:
        # 提取字段并将其存储为字典
        fields = input_data.dict()

        # 创建一个列表来存储所有文本数据
        result = [fields]

        # 如果文件存在，读取现有数据
        if os.path.exists(FILE_PATH):
            with open(FILE_PATH, "r", encoding="utf-8") as file:
                existing_data = json.load(file)
        else:
            existing_data = []

        # 将新数据追加到现有数据中
        existing_data.extend(result)

        # 将更新后的数据写入文件
        with open(FILE_PATH, "w", encoding="utf-8") as file:
            json.dump(existing_data, file, ensure_ascii=False, indent=4)

        result = preprocess()

        return {"message": "Data successfully appended to file.", "data": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_db_connection():
    conn = sqlite3.connect('../spider1/notices.db')
    conn.row_factory = sqlite3.Row
    return conn

class Notice(BaseModel):
    title: str
    date: str
    link: str
    content: str

@app.get("/notices/{table_name}", response_model=list[Notice])
def read_notices(table_name: str, limit: int = 10):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(f"SELECT title, date, link, content FROM {table_name} ORDER BY date DESC LIMIT ?", (limit,))
    notices = cursor.fetchall()

    conn.close()

    if not notices:
        raise HTTPException(status_code=404, detail="No notices found")

    validated_notices = []
    for notice in notices:
        try:
            validated_notices.append(Notice(**dict(notice)))
        except ValidationError as e:
            print(f"Validation error for notice: {notice}")
            print(e)

    return validated_notices


@app.get("/notices/{table_name}/{notice_id}", response_model=Notice)
def read_notice(table_name: str, notice_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(f"SELECT title, date, link, content FROM {table_name} WHERE id = ?", (notice_id,))
    notice = cursor.fetchone()

    conn.close()

    if notice is None:
        raise HTTPException(status_code=404, detail="Notice not found")

    try:
        return Notice(**dict(notice))
    except ValidationError as e:
        print(f"Validation error for notice: {notice}")
        print(e)
        raise HTTPException(status_code=400, detail="Invalid notice data")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)