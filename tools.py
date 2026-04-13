import os
import groq
from config import GROQ_API_KEY, LLM_MODEL, OUTPUT_FOLDER

# Initialize Groq client
client = groq.Groq(api_key=GROQ_API_KEY)

# Make sure output folder exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def execute_tool(intent_data, original_text):
    """
    Takes intent data and executes the appropriate tool.
    Returns a result dictionary with action taken and output.
    """
    intent = intent_data.get("intent", "chat")
    details = intent_data.get("details", {})

    if intent == "create_file":
        return create_file_tool(details)

    elif intent == "write_code":
        return write_code_tool(details, original_text)

    elif intent == "summarize":
        return summarize_tool(details, original_text)

    elif intent == "chat":
        return chat_tool(original_text)

    else:
        return {
            "action": "Unknown intent",
            "output": "Sorry, I could not understand what you wanted to do.",
            "success": False
        }


def create_file_tool(details):
    """
    Creates a new empty file or folder inside output/ folder.
    """
    try:
        filename = details.get("filename", "new_file.txt")

        # Safety: always save inside output/ folder
        safe_path = os.path.join(OUTPUT_FOLDER, filename)

        # Check if it's a folder request
        if "." not in filename:
            os.makedirs(safe_path, exist_ok=True)
            return {
                "action": f"Created folder: output/{filename}",
                "output": f"✅ Folder '{filename}' created successfully inside output/",
                "success": True
            }
        else:
            # Create the file
            with open(safe_path, "w") as f:
                f.write("")

            return {
                "action": f"Created file: output/{filename}",
                "output": f"✅ File '{filename}' created successfully inside output/",
                "success": True
            }

    except Exception as e:
        return {
            "action": "Create file failed",
            "output": f"❌ Error creating file: {str(e)}",
            "success": False
        }


def write_code_tool(details, original_text):
    """
    Generates code using Groq LLM and saves it to a file.
    """
    try:
        filename = details.get("filename", "generated_code.py")
        language = details.get("language", "python")
        content = details.get("content", original_text)

        # Ask Groq LLM to generate the code
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": f"You are a code generator. Generate clean, working {language} code only. No explanations, no markdown, just the raw code."
                },
                {
                    "role": "user",
                    "content": f"Write {language} code for: {content}"
                }
            ],
            temperature=0.3
        )

        # Get generated code
        generated_code = response.choices[0].message.content.strip()

        # Remove markdown code blocks if LLM added them
        generated_code = generated_code.replace("```python", "").replace("```", "").strip()

        # Safety: always save inside output/ folder
        safe_path = os.path.join(OUTPUT_FOLDER, filename)

        # Save to file
        with open(safe_path, "w") as f:
            f.write(generated_code)

        return {
            "action": f"Generated and saved code to: output/{filename}",
            "output": generated_code,
            "success": True
        }

    except Exception as e:
        return {
            "action": "Code generation failed",
            "output": f"❌ Error generating code: {str(e)}",
            "success": False
        }


def summarize_tool(details, original_text):
    """
    Summarizes the provided text using Groq LLM.
    """
    try:
        content = details.get("content", original_text)

        # Ask Groq LLM to summarize
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a text summarizer. Provide a clear and concise summary of the given text."
                },
                {
                    "role": "user",
                    "content": f"Summarize this: {content}"
                }
            ],
            temperature=0.3
        )

        summary = response.choices[0].message.content.strip()

        return {
            "action": "Summarized the provided text",
            "output": summary,
            "success": True
        }

    except Exception as e:
        return {
            "action": "Summarization failed",
            "output": f"❌ Error summarizing: {str(e)}",
            "success": False
        }


def chat_tool(original_text):
    """
    Handles general chat/questions using Groq LLM.
    """
    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant. Answer the user's questions clearly and concisely."
                },
                {
                    "role": "user",
                    "content": original_text
                }
            ],
            temperature=0.7
        )

        answer = response.choices[0].message.content.strip()

        return {
            "action": "Responded to general chat",
            "output": answer,
            "success": True
        }

    except Exception as e:
        return {
            "action": "Chat failed",
            "output": f"❌ Error in chat: {str(e)}",
            "success": False
        }