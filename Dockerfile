FROM python:3.11

WORKDIR /app

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
    libgtk-3-0  \
    dpkg

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN apt-get update && apt-get -y install google-chrome-stable

# Copy your Python scripts or CLI tool into the container
COPY . /app

# Install Python dependencies
RUN pip install -r requirements.txt

ARG HEADLESS_MODE=True

# Run your CLI tool when the container starts
CMD ["python", "-m", "ycombinator_scraper"]
