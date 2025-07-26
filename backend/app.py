import base64
import uvicorn

from openai import OpenAI, BadRequestError
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

from config import API_KEY, SYSTEM_PROMPT, USER_PROMPT

app = FastAPI()


client = OpenAI(api_key=API_KEY)


@app.post("/detect-food")
async def detect_food(image: UploadFile = File(...)):

    image_bytes = await image.read()
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    try:
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": USER_PROMPT,
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            },
                        },
                    ],
                },
            ],
        )
        food_items = response.choices[0].message.content
        return JSONResponse(content={"food_items": food_items})
    except BadRequestError as e:
        e = str(e)
        if "unsupported image" in e or "invalid_image_format" in e:
            msg = (
                f"The file you uploaded is not supported. "
                f"Supported image file formats are: png, jpeg, gif, webp. "
                f"Your file type: {image.content_type}"
            )
            return JSONResponse(content={"error": msg}, status_code=400)
        return JSONResponse(content={"error": e}, status_code=400)
