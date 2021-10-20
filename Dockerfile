FROM python:3.7.3-stretch
LABEL maintainer="Adeyemi A."

## Step 1:
# Create a working directory
WORKDIR /app

## Step 2:
# Copy source code to working directory
COPY ./techtrends /app

## Step 3:
# Install packages from requirements.txt
# hadolint ignore=DL3013
RUN pip install --upgrade pip &&\
    pip install --trusted-host pypi.python.org -r requirements.txt

RUN python init_db.py

## Step 4:
# Expose port 3111
EXPOSE 3111

## Step 5:
# Run app.py at container launch
CMD ["python", "app.py"]