FROM python:3.10

# Install dependencies
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

# Copy the API code
COPY app.py /app/
COPY auth.py /app/
COPY database.py /app/
COPY fnb.py /app/
COPY script.py /app/

# Set the working directory to the API code
WORKDIR /app

# Expose the API port
EXPOSE 5000

# Run the API
CMD ["flask", "run"]