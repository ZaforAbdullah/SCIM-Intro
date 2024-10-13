# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose ports
EXPOSE 5000

# Define environment variable to disable buffered output
ENV PYTHONUNBUFFERED=1

# Run app.py when the container launches
CMD python server.py && tail -f /dev/null
