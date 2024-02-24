FROM python:3.9

COPY . /app
WORKDIR /app

# RUN chown -R root /app && chmod +x /app/effectBot.py
RUN pip install -r requirements.txt

CMD ["python3", "/app/effectBot.py"]
