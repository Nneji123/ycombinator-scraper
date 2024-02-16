FROM python:3.11

WORKDIR /app

RUN apt-get update && \
    apt-get install -y \
    wget \
    unzip \
    dpkg

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN apt-get update && apt-get -y install google-chrome-stable

# Copy your Python scripts or CLI tool into the container
COPY . /app

ENV VIRTUAL_ENV=/usr/local
ADD --chmod=655 https://astral.sh/uv/install.sh /install.sh
RUN /install.sh && rm /install.sh
 
COPY requirements.txt /requirements.txt
 
RUN /root/.cargo/bin/uv pip install --no-cache -r requirements.txt

# Run your CLI tool when the container starts
CMD ["python", "-m", "ycombinator_scraper"]
