import torch
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from peft import PeftModel

try:
    from rag_engine import RecipeRAG
except ImportError:
    try:
        from .rag_engine import RecipeRAG
    except ImportError:
        RecipeRAG = None

app = FastAPI(title="Cooking AI Chef API")

# Allow CORS for local Vite development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

# Context variables loaded on startup
rag = None
pipe = None
model_loaded_successfully = False

@app.on_event("startup")
def startup_event():
    global rag, pipe, model_loaded_successfully

    print("🔥 Warming up the Kitchen... Initializing AI Chef API.")

    # 1. RAG
    if RecipeRAG:
        try:
            rag = RecipeRAG()
            print("✅ RAG Engine Loaded")
        except Exception as e:
            print(f"❌ RAG Engine failed: {e}")
    else:
        print("⚠️ rag_engine.py not found — running without RAG")

    # 2. DEVICE Setup
    if torch.cuda.is_available():
        device = "cuda"
        dtype = torch.float16
        print(f"⚡ Using GPU: {torch.cuda.get_device_name(0)}")
    else:
        device = "cpu"
        dtype = torch.float32
        print("🐢 Using CPU (slow mode)")

    # 3. Model Setup
    model_dir = "models/cooking-slm"
    base_model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

    print("📦 Loading model...")
    if os.path.exists(model_dir):
        try:
            tokenizer = AutoTokenizer.from_pretrained(model_dir)
            base_model = AutoModelForCausalLM.from_pretrained(
                base_model_id,
                torch_dtype=dtype,
                device_map="auto"
            )
            model = PeftModel.from_pretrained(base_model, model_dir)
            model.eval()

            pipe = pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer
            )
            model_loaded_successfully = True
            print("✅ Model loaded successfully!")
        except Exception as e:
            print(f"❌ Model loading failed: {e}")
    else:
        print("\n❌ ERROR: Model directory not found!")
        print("➡️ Run: python src/train.py\n")

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if not model_loaded_successfully:
        raise HTTPException(status_code=503, detail="Model not loaded. Please train or check model path.")

    if rag is None:
        raise HTTPException(status_code=503, detail="RAG system unavailable.")

    user_message = request.message

    try:
        recipe_info = rag.search(user_message, threshold=1.2)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG Error: {e}")

    if recipe_info:
        name = recipe_info.get("name", "Recipe")
        ingreds = "\n".join(f"- {str(i).strip()}" for i in recipe_info.get("ingredients", []))
        steps = "\n\n".join(f"Step {idx+1}. {str(s).capitalize()}" for idx, s in enumerate(recipe_info.get("steps", [])))

        prompt = f"<s>[INST]\nUser asked: {user_message}\n\nRecipe: {name}\n\nIngredients:\n{ingreds}\n\nInstructions:\n{steps}\n\nRespond nicely using this exact info.\n[/INST]"

        try:
            output = pipe(
                prompt,
                max_new_tokens=512,
                do_sample=True,
                temperature=0.3
            )[0]["generated_text"]

            response = output.split("[/INST]")[-1].strip()

            # Fallback
            if "Step 1." not in response or "-" not in response:
                response = f"🍽️ Here is the recipe for {name}:\n\n**Ingredients**\n{ingreds}\n\n**Instructions**\n{steps}\n\nHappy cooking! 👨‍🍳"

            return ChatResponse(response=response)

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Generation error: {e}")

    return ChatResponse(response="🤖 I specialize in cooking recipes. Try asking about a dish!")
