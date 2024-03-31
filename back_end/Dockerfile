FROM python:3.7.16

# WORKDIR /app
# COPY ./detectors ./detectors
# COPY ./static ./static
# COPY ./templates ./templates
# COPY app.py ./
# COPY app_1.py ./
# COPY config.py ./
# COPY dataOfEffect.json ./
# COPY detect.py ./
# COPY normalize.py ./
# COPY package-lock.json ./
# COPY requirements.txt ./
# COPY ./__pycache__ ./__pycache__
# RUN pip3 install -r requirements.txt

COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY . /app

CMD ["python3", "app.py"]