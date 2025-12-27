# Resonance-Life-Design-Agent
> 2025 Theory of Computation Final Project
> **Topic:** Intelligent Agents with LLMs - Life Design & Social Resonance Matching

## 📖 專案簡介 (Introduction)

**Resonance Agent** 是一個基於大型語言模型 (LLM) 的智慧代理人系統。不同於傳統的交友軟體只關注外在條件，本系統旨在透過深度的「人生設計訪談」，協助使用者探索核心價值。

本專案結合了 **Life Design (人生設計)** 與 **Resonance Algorithm (共振演算法)**，將非結構化的對話轉化為可量化的「人生向量」，並據此尋找能夠在夢想與天賦上互補的「成長夥伴 (Growth Partners)」。

## ✨ 核心功能 (Key Features)

1. **深度訪談狀態機 (Interview State Machine)**：
* 透過引導式對話，依序探索使用者的 **價值觀 (Values)**、**天賦 (Talents)** 與 **夢想 (Dreams)**。
* 支援 **Demo Mode**，可直接讀取使用者文本進行快速分析。


2. **LLM 語意分析 (Semantic Analysis)**：
* 串接 **Ollama API** ，將自然語言對話轉化為結構化的 JSON 靈魂檔案 (Soul Profile)。


* 自動生成「天賦 x 夢想」的人生方向建議。


3. **共振配對演算法 (Resonance Matching Algorithm)**：
* 計算使用者與資料庫中潛在夥伴的適配度。
* **邏輯**：價值觀一致 (Alignment) + 夢想同向 (Direction) + 天賦互補 (Complementarity)。



## ⚙️ 系統架構 (System Architecture)

本系統採用狀態機 (State Machine) 模型設計，如下圖所示：

```mermaid
graph TD
    Start([啟動 Agent]) --> ModeCheck{Demo Mode?}
    ModeCheck -->|Yes| FastTrack[讀取預設文本]
    ModeCheck -->|No| Q_Values[階段一：價值觀提問]
    
    Q_Values --> Q_Talents[階段二：天賦與才能提問]
    Q_Talents --> Q_Dreams[階段三：夢想提問]
    
    Q_Dreams --> Synthesis
    FastTrack --> Synthesis[資料聚合]
    
    Synthesis --> Analysis[LLM 分析與結構化 (Ollama API)]
    Analysis --> |生成| User_JSON[建立靈魂檔案 JSON]
    
    User_JSON --> Matching[共振演算法運算]
    
    subgraph Resonance_Logic [配對邏輯]
    Matching --> Filter{價值觀檢核}
    Filter --> Score[計算互補分數]
    end
    
    Score --> Output([輸出：人生報告與夥伴推薦])

```

## 📂 檔案結構 (File Structure)

```text
Resonance-Agent/
├── data/
│   └── mock_database.json   # 預先生成的虛擬夥伴資料庫 (用於演示配對功能)
├── src/
│   ├── agent.py             # 核心 Agent 類別 (狀態機邏輯實作)
│   ├── llm_client.py        # Ollama API 串接模組
│   ├── matcher.py           # Resonance 配對演算法
│   └── utils.py             # 工具函式 (JSON 處理、CLI 美化)
├── main.py                  # 程式進入點
├── requirements.txt         # 專案依賴套件
└── README.md                # 專案說明文件

```

## 🚀 快速開始 (Quick Start)

### 1. 環境設定 (Prerequisites)

確保已安裝 Python 3.8+。

```bash
# Clone 此專案
git clone https://github.com/YourUsername/Resonance-Life-Design-Agent.git
cd Resonance-Life-Design-Agent

# 安裝依賴套件
pip install -r requirements.txt

```

### 2. 設定 API Key

本專案使用助教提供的 Ollama API 服務。請在專案根目錄建立 `.env` 檔案或直接在 `src/llm_client.py` 中設定：

```python
# src/llm_client.py
API_KEY = "your_provided_api_key"
API_URL = "http://140.116.xxx.xxx:11434/api/generate" # 依助教公告為準

```

### 3. 執行程式

執行 `main.py` 啟動代理人：

```bash
python main.py

```

* **一般模式**：依照指示回答問題進行完整訪談。
* **Demo 模式**：程式會自動載入預設回答，展示分析與配對結果（適合期末展示）。

## 🧠 演算法設計 (Algorithm Design)

我們定義兩個人  (User) 與  (Candidate) 之間的共振分數 ：

*  (Values Match): 價值觀重疊度 (必要條件，若為 0 則總分為 0)。
*  (Dream Alignment): 夢想領域的相關性。
*  (Talent Complementarity): 天賦的互補性（例如：技術 + 行銷）。

## 📝 開發工具與引用 (Tools & Credits)

* **LLM Engine**: Meta Llama 3 (via Ollama API)
* **Development Assistant**: Google AI Studio & Gemini (for data generation & prompt engineering)
* **Diagrams**: Mermaid.js
