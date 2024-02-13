FROM python:3.8-slim-buster

RUN /usr/local/bin/python -m pip install --upgrade pip --progress-bar off
RUN pip install pandas==1.3.5 --progress-bar off

WORKDIR /app
COPY pipeline.py /app/pipeline.py

ENTRYPOINT ["bash"]