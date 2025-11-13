"""
Google Colab API Setup Template
================================
Copy this code into a new cell in your Colab notebook to expose your finetuned model as an API.

Prerequisites in Colab:
1. Install dependencies:
   !pip install fastapi uvicorn pyngrok transformers torch

2. Load your finetuned model (adjust based on your model type):
   from transformers import AutoModelForCausalLM, AutoTokenizer
   model = AutoModelForCausalLM.from_pretrained("path/to/your/model")
   tokenizer = AutoTokenizer.from_pretrained("path/to/your/model")
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from pyngrok import ngrok

# Initialize FastAPI app
app = FastAPI(title="Colab Model API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load your model here (adjust based on your setup)
# Example for HuggingFace transformers:
# from transformers import AutoModelForCausalLM, AutoTokenizer
# model = AutoModelForCausalLM.from_pretrained("path/to/your/finetuned/model")
# tokenizer = AutoTokenizer.from_pretrained("path/to/your/finetuned/model")
# model.eval()

class SolveRequest(BaseModel):
    problem: str
    system_prompt: str = None
    temperature: float = 0.2
    max_tokens: int = 512

class SolveResponse(BaseModel):
    output: str

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/predict", response_model=SolveResponse)
async def predict(request: SolveRequest):
    """
    Generate solution for competitive programming problem.
    Adjust this function based on your model's inference method.
    """
    # Example inference (adjust based on your model):
    # prompt = request.system_prompt + "\n\n" + request.problem if request.system_prompt else request.problem
    # inputs = tokenizer(prompt, return_tensors="pt")
    # outputs = model.generate(
    #     inputs.input_ids,
    #     max_length=len(inputs.input_ids[0]) + request.max_tokens,
    #     temperature=request.temperature,
    #     do_sample=True,
    # )
    # output_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # For now, return a placeholder - replace with your actual model inference
    output_text = f"[Model inference placeholder] Problem: {request.problem[:50]}..."
    
    return SolveResponse(output=output_text)

# Run the server
if __name__ == "__main__":
    # Expose via ngrok (free tier)
    public_url = ngrok.connect(8000)
    print(f"Public URL: {public_url}")
    print(f"Use this URL in your .env file: {public_url}/predict")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)

