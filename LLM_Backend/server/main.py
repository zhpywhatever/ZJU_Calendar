import sqlite3

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os

from data_process import preprocess

app = FastAPI()

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
    conn = sqlite3.connect('yunfeng_notices.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/notices/")
def read_notices(limit: int = 10):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM notices ORDER BY date DESC LIMIT ?", (limit,))
    notices = cursor.fetchall()

    conn.close()

    if not notices:
        raise HTTPException(status_code=404, detail="No notices found")

    return [dict(notice) for notice in notices]


@app.get("/notices/{notice_id}")
def read_notice(notice_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM notices WHERE id = ?", (notice_id,))
    notice = cursor.fetchone()

    conn.close()

    if notice is None:
        raise HTTPException(status_code=404, detail="Notice not found")

    return dict(notice)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
