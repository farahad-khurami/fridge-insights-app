import base64
import json

from openai import OpenAI, BadRequestError
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

from config import API_KEY, SYSTEM_PROMPT, USER_PROMPT, MODEL

app = FastAPI()


client = OpenAI(api_key=API_KEY)


@app.post("/detect-food")
async def detect_food(image: UploadFile = File(...)):

    img_bytes = await image.read()
    img_b64 = base64.b64encode(img_bytes).decode("utf-8")

    msg = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": USER_PROMPT},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"},
                },
            ],
        },
    ]

    try:
        res = client.chat.completions.create(
            model=MODEL,
            messages=msg,
            response_format={"type": "json_object"},
        )
        res_obj = json.loads(res.choices[0].message.content)
        return JSONResponse(content=res_obj)
    except BadRequestError as err:
        err_str = str(err)
        if "unsupported image" in err_str or "invalid_image_format" in err_str:
            msg = (
                f"The file you uploaded is not supported. "
                f"Supported image file formats are: png, jpeg, gif, webp. "
                f"Your file type: {image.content_type}"
            )
            return JSONResponse(content={"error": msg}, status_code=400)
        return JSONResponse(content={"error": err_str}, status_code=400)
