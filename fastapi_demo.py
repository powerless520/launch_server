from typing import Any

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from SegmentDataQwenChunLianGenerateV6 import pipeline
from file_cloud_def import OssClient
app = FastAPI()
# 静态资源访问
app.mount("/result", StaticFiles(directory="./result"), name="result")

oss = OssClient()


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
    data: str


@app.post("/chunlian", response_model=OutPutData)
def chunlian(inputData: InputData) -> Any:
    custom_text = inputData.text
    flag, result = pipeline(custom_text)

    if flag:
        returnUrl = oss.upload_to_oss(result)
        # returnUrlPrefix = 'http://127.0.0.1:8177/result/'

        out = OutPutData(
            code=200,
            msg="success",
            data=returnUrl
        )
    else:
        out = OutPutData(
            msg="failure"
        )

    return out


@app.post("/items", response_model=OutPutData)
async def create_item(item: Item) -> OutPutData:
    out = OutPutData(
        code=200,
        msg="success",
        data=item
    )
    return out


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8177)