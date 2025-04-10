FROM python:3.11-slim
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["streamlit", "run", "./Home.py", "--server.address=0.0.0.0", "--server.port=8501"]
EXPOSE 8501
