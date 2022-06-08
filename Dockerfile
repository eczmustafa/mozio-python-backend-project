FROM python:3.9.7

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install gdal
RUN apt-get update &&\
    apt-get install -y binutils libproj-dev gdal-bin

RUN apt install -y postgis postgresql-13-postgis-3

COPY requirements.txt /app/

# Install pipenv
RUN pip install --upgrade pip 
# RUN pip install --upgrade protobuf<=3.20.1
RUN pip install -r requirements.txt

# Install application dependencies
#COPY Pipfile Pipfile.lock /app/
# We use the --system flag so packages are installed into the system python
# and not into a virtualenv. Docker containers don't need virtual environments. 
#RUN pipenv install --system --dev

# Copy the application files into the image
COPY . /app/

# Expose port 8000 on the container
EXPOSE 8000