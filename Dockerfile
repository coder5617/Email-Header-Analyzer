FROM python:3.13-slim

WORKDIR /app
ENV PYTHONPATH=/app/src

RUN pip install --upgrade pip pip-tools

COPY requirements.in .

RUN pip-compile requirements.in --output-file=requirements.txt && \
    pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

EXPOSE 8501
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

CMD ["streamlit", "run", "src/email_header_analyzer/ui/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
