FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

ENV APP_HOME=/app

COPY requirements.txt $APP_HOME/requirements.txt

RUN pip install --no-cache-dir --upgrade -r $APP_HOME/requirements.txt

COPY models/machine-learning-models/models $APP_HOME/models

RUN find $APP_HOME/models -type f -name 'requirements.txt' -exec pip install -r {} \;

COPY routes $APP_HOME/routes
COPY main.py $APP_HOME/main.py