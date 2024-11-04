# Use an official lightweight Python image.
FROM python:3.8-slim

# Set the working directory in the Docker container to /app
WORKDIR /app

# Copy the local directory contents to the container at /app
COPY . /app

# Install any necessary packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Define an environment variable
ENV NAME World

# Command to run on container start: run the Streamlit application
CMD ["streamlit", "run", "ship-prediction-app.py"]
