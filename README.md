# Cooking GPT - RAG + SLM Fine-Tuning Project

This project builds a custom Small Language Model (SLM) based on TinyLlama, fine-tuned specifically for the cooking domain. It utilizes a Retrieval-Augmented Generation (RAG) architecture via `sentence-transformers` and `faiss` so that the model only relies on recipes strictly present in the dataset and responds with "I don't know" otherwise.

## System Requirements
- OS: Windows
- RAM: 16GB
- GPU: NVIDIA RTX 4050 (or any CUDA compatible GPU)
- Python 3.10

## Project Setup

### 1. Place the Dataset Data
Make sure you have downloaded the datasets. Specifically, move `RAW_recipes.csv` and `RAW_interactions.csv` into the `data/` folder.
*If the `data` directory does not exist, create it inside the project root before placing the datasets.*

### 2. Install Dependencies
Run the following command to download necessary libraries like `torch` with CUDA support:
```bash
pip install -r requirements.txt
```

### 3. Prepare the Dataset
After downloading the data into `data/`, run the dataset generation script:
```bash
python src/prepare_dataset.py
```
This filters the dataset for highly rated recipes, adds Indian recipes, generates prompt formats for training, and prepares `cooking_finetune.json`.

### 4. Fine-Tune the SLM Model
To initiate the LoRA fine-tuning for TinyLlama using PyTorch & TRL via the GPU, run:
```bash
python src/train.py
```

### 5. Launch the Chat App
Start the Gradio interactive chat:
```bash
python src/app.py
```
This will open a friendly web UI. The RAG engine will fetch the most related recipes to answer queries accurately!
