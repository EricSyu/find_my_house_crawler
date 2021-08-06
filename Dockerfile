# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim-buster

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# setup env of app 
ENV TZ=Asia/Taipei
ENV MYSQL_HOST=
ENV MYSQL_PORT=
ENV MYSQL_DB_NAME=
ENV MYSQL_USER=
ENV MYSQL_PWD=
ENV HOUSE_TABLE_NAME=
ENV SENTRY_URL=
ENV SEQ_SERVER_URL=
ENV SEARCH_HOUSE_STR=

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "main.py"]
