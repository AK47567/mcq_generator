import requests




def fetch_questions(api_key):
    try:
        res = requests.post(
            "https://api.openai.com/v1/chat/completions",
            json={
                "model": "gpt-4",
                "messages": [{"role": "user", "content": "Give 5 MCQs on Laws of Motion for Grade 9"}],
                "max_tokens": 1000,
                "temperature": 0.7
            },
            headers={"Authorization": f"Bearer {api_key}"}
        )
        res.raise_for_status()
        data = res.json()
        # Defensive parsing
        choices = data.get('choices')
        if not choices or not isinstance(choices, list) or not choices[0].get('message', {}).get('content'):
            return None
        return choices[0]['message']['content']
    except requests.exceptions.RequestException as e:
        print(f"API request error: {e}")
        return None
    except (KeyError, ValueError, IndexError, TypeError) as e:
        print(f"Response parsing error: {e}")
        return None
