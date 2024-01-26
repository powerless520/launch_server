from typing import Any

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from SegmentDataQwenChunLianGenerateV5 import pipeline
from file_cloud_def import OssClient
app = FastAPI()
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
        out = OutPutData(
            code=200,
            msg="success",
            data=result
        )
        oss.upload_to_oss(result)
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