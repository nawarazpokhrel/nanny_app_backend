# Use an official Python runtime as a parent image
FROM python:3.8

# Set environment variable for Python to run in unbuffered mode
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Copy the entrypoint.sh script into the container
COPY entrypoint.sh /app/

# Make the entrypoint.sh script executable
RUN chmod +x /app/entrypoint.sh

# Expose port 8002 for the Django application
EXPOSE 8002

# Set the entry point to your entrypoint.sh script
ENTRYPOINT ["/app/entrypoint.sh"]
