FROM python:3.12-slim
WORKDIR /app
COPY app.py .
RUN useradd --system --no-create-home appuser
USER appuser
EXPOSE 8002
CMD ["python", "app.py"]
