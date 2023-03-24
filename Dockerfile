FROM public.ecr.aws/docker/library/python:latest

COPY ./src /service
COPY requirements-docker.txt /service
WORKDIR /service
RUN echo Installing Python packages listed in requirements.txt
RUN pip3 install -r requirements-docker.txt
RUN echo Starting python and starting the Flask service...
ENTRYPOINT ["python3"]
CMD ["flask_app.py"]