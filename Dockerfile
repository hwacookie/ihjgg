# Use the official lightweight Python image.
FROM python:3.9-slim

# Set the working directory.
WORKDIR /app

# Copy the requirements file into the container.
COPY requirements.txt requirements.txt

# Install the dependencies.
RUN pip install -r requirements.txt

# Copy the rest of the working directory contents into the container.
COPY . .

# Copy the service account key
COPY ~/.keys/ihjgg-430319-b3a475019084.json /app/service-account-file.json

# Set the environment variable
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/service-account-file.json"

# Run Streamlit.
CMD streamlit run app.py --server.port $PORT
