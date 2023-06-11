FROM python:3.9.5

# Set the working directory to /app
WORKDIR /kacaaki
COPY requirements.txt /kacaaki

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 8000

COPY . .

# Define environment variable
# ENV NAME kacaaki

# Run app.py when the container launches
CMD ["python","manage.py","runserver","0.0.0.0:8000"]