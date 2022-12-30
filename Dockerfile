FROM python:3.10-slim
LABEL maintainer="super.mvk@yandex.ru"

ENV VENV_PATH=/opt/venv \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
ENV PATH="$VENV_PATH/bin:$PATH"
RUN python -m venv $VENV_PATH && \
    useradd -ms /bin/sh app

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot ./bot/
COPY main.py .
RUN mkdir storage && \
    chown app:app storage

USER app

CMD ["python3", "main.py"]
