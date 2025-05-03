# Physics MCQ Generator & Review Pipeline

This repository contains solutions for the Python + AI + API Integration - Candidate Evaluation Test. The project automates the generation, validation, review, and publishing of multiple-choice questions (MCQs) on the topic "Laws of Motion - Grade 9" using GPT-4/Gemini APIs and Python.

---

## Setup Instructions

### 1. Clone the Repository

git clone <your-repo-url>
cd <your-repo-directory>


### 2. Set Up a Virtual Environment

python3 -m venv .venv

source .venv/bin/activate 

#### On Windows: 

.venv\Scripts\activate


### 3. Install Dependencies

pip install -r requirements.txt


---

## Project Structure and How to Run

### Questions 1 & 2: MCQ Generation and Error Detection

- Both Question 1 and Question 2 are implemented in the Jupyter notebook `questions.ipynb`.
    - Question 1: Generates and validates 10 MCQs, saves them to `questions.json`.
    - Question 2: Checks for duplicate options, answer mismatches, and grammar errors.
- To run:
    ```
    jupyter notebook questions.ipynb
    ```

### Question 3: Automated Review & Rewriting API

- Implemented in `main.py` using FastAPI.
- The `/review` endpoint accepts a batch of MCQs, reviews each, rewrites faulty ones, and marks them with `revised=True`.
- To run the FastAPI server:
    ```
    uvicorn main:app --reload --port 8000
    ```
- Interactive documentation is available at [http://localhost:8000/docs](http://localhost:8000/docs).

### Question 4: Publishing Pipeline

- Implemented in `publisher.py`.
- Reads reviewed questions from `reviewed_questions.json`, publishes each to a simulated content API (e.g., httpbin.org), logs the response, and supports retries.
- To run:
    ```
    python publisher.py
    ```

### Question 5: Code Debugging and Unit Testing

- The corrected OpenAI API call is in `module.py`.
- Unit tests for this function are in `tests.py`.
- To run the tests:
    ```
    pytest -s tests.py
    ```

---

## Notes

- Store your OpenAI/Gemini API keys securely, preferably as environment variables.
- For Question 4, a simulated API endpoint such as `https://httpbin.org/post` is used.
- All required dependencies are listed in `requirements.txt`.

---



