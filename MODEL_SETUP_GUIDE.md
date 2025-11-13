# Connecting Your Finetuned Model - Setup Guide

This guide shows you how to connect your finetuned model from Google Colab to this project by exposing it as an API endpoint.

## Steps:

1. **In your Colab notebook**, copy the code from `colab_api_setup.py` into a new cell.

2. **Install required packages in Colab:**
   ```python
   !pip install fastapi uvicorn pyngrok transformers torch
   ```

3. **Load your finetuned model** (adjust based on your model type):
   ```python
   from transformers import AutoModelForCausalLM, AutoTokenizer
   
   # If you saved to Google Drive:
   model = AutoModelForCausalLM.from_pretrained("/content/drive/MyDrive/your_model_path")
   tokenizer = AutoTokenizer.from_pretrained("/content/drive/MyDrive/your_model_path")
   
   # Or if using HuggingFace:
   # model = AutoModelForCausalLM.from_pretrained("your-username/your-model")
   # tokenizer = AutoTokenizer.from_pretrained("your-username/your-model")
   
   model.eval()
   ```

4. **Update the `/predict` endpoint** in the Colab code to use your actual model inference.

5. **Run the API server** in Colab - it will print a public URL (via ngrok).

6. **In your local project**, create a `.env` file in the project root:
   ```
   COLAB_ENDPOINT=https://your-ngrok-url.ngrok.io/predict
   ```

7. **Start your backend:**
   ```bash
   uv run uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
   ```

**Note:** The ngrok URL changes each time you restart Colab. You'll need to update your `.env` file each time.

---

## Troubleshooting

- **"COLAB_ENDPOINT not configured"**: Make sure your `.env` file has `COLAB_ENDPOINT` set
- **Connection errors**: Check that Colab notebook is still running and ngrok URL is correct
- **Timeout errors**: Increase timeout in `backend/main.py` (currently 60 seconds)

---

## Example .env File

Create a `.env` file in the project root:

```
COLAB_ENDPOINT=https://abc123.ngrok.io/predict
# Optional:
# COLAB_API_KEY=your_api_key_here
```

**Note:** Don't commit the `.env` file to git (it should be in `.gitignore`).

