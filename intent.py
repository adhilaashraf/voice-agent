import groq
import json
from config import GROQ_API_KEY, LLM_MODEL

client = groq.Groq(api_key=GROQ_API_KEY)

def detect_intent(transcribed_text):
    try:
        system_prompt = """
        You are an intent classifier. Analyze the user's text and return ONLY a valid JSON object.
        
        Rules:
        - Return ONLY JSON, no explanation, no markdown, no code blocks
        - Choose intent from: "create_file", "write_code", "summarize", "chat"
        - Extract filename, language, and content from the text
        
        Example output:
        {"intent": "write_code", "details": {"filename": "add.py", "language": "python", "content": "add two numbers"}}
        """

        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": transcribed_text}
            ],
            temperature=0.1
        )

        response_text = response.choices[0].message.content.strip()

        # Remove markdown if LLM added it
        response_text = response_text.replace("```json", "").replace("```", "").strip()

        # Find JSON object in response
        start = response_text.find("{")
        end = response_text.rfind("}") + 1
        if start != -1 and end != 0:
            response_text = response_text[start:end]

        intent_data = json.loads(response_text)
        return intent_data

    except json.JSONDecodeError:
        return {
            "intent": "chat",
            "details": {"content": transcribed_text}
        }

    except Exception as e:
        return {
            "intent": "chat",
            "details": {"content": transcribed_text}
        }


def get_intent_label(intent):
    labels = {
        "create_file": "📁 Create File",
        "write_code": "💻 Write Code",
        "summarize": "📝 Summarize Text",
        "chat": "💬 General Chat",
        "error": "❌ Error"
    }
    return labels.get(intent, "❓ Unknown")