from typing import Any

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

import chunlian_generate

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class InputData(BaseModel):
    text: str


class OutPutData(BaseModel):
    code: int
    msg: str
    data: list = []


@app.post("/chunlian", response_model=OutPutData)
def chunlian(inputData: InputData) -> Any:
    # Read the image file and encode it as base64
    # with open(image_path, "rb") as image_file:
    #     encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
    custom_text = inputData.text
    print("输入的信息内容: ", custom_text)

    result = chunlian_generate.BuildChunlian(custom_text)

    out = OutPutData
    out.code = 200
    out.msg = "success"
    out.data = [result]

    return out


@app.post("/items", response_model=OutPutData)
async def create_item(item: Item) -> Any:
    out = OutPutData
    out.code = 200
    out.msg = "success"
    out.data = item
    return out


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8099)
