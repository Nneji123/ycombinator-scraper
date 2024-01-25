# Use the official Python image as the base image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Install necessary dependencies
RUN apt-get update && \
    apt-get install -y \
    wget \
    unzip \
    libglib2.0-0 \
    libnss3 \
    libx11-6 \
    libx11-xcb1 \
    libxcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxi6 \
    libxrandr2 \
    libxrender1 \
    libxss1 \
    libxtst6 \
    fonts-liberation \
    libappindicator1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0

# Download and install Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' && \
    apt-get update && \
    apt-get install -y google-chrome-stable

# Download and install Chromedriver
RUN CHROME_VERSION=$(google-chrome-stable --version | awk '{print $3}' | cut -d. -f1) && \
    CHROMEDRIVER_VERSION=$(curl -sS https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_$CHROME_VERSION) && \
    wget -q https://googlechromelabs.github.io/$CHROMEDRIVER_VERSION/chromedriver-linux64.zip && \
    unzip chromedriver-linux64.zip && \
    rm chromedriver-linux64.zip && \
    mv chromedriver /usr/local/bin/

# Copy your Python scripts or CLI tool into the container
COPY . /app

# Install Python dependencies
RUN pip install -r requirements.txt  # Adjust this based on your requirements

# Set environment variables, if needed
# ENV VARIABLE_NAME=value

# Run your CLI tool when the container starts
CMD ["python", "-m", "cli.py"]
