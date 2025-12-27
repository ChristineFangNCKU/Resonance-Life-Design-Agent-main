import json
import os
import sys
from colorama import Fore, Style, init

# 初始化顏色設定
init(autoreset=True)

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

def load_database(filepath="data/mock_database.json"):
    """讀取 JSON 資料庫，包含錯誤處理"""
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