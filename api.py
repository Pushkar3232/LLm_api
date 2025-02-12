import os
import json
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from main import user_input  # Assuming user_input is defined in main.py

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust origins as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def hello_world():
    return PlainTextResponse("Hello from FastAPI")

@app.post("/api/data")
async def qa(request: Request):
    body = await request.json()
    question = body.get("prompt")
    print(question)
    print(f"Received question: {question}")

    # Call the user_input function and get its output directly.
    result = user_input(question)

    # Optionally, handle the case where result is None.
    if result is None:
        return PlainTextResponse("Sorry, something went wrong.", status_code=500)

    # If the result is a dict, extract the text under the key "output_text"
    if isinstance(result, dict):
        result_text = result.get("output_text", "")
    else:
        result_text = result

    return PlainTextResponse(result_text)



if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
