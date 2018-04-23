FROM python:3.6

COPY get_count.py get_count.py

ENTRYPOINT ["python"]
CMD "get_count.py"
