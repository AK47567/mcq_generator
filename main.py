import google.generativeai as genai
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import language_tool_python
import os
import json
import time

# Configure Gemini API key
genai.configure(api_key="AIzaSyCHIww64bVyX04blLPRFjH2ILp40-L3kv4")  # <-- Replace with your key

MODEL_NAME = "models/gemini-2.5-pro-exp-03-25"  # Use a supported model

tool = language_tool_python.LanguageTool('en-US')
app = FastAPI()

# --- MCQ Validation Functions ---
def check_duplicate_options(options):
    seen = set()
    duplicates = set()
    for opt in options:
        if opt in seen:
            duplicates.add(opt)
        else:
            seen.add(opt)
    return list(duplicates)

def check_answer_mismatch(options, answer):
    return answer not in options

def check_grammar(text):
    matches = tool.check(text)
    return len(matches) > 0

def is_faulty(mcq):
    if check_duplicate_options(mcq["options"]):
        return True
    if check_answer_mismatch(mcq["options"], mcq["answer"]):
        return True
    if check_grammar(mcq["question"]):
        return True
    return False

# --- Pydantic Models ---
class MCQ(BaseModel):
    question: str
    options: List[str]
    answer: str

class MCQBatch(BaseModel):
    mcqs: List[MCQ]

# --- Gemini Correction Function ---
def correct_mcq_with_gemini(mcq):
    prompt = (
        "Review and improve the following multiple-choice question for clarity, grammar, and correctness. "
        "Ensure there are exactly 4 unique options, the answer is present in the options, and the question is grammatically correct. "
        "Return ONLY a JSON object in this format: "
        '{"question": "...", "options": ["...","...","...","..."], "answer": "..."}\n\n'
        f"MCQ:\n"
        f"Question: {mcq['question']}\n"
        f"Options: {mcq['options']}\n"
        f"Answer: {mcq['answer']}\n"
    )
    model = genai.GenerativeModel(MODEL_NAME)
    try:
        response = model.generate_content(prompt)
        text = response.text
        start = text.find('{')
        end = text.rfind('}') + 1
        json_str = text[start:end]
        fixed_mcq = json.loads(json_str)
        return fixed_mcq
    except Exception as e:
        print(f"Gemini correction error: {e}")
        return mcq


# --- FastAPI Endpoint ---
@app.post("/review")
async def review_mcqs(batch: MCQBatch):
    reviewed = []
    for mcq in batch.mcqs:
        mcq_dict = mcq.model_dump()
        if is_faulty(mcq_dict):
            improved = correct_mcq_with_gemini(mcq_dict)
            improved["revised"] = True
            reviewed.append(improved)
        else:
            mcq_dict["revised"] = False
            reviewed.append(mcq_dict)

    # Save reviewed MCQs to JSON file
    with open("reviewed_questions.json", "w") as f:
        json.dump({"reviewed_mcqs": reviewed}, f, indent=2)

    return {"reviewed_mcqs": reviewed}
