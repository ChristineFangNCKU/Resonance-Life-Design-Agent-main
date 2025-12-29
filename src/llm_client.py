import requests
import json
from .utils import print_system

# [Requirement: LLM API Usage]
API_URL = "https://api-gateway.netdb.csie.ncku.edu.tw/api/generate"  
API_KEY = "b69eae46e4864a455b3f6e17e5b894ac7a15fa9d344b028bba2f5635c99d16d7"           
MODEL_NAME = "gemma3:4b"                            # 指定的模型

class LLMClient:
    def analyze_user(self, context_history):
        """
        將對話紀錄傳送給 LLM，並要求回傳 JSON 格式的人格分析。
        """
        context_str = "\n".join(context_history)
        
        # System Prompt: 定義 LLM 的角色與輸出格式
        system_prompt = """
        You are a sharp psychological analyst for a Life Design system.
        Analyze the user's interview answers provided below to find their true underlying drivers.
        
        Task:
        1. Extract 3 core values. 
           IMPORTANT: Be specific to the user's text. Avoid generic corporate buzzwords like "Innovation" unless explicitly stated.
           Look for deeper values like "Competence", "Privacy", "Autonomy", "Authenticity", "Craftsmanship".
           **CRITICAL: Even if the user answers in Chinese, you MUST translate the extracted values into ENGLISH.**
        
        2. Identify 2-3 top talents. Focus on what they do effortlessly or what frustrates them about others.
        **CRITICAL: Even if the user answers in Chinese, you MUST translate the extracted values into ENGLISH.**
        
        3. Identify 1-2 dream domains they want to work in.
        **CRITICAL: Even if the user answers in Chinese, you MUST translate the extracted values into ENGLISH.**
        
        4. Summarize their personality in one sentence.

        Format:
        Output ONLY a valid JSON object. Do not include markdown formatting.
        {
            "core_values": ["Value1", "Value2", "Value3"],
            "top_talents": ["Talent1", "Talent2"],
            "dream_domain": ["Domain1", "Domain2"],
            "analysis_summary": "Short summary here."
        }
        """

        payload = {
            "model": MODEL_NAME,
            "prompt": f"{system_prompt}\n\n[User Interview Data]:\n{context_str}",
            "stream": False
        }
        
        headers = {"Authorization": f"Bearer {API_KEY}"} if "localhost" not in API_URL else {}

        try:
            print_system("Sending data to LLM API...")
            response = requests.post(API_URL, json=payload, headers=headers, timeout=120)
            response.raise_for_status()
            
            # 解析回應
            result_text = response.json().get('response', '')
            # 清理可能存在的 Markdown 符號
            clean_json = result_text.replace("```json", "").replace("```", "").strip()
            
            profile = json.loads(clean_json)
            return profile

        except Exception as e:
            print_system(f"LLM API Error: {e}")
            print_system("Using fallback profile for demo continuity.")
            # Fallback (保底機制，避免 Demo 當掉)
            return {
                "core_values": ["Innovation", "Resilience", "Impact"],
                "top_talents": ["Strategic Thinking", "Design"],
                "dream_domain": ["Social Enterprise"],
                "analysis_summary": "(Fallback) An ambitious change-maker."
            }