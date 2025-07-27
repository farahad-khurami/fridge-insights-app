import base64
import json

from openai import OpenAI, BadRequestError
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

from config import API_KEY, SYSTEM_PROMPT, USER_PROMPT, MODEL
from models import FoodAnalysisResult

app = FastAPI()


client = OpenAI(api_key=API_KEY)


@app.post("/detect-food")
async def detect_food(image: UploadFile = File(...)):

    img_bytes = await image.read()
    img_b64 = base64.b64encode(img_bytes).decode("utf-8")

    try:
        res = client.responses.parse(
            model=MODEL,
            input=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": USER_PROMPT},
                        {
                            "type": "input_image",
                            "image_url": f"data:image/jpeg;base64,{img_b64}",
                        },
                    ],
                },
            ],
            text_format=FoodAnalysisResult,
        )

        result = res.output_parsed
        return JSONResponse(content=result.model_dump())
    except BadRequestError as err:
        err_dict = json.loads(err.response.text)
        msg = err_dict.get("error", {}).get("message", str(err))
        return JSONResponse(content={"error": msg}, status_code=400)
