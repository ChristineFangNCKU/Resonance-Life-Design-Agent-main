import requests
import json
import re  # [必要的修正] 加入正規表達式模組
from .utils import print_system, load_knowledge_base, learn_new_concept

# [Requirement: LLM API Usage]
API_URL = "https://api-gateway.netdb.csie.ncku.edu.tw/api/generate"  
API_KEY = "b69eae46e4864a455b3f6e17e5b894ac7a15fa9d344b028bba2f5635c99d16d7"           
MODEL_NAME = "gemma3:4b" 

class LLMClient:
    def analyze_user(self, context_history):
        # 1. [Dynamic Knowledge] 讀取目前的知識庫
        kb = load_knowledge_base()
        values_str = ", ".join(kb['values'])
        talents_str = ", ".join(kb['talents'])
        dreams_str = ", ".join(kb['dreams'])
        
        context_str = "\n".join(context_history)
        
        # 2. [Prompt Engineering] 
        # 使用你指定的最優化 Prompt (Constraint Generation)
        system_prompt = f"""
        You are a sharp psychological analyst. Analyze the user's answers.
        
        **ADAPTIVE KNOWLEDGE BASE:**
        The system currently understands these concepts. PREFER mapping to these if they fit well.
        - Known Values: [{values_str}]
        - Known Talents: [{talents_str}]
        - Known Dream Domains: [{dreams_str}]

        **INSTRUCTIONS:**
        1. Extract 3 Core Values (English). 
           - Map to "Known Values" if close. If user expresses a NEW value, generate a concise English term for it.
        
        2. Identify 2-3 Top Talents (English).
           - Map to "Known Talents" if close. If NEW, generate a concise English term.

        3. Identify 1-2 Dream Domains (English).
           - Map to "Known Dream Domains" if close. If NEW, generate a concise English term.
        
        4. Summarize personality (English).

        **CRITICAL:** - Even if user speaks Chinese, OUTPUT ONLY ENGLISH JSON.
        - Output format must be strictly JSON.

        Format:
        {{
            "core_values": ["Value1", "Value2", "Value3"],
            "top_talents": ["Talent1", "Talent2"],
            "dream_domain": ["Domain1","Domain2"], 
            "analysis_summary": "..."
        }}
        """

        payload = {
            "model": MODEL_NAME,
            "prompt": f"{system_prompt}\n\n[User Interview Data]:\n{context_str}",
            "stream": False
        }
        
        headers = {"Authorization": f"Bearer {API_KEY}"}

        try:
            print_system("Sending data to LLM API...")
            response = requests.post(API_URL, json=payload, headers=headers, timeout=120)
            response.raise_for_status()
            
            result_text = response.json().get('response', '')
            
            # [FIX: 強力 JSON 清洗] 
            # 這裡不改變 Prompt，只改變「如何讀取結果」，解決 Invalid control character 問題
            match = re.search(r'\{.*\}', result_text, re.DOTALL)
            if match:
                clean_json = match.group(0)
            else:
                clean_json = result_text

            # 使用 strict=False 容忍換行符號等控制字元
            profile = json.loads(clean_json, strict=False)
            
            # 3. [Self-Learning Loop] 學習新概念
            learn_new_concept('values', profile.get('core_values', []))
            learn_new_concept('talents', profile.get('top_talents', []))
            learn_new_concept('dreams', profile.get('dream_domain', []))
            
            return profile

        except Exception as e:
            print_system(f"LLM API Error: {e}")
            print_system("Using fallback profile for demo continuity.")
            return {
                "core_values": ["Innovation", "Resilience", "Impact"],
                "top_talents": ["Strategic Thinking", "Design"],
                "dream_domain": ["Social Entrepreneurship"],
                "analysis_summary": "(Fallback) An ambitious change-maker."
            }