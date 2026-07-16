FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY streamlit/dashboard.py .
CMD ["streamlit", "run", "dashboard.py", "--server.port=8501"]
