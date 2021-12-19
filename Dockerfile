FROM python:3.7-slim AS compile-image

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --user -r requirements.txt --no-cache-dir


FROM python:3.7-alpine AS build-image
COPY --from=compile-image /root/.local /root/.local
COPY . /bot
ENV PYTHONUNBUFFERED=1
ENV PATH=/root/.local/bin:$PATH

CMD cd /bot && ls && python main.py
#CMD python /bot/main.py