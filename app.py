import streamlit as st
import requests
import json

# --- 應用標題與配置 ---
st.set_page_config(page_title="🔮 AI 塔羅牌大師", layout="wide")

# ==============================================================================
WEBHOOK_URL = "https://Angela-Kao-n8n-free.hf.space/webhook/34eaca38-15d2-42a5-8194-889ec8ce4149" 


st.title("🔮 AI 塔羅牌大師")

# --- 側邊欄：牌陣說明 ---
st.sidebar.header("牌陣與主題")
st.sidebar.markdown(
    """
    此服務將根據您的問題和情境，自動選擇合適的牌陣 (例如：時間流、聖三角等)，
    並調用 RWS 專業模型進行深度解讀。
    """
)

# --- 用戶輸入區 (Agent 1) ---
st.header("1. 輸入您的問題與情境")

# 選擇主題 (用於 FastAPI 決定牌陣)
topic_options = ['整體運勢/通用', '愛情/關係', '事業/工作', '財務/金錢', '身心靈/成長']
selected_topic = st.selectbox("請選擇您的主要主題：", topic_options)

# 核心輸入
user_question = st.text_input("輸入您的核心問題：(例如：我近期應該注意什麼？)")
user_context = st.text_area("提供背景情境描述：(例如：我剛換了新工作，感到有些焦慮。)", height=100)

# --- 提交按鈕與處理 ---
if st.button("✨ 獲取塔羅解讀報告", type="primary"):
    
    # 檢查必要輸入
    if not user_question.strip():
        st.error("請完整輸入您的核心問題！")
    else:
        # 1. 準備發送給 n8n 的數據
        payload = {
            "question": user_question,
            "topic": selected_topic,
            "context": user_context
        }
        
        # 2. 顯示加載狀態
        with st.spinner("⏳ 正在調用 AI 代理人進行抽牌與解讀 (Agent 2, 3, 4)..."):
            try:
                # 3. 發送 POST 請求到 n8n Webhook (Agent 4 的入口)
                response = requests.post(WEBHOOK_URL, json=payload, timeout=60)
                
                # 4. 檢查 HTTP 狀態碼
                if response.status_code == 200:
                    # 5. 解析 n8n 回傳的 JSON 數據
                    report_data = response.json()
                    
                    # --- 顯示最終結果 (從 Agent 4 接收) ---
                    st.success("✅ 塔羅解讀報告已完成！")
                    
                    st.markdown("---")
                    
                    # 顯示 LLM 產生的解讀報告 (Markdown 格式)
                    st.markdown("### 📜 您的專屬解讀報告")
                    # report_data['tarot_report'] 包含 LLM 產生的 Markdown 文本
                    st.markdown(report_data.get('tarot_report', '抱歉，解讀內容缺失。')) 
                    
                else:
                    st.error(f"❌ 後端服務調用失敗 (HTTP 狀態碼: {response.status_code})")
                    st.json(response.json()) # 顯示錯誤詳情
                    
            except requests.exceptions.Timeout:
                st.error("❌ 請求超時！請檢查 n8n 流程是否執行時間過長。")
            except Exception as e:
                st.error(f"❌ 發生未知錯誤: {e}")

