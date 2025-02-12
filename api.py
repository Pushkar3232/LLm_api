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

    # Call the user_input function and collect its entire output.
    # Here we assume that user_input(question) returns an iterable of JSON strings.
    responses = []
    for part in user_input(question):
        # Decode if needed
        if isinstance(part, bytes):
            part = part.decode("utf-8")
        try:
            # Parse each JSON string and extract the 'response' field.
            data = json.loads(part)
            responses.append(data.get("response", ""))
        except Exception as e:
            print(f"Error processing part: {e}")
            continue

    # Combine all parts into one final response.
    complete_response = "".join(responses)
    return PlainTextResponse(complete_response)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port, reload=True)
