import json
import os
import sys
from colorama import Fore, Style, init

# 初始化顏色設定
init(autoreset=True)

# 設定知識庫路徑
KB_FILE = os.path.join("data", "knowledge_base.json")

# =========================================
#  UI 顯示功能 (保留原有的)
# =========================================

def print_system(text):
    print(f"{Fore.CYAN}[System]: {text}{Style.RESET_ALL}")

def print_agent(text):
    print(f"{Fore.GREEN}[Agent]: {text}{Style.RESET_ALL}")

def print_user(text, is_demo=False):
    if is_demo:
        print(f"{Fore.YELLOW}[User (Demo)]: {text}{Style.RESET_ALL}")
    else:
        # 手動輸入時不重複印出，這裡僅供 Demo 模式使用
        pass

# =========================================
#  資料庫與檔案功能
# =========================================

def load_database(filepath="data/mock_database.json"):
    """讀取 JSON 資料庫，包含錯誤處理 (保留原有的)"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            print_system(f"Successfully loaded {len(data)} candidates.")
            return data
    except FileNotFoundError:
        print(f"{Fore.RED}[Error]: Database file not found at {filepath}")
        print(f"Please generate mock data first.{Style.RESET_ALL}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"{Fore.RED}[Error]: JSON format error in database.{Style.RESET_ALL}")
        sys.exit(1)

# =========================================
#  AI 知識庫學習功能 (新增的)
# =========================================

def load_knowledge_base():
    """讀取整個知識庫，如果不存在則建立預設值"""
    # 預設值：包含 mock_database.json 裡已經有的詞，確保一開始就能配對
    defaults = {
        "values": [
            "Innovation", "Impact", "Efficiency", "Truth", "Autonomy", 
            "Competence", "Empathy", "Justice", "Connection", "Security", 
            "Discipline", "Responsibility", "Creativity", "Freedom", 
            "Authenticity", "Compassion", "Vulnerability", "Growth"
        ],
        "talents": [
            "Persuasive Communication", "Aesthetic Sensitivity", "System Optimization",
            "Deep Focus", "Logical Debugging", "Technical Mastery",
            "Conflict Resolution", "Active Listening", "Community Building",
            "Risk Assessment", "Financial Planning", "Data Organization",
            "Visual Storytelling", "Imaginative Thinking", "Breaking Convention",
            "Deep Empathy", "Creating Safety", "Insight"
        ],
        "dreams": [
            "Social Entrepreneurship", "Venture Capital", "Open Source", "Cybersecurity",
            "Social Work", "Public Policy", "Wealth Management", "Economic Analysis",
            "Animation", "Illustration", "Therapy", "Mental Health Advocacy",
            "Social Impact", "Technology", "Art & Design", "Finance", "Education"
        ]
    }
    
    if os.path.exists(KB_FILE):
        try:
            with open(KB_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # 簡單檢查結構是否完整，若缺漏則補上
                for key in defaults:
                    if key not in data:
                        data[key] = defaults[key]
                return data
        except Exception:
            print_system(f"{Fore.RED}Error loading KB, using defaults.{Style.RESET_ALL}")
            return defaults
    else:
        # 建立新檔案
        save_knowledge_base(defaults, is_init=True)
        return defaults

def save_knowledge_base(data, is_init=False):
    """寫入知識庫"""
    # 確保 data 資料夾存在
    os.makedirs(os.path.dirname(KB_FILE), exist_ok=True)
    
    with open(KB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def learn_new_concept(category, new_items, is_init=False):
    """
    動態學習新概念
    category: 'values', 'talents', or 'dreams'
    new_items: list of strings (e.g., ['Culinary Arts'])
    """
    kb = load_knowledge_base()
    
    # 確保該分類存在
    if category not in kb:
        kb[category] = []
    
    current_list = kb[category]
    learned_something = False

    for item in new_items:
        # 轉成 Title Case 統一格式 (e.g., "coding" -> "Coding")
        clean_item = item.strip().title()
        # 簡單去重檢查
        if clean_item not in current_list:
            current_list.append(clean_item)
            if not is_init: # 初始化時不印
                print(f"{Fore.YELLOW}[Learning]: System learned a new {category[:-1]}: '{clean_item}'{Style.RESET_ALL}")
            learned_something = True
    
    if learned_something:
        save_knowledge_base(kb)