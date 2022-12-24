FROM python:3.9
COPY . /
WORKDIR /
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 8081
ENTRYPOINT [ "python3" ]
CMD [ "app/serverB.py"]