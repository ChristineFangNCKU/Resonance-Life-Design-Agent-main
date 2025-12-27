import argparse
from src.utils import load_database
from src.agent import ResonanceAgent

def main():
    # 1. 設定 CLI 參數
    parser = argparse.ArgumentParser(description="Resonance Life Design Agent")
    parser.add_argument("--demo", action="store_true", help="Run in auto-pilot Demo mode")
    args = parser.parse_args()

    # 2. 載入資料庫
    db = load_database("data/mock_database.json")

    # 3. 啟動 Agent
    # [Requirement: Working Prototype]
    agent = ResonanceAgent(db, demo_mode=args.demo)
    agent.run()

if __name__ == "__main__":
    main()