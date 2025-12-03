# main.py (FastAPI 服務版本 - 完整的 Agent 1 & 2 封裝)
# ----------------------------------------------------
import random
from typing import Dict, List, Any
from fastapi import FastAPI
from pydantic import BaseModel

# 從本地檔案導入資料 (需要 tarot_data.py 和 tarot_keywords.py)
from tarot_data import CARD_DECK, SPREADS, TOPIC_TO_SPREAD

# 初始化 FastAPI 應用
app = FastAPI(title="Tarot Agent Service")

# 定義輸入資料格式 (使用 Pydantic)
class TarotInput(BaseModel):
    question: str
    topic: str
    context: str

# ====================================================
# AGENT 1: 提問者/情境設定代理人 核心邏輯
# ====================================================
def agent1_context_setup(raw_data: Dict[str, str]) -> Dict[str, str]:
    """
    Agent 1 核心函式：接收原始輸入，進行清理和標準化。
    """
    raw_question = raw_data.get('question', '').strip()
    raw_topic = raw_data.get('topic', '').strip()
    raw_context = raw_data.get('context', '').strip()

    # --- 步驟 1: 輸入清理與驗證 ---
    if not raw_question:
        raw_question = "沒有明確問題，請求進行整體運勢解讀。"
    if raw_topic not in TOPIC_TO_SPREAD:
        raw_topic = '通用/其他'
    if not raw_context:
        raw_context = "問卜者未提供額外情境描述。"
        
    standard_output = {
        'question': raw_question,
        'topic': raw_topic,
        'context': raw_context
    }
    return standard_output
    
# ====================================================
# AGENT 2: 牌陣選擇/抽牌代理人 核心邏輯
# ====================================================
def agent2_card_selection(topic: str) -> Dict[str, Any]:
    """
    Agent 2 的核心函式：根據主題選擇牌陣並進行虛擬抽牌。
    """
    spread_name = TOPIC_TO_SPREAD.get(topic, TOPIC_TO_SPREAD['通用/其他'])
    position_names = SPREADS[spread_name]
    num_cards = len(position_names)
    
    try:
        drawn_cards = random.sample(CARD_DECK, num_cards)
    except ValueError:
        return {"error": "Invalid card count", "spread_name": spread_name}
    
    result_list = []
    for i in range(num_cards):
        card_name = drawn_cards[i]
        position_name = position_names[i]
        orientation = "正位" if random.random() < 0.5 else "逆位"
        
        result_list.append({
            'position_name': position_name,
            'card_name': card_name,
            'orientation': orientation
        })
    
    return {
        'spread_name': spread_name,
        'cards_drawn': result_list
    }

# ====================================================
# API 路由：結合 Agent 1 和 Agent 2
# ====================================================
@app.post("/api/v1/draw_cards")
def draw_cards_api(input_data: TarotInput):
    # 1. Agent 1 處理輸入 (將 Pydantic 模型轉為字典)
    standard_data = agent1_context_setup(input_data.model_dump())
    
    # 2. Agent 2 根據標準化後的 topic 抽牌
    card_data = agent2_card_selection(standard_data['topic'])
    
    # 3. 組合最終輸出 (包含情境和抽牌結果)
    final_output = {**standard_data, **card_data} # 合併兩個字典
    
    return final_output

# ====================================================
# 啟動區塊 (用於本地測試)
# ====================================================
if __name__ == "__main__":
    import uvicorn
    print("--- 啟動 FastAPI 服務 (Agent 1 & 2) ---")
    # uvicorn 會在 http://127.0.0.1:8000 啟動服務
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)