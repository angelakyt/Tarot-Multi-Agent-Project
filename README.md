# 🔮 多代理塔羅解讀系統 (Multi-Agent Tarot Reading System)

## 簡介
本專案基於 **大型語言模型 (LLM)** 和 **多代理系統 (MAS)** 架構，提供一個高效、專業且可客製化的 AI 塔羅牌解讀服務。

## 專案架構與代理人分工

| 代理人 (Agent) | 角色 | 技術/實現檔案 |
| :--- | :--- | :--- |
| **Agent 1** (情境設定) | 清理、規範化使用者輸入。 | FastAPI (`main.py`) |
| **Agent 2** (抽牌邏輯) | 根據主題選擇牌陣並執行隨機抽牌。 | FastAPI (`main.py`, `tarot_data.py`) |
| **Agent 3** (知識嵌入/RAG) | 檢索 RWS 關鍵字，增強 LLM 上下文。 | n8n Code 節點 (`多代理-塔羅.json`) |
| **Agent 4** (報告生成/協調) | 整合所有數據，生成最終報告，控制流程。 | n8n LLM 節點 (`多代理-塔羅.json`) |

## 🕹️ 網頁 DEMO 連結 
**[請在步驟 3 部署完成後，將 Streamlit 網址貼在此處]**

## 📂 原始碼文件

* `app.py`: Streamlit 前端介面。
* `main.py`: 封裝 Agent 1 (輸入處理) 和 Agent 2 (抽牌邏輯) 的 FastAPI 服務。
* `tarot_data.py`: 牌陣定義與牌組清單（Agent 2 靜態知識庫）。
* `tarot_keywords.py`: RWS 牌義關鍵字資料庫（Agent 3 RAG 知識庫）。
* `多代理-塔羅.json`: n8n 工作流設定檔（Agent 3 & 4 協調層）。

## ⚙️ 環境設置 (Run Locally)
1. 確保 Python 3.8+。
2. 啟動虛擬環境：`source venv/bin/activate`
3. 安裝依賴：`pip install -r requirements.txt` 
4. 運行 FastAPI 後端：`uvicorn main:app --reload`
5. 運行 Streamlit 前端：`streamlit run app.py`