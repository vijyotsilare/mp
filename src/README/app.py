import gradio as gr
import torch
import os

from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from peft import PeftModel

# Try importing RAG safely
try:
    from rag_engine import RecipeRAG
except ImportError:
    RecipeRAG = None

print("🔥 Warming up the Kitchen... Initializing AI Chef Components.")

model_dir = "models/cooking-slm"
base_model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

# =========================
# Step 1: Initialize RAG
# =========================
rag = None
if RecipeRAG:
    try:
        rag = RecipeRAG()
        print("✅ RAG Engine Loaded")
    except Exception as e:
        print(f"❌ RAG Engine failed: {e}")
else:
    print("⚠️ rag_engine.py not found — running without RAG")

# =========================
# Step 2: Device Setup
# =========================
if torch.cuda.is_available():
    device = "cuda"
    dtype = torch.float16
    print(f"⚡ Using GPU: {torch.cuda.get_device_name(0)}")
else:
    device = "cpu"
    dtype = torch.float32
    print("🐢 Using CPU (slow mode)")

# =========================
# Step 3: Load Model
# =========================
pipe = None
model_loaded_successfully = False

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

# =========================
# Step 4: Chat Function
# =========================
def generate_response(user_message, history):
    if not model_loaded_successfully:
        return "⚠️ Model not loaded. Please train or check model path."

    if rag is None:
        return "⚠️ RAG system unavailable."

    try:
        recipe_info = rag.search(user_message, threshold=1.2)
    except Exception as e:
        return f"RAG Error: {e}"

    if recipe_info:
        name = recipe_info.get("name", "Recipe")

        ingreds = "\n".join(
            f"- {str(i).strip()}" for i in recipe_info.get("ingredients", [])
        )

        steps = "\n\n".join(
            f"Step {idx+1}. {str(s).capitalize()}"
            for idx, s in enumerate(recipe_info.get("steps", []))
        )

        prompt = f"""<s>[INST]
User asked: {user_message}

Recipe: {name}

Ingredients:
{ingreds}

Instructions:
{steps}

Respond nicely using this exact info.
[/INST]"""

        try:
            output = pipe(
                prompt,
                max_new_tokens=512,
                do_sample=True,
                temperature=0.3
            )[0]["generated_text"]

            response = output.split("[/INST]")[-1].strip()

            # fallback safety
            if "Step 1." not in response or "-" not in response:
                response = f"""🍽️ Here is the recipe for {name}:

**Ingredients**
{ingreds}

**Instructions**
{steps}

Happy cooking! 👨‍🍳"""

            return response

        except Exception as e:
            return f"❌ Generation error: {e}"

    return "🤖 I specialize in cooking recipes. Try asking about a dish!"

# =========================
# Step 5: UI Setup
# =========================
examples_list = [
    "How do I make roti?",
    "How do I make biryani?",
    "Butter chicken ingredients?",
    "Steps for dal tadka?",
    "How to make samosa?",
    "Pasta carbonara recipe?"
]

demo = gr.ChatInterface(
    fn=generate_response,
    title="🍳 Cooking AI Chef",
    description="Ask me anything about cooking!",
    examples=examples_list,
    theme=gr.themes.Soft()
)

# =========================
# Step 6: Launch
# =========================
if __name__ == "__main__":
    print("🚀 Launching AI Chef...")
    demo.launch(server_name="127.0.0.1", server_port=7860, share=False)