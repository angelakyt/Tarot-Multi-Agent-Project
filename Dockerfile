# 使用官方 Python 基礎鏡像
FROM python:3.10-slim

# 將工作目錄設定為 /app
WORKDIR /app

# 將 requirements.txt 複製到工作目錄並安裝依賴
# 使用 --no-cache-dir 確保鏡像體積小
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製專案檔案 (main.py, tarot_data.py 等)
COPY . .

# 暴露 FastAPI 預設端口 (Hugging Face Spaces 預設使用 7860/7861)
# 這裡使用 7860 作為標準
EXPOSE 7860 

# 運行 FastAPI 服務 (這是啟動命令)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]