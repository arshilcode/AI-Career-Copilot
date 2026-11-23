from groq import Groq
import json
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
def get_active_model():
    """Active aur JSON-compatible text model dynamically fetch karta hai"""
    models = client.models.list().data
    excluded = ["whisper", "guard", "tts", "playai", "vision", "embed"]
    chat_models = [
        m.id for m in models 
        if not any(ex in m.id.lower() for ex in excluded)
    ]
    
    for preferred in ["llama-4", "70b", "32b", "versatile", "instant"]:
        for m_id in chat_models:
            if preferred in m_id.lower():
                return m_id
                
    return chat_models[0]

def analyze_resume(resume_text, user_goal):
    try:
        active_model = get_active_model()
        
        completion = client.chat.completions.create(
            model=active_model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that outputs only valid JSON. Do not include any conversational text or markdown formatting."
                },
                {
                    "role": "user",
                    "content": f"""
                    Analyze this resume for the role: "{user_goal}".
                    Resume content: {resume_text}
                    
                    You MUST return a JSON object with this exact structure:
                    {{
                        "skills": ["skill1", "skill2"],
                        "missing_skills": ["skillA", "skillB"],
                        "roadmap": ["step1", "step2"],
                        "interview_questions": ["question1", "question2"]
                    }}
                    """
                }
            ],
            response_format={"type": "json_object"}
        )

        content = completion.choices[0].message.content
        return json.loads(content)

    except Exception as e:
        return {"error": f"Groq Error: {str(e)}"}