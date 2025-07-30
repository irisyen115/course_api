# 使用輕量版 Python 作為基底
FROM python:3.11-slim

# 設定工作目錄
WORKDIR /app

# 複製需求與程式碼
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app

# 執行 FastAPI 應用程式
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
