FROM python:3.9

#RUN mkdir /code
#COPY requirements.txt /code
#RUN pip install -r /code/requirements.txt
#COPY . /code
##CMD ["python", "/code/manage.py", "runserver"]
#ENTRYPOINT ["python /code/manage.py runserver"]

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
#RUN mkdir /code
WORKDIR /code
RUN pip install --upgrade pip
COPY requirements.txt .

RUN pip install -r requirements.txt
COPY . .

CMD ["python", "manage.py", "runserver"]