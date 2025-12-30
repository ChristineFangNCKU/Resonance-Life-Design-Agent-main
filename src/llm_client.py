import requests
import json
import re
from .utils import print_system, load_knowledge_base, learn_new_concept

# [Requirement: LLM API Usage]
API_URL = "https://api-gateway.netdb.csie.ncku.edu.tw/api/generate"  
API_KEY = "b69eae46e4864a455b3f6e17e5b894ac7a15fa9d344b028bba2f5635c99d16d7"           
MODEL_NAME = "gemma3:4b" 

class LLMClient:
    def analyze_user(self, context_history):
        kb = load_knowledge_base()
        values_str = ", ".join(kb['values'])
        talents_str = ", ".join(kb['talents'])
        dreams_str = ", ".join(kb['dreams'])
        
        context_str = "\n".join(context_history)
        
        # [核心升級]：植入您定義的心理學分析框架
        system_prompt = f"""
        You are an expert Life Design Psychologist. Your job is not just to extract keywords, but to interpret the **underlying psychology** of the user's answers based on the following framework.

        **THEORETICAL FRAMEWORK (MUST FOLLOW):**

        **1. CORE VALUES (The "Internal Compass"):**
           - **Definition:** What the user believes is non-negotiable. Their standard for action. What they DO vs. what they DON'T DO.
           - **Logic:** If they admire someone, ask "Why?" -> That quality is their value.
        
        **2. TOP TALENTS (The "Innate Gift", NOT just Skills):**
           - **Definition:** Innate traits that require little effort (e.g., strong memory, high focus, aesthetic sense), NOT just learned skills (e.g., Python, Accounting).
           - **The "Impatience" Clue:** If the user gets impatient with others for being X, it means the user is naturally gifted at the opposite of X.
             - *Example:* "I hate slow people" -> Talent is "Efficiency/Speed".
             - *Example:* "I hate messy logic" -> Talent is "Logical Structure".
           - **Mapping:** You may infer suitable skills from these traits (e.g., Logic -> Coding), but prioritize the Trait first.

        **3. DREAM DOMAINS (The "Intrinsic Motivation"):**
           - **Definition:** What they would do even if unpaid. A deep passion or an ultimate goal.
           - **The "Anger" Nuance (CRITICAL):**
             - **Type A: Aversion (Hate/Avoidance):** "I hate discussing politics." -> User wants to AVOID this field. -> **EXCLUDE**.
             - **Type B: Constructive Anger (Drive to Change):** "I am angry about social injustice." -> User wants to CHANGE this. -> **INCLUDE** (e.g., Social Reform).
             - **Distinction:** Does the anger stem from "tiredness/disinterest" (Exclude) or "passion for improvement" (Include)?

        **KNOWLEDGE BASE (Reference):**
        - Known Values: [{values_str}]
        - Known Talents: [{talents_str}]
        - Known Dream Domains: [{dreams_str}]
        - (You may generate new terms if the user's concept is unique.)

        **MAPPING RULES (CRITICAL):**
        1. **PRIORITIZE EXISTING TERMS:** You MUST try to map the user's input to a "Known Concept" first.
           - *Bad:* User says "Calm" -> You output "Calm" (New Term).
           - *Good:* User says "Calm" -> You output "Balance" or "Simplicity" (Existing Term).
        2. **ONLY create a new term if NO existing term fits.** - If you create a new term, ensure it is a high-level psychological concept, not just a translation of the user's word.

        **OUTPUT FORMAT:**
        **CRITICAL:** - Even if user speaks Chinese, OUTPUT ONLY ENGLISH JSON.
        Return a single VALID JSON object with a "reasoning" field first.

        {{
            "reasoning": "Step-by-step psychological deduction. Explicitly explain how you distinguished 'Aversion' from 'Drive' in the Dream section.",
            "core_values": ["Value1", "Value2", "Value3"],
            "top_talents": ["Talent1", "Talent2"],
            "dream_domain": ["Domain1"], 
            "analysis_summary": "One sentence summary."
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
            
            # Regex Cleaning
            match = re.search(r'\{.*\}', result_text, re.DOTALL)
            if match:
                clean_json = match.group(0)
            else:
                clean_json = result_text

            profile = json.loads(clean_json, strict=False)
            
            if 'reasoning' in profile:
                print_system(f"LLM Psychology Analysis:\n{profile['reasoning']}")

            learn_new_concept('values', profile.get('core_values', []))
            learn_new_concept('talents', profile.get('top_talents', []))
            learn_new_concept('dreams', profile.get('dream_domain', []))
            
            return profile

        except Exception as e:
            print_system(f"LLM API Error: {e}")
            return {
                "core_values": ["Innovation", "Resilience", "Impact"],
                "top_talents": ["Strategic Thinking", "Design"],
                "dream_domain": ["Social Entrepreneurship"],
                "analysis_summary": "(Fallback) An ambitious change-maker."
            }