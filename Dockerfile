FROM python:latest

WORKDIR /tmp

COPY generate_logs.py ./

CMD ["python", "./generate_logs.py"]