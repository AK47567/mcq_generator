import requests
import json
import time

API_URL = "https://httpbin.org/post"  # Simulated CMS API endpoint
AUTH_TOKEN = "Bearer MOCK_TOKEN"       # Simulated auth token
REVIEWED_QUESTIONS_FILE = "reviewed_questions.json"
LOG_FILE = "publish_log.txt"
MAX_RETRIES = 3

def load_questions(filename):
    with open(filename, "r") as f:
        data = json.load(f)
        return data.get("reviewed_mcqs", [])

def publish_question(question, session, retries=MAX_RETRIES):
    headers = {
        "Authorization": AUTH_TOKEN,
        "Content-Type": "application/json"
    }
    for attempt in range(1, retries + 1):
        try:
            response = session.post(API_URL, headers=headers, json=question, timeout=10)
            if response.status_code == 200:
                return True, response.json()
            else:
                print(f"Attempt {attempt}: Failed with status {response.status_code}")
        except Exception as e:
            print(f"Attempt {attempt}: Exception occurred: {e}")
        time.sleep(1)
    return False, None

def main():
    questions = load_questions(REVIEWED_QUESTIONS_FILE)
    session = requests.Session()
    log_entries = []
    for idx, question in enumerate(questions, 1):
        success, resp = publish_question(question, session)
        log_entry = {
            "question_index": idx,
            "question": question.get("question"),
            "status": "success" if success else "failure",
            "response": resp
        }
        log_entries.append(log_entry)
        print(f"Question {idx}: {'Success' if success else 'Failure'}")
    # Write log file
    with open(LOG_FILE, "w") as f:
        for entry in log_entries:
            f.write(json.dumps(entry) + "\n")
    print(f"Publishing complete. Log saved to {LOG_FILE}")

if __name__ == "__main__":
    main()
