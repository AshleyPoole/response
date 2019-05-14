FROM python:3.7

RUN apt-get update && apt-get install -y \
    netcat

# apt-get and system utilities
RUN apt-get update && apt-get install -y \
    curl apt-utils apt-transport-https debconf-utils gcc build-essential\
    && rm -rf /var/lib/apt/lists/*

# adding custom MS repository
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/16.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

# install SQL Server drivers
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql unixodbc-dev

WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app/

ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]