# Use a lightweight Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the script
COPY listener.py .

# Expose the TCP listening port
EXPOSE 5055

# Run the listener script
CMD ["python", "listener.py"]
