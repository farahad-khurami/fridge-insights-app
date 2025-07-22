import base64
import uvicorn

import openai
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

from config import API_KEY, SYSTEM_PROMPT, USER_PROMPT

app = FastAPI()


client = openai.OpenAI(api_key=API_KEY)


@app.post("/detect-food")
async def detect_food(image: UploadFile = File(...)):

    image_bytes = await image.read()
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")
    
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
                        "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"},
                    },
                ],
            },
        ],
    )
    food_items = response.choices[0].message.content
    return JSONResponse(content={"food_items": food_items})


if __name__ == "__main__":

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
