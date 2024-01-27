# Using Docker for YCombinator Scraper

## Prerequisites

Before you start, ensure that you have Docker installed on your system.

## Building the Docker Image

To build the Docker image, navigate to the directory containing the Dockerfile and run the following command:

```bash
docker build -t yc-scraper .
```

This command builds the Docker image and tags it with the name `yc-scraper`.

## Running the Docker Container

Once the image is built, you can run the Docker container using the following command:

```bash
docker run -e LOGIN_USERNAME=your_username -e LOGIN_PASSWORD=your_password yc-scraper
```

Replace `your_username` and `your_password` with your actual Workatastartup username and password.

### Environment Variables

- `LOGIN_USERNAME`: Your Workatastartup username.
- `LOGIN_PASSWORD`: Your Workatastartup password.

### Optional Environment Variables

You can also set the following optional environment variables:

- `LOGS_DIRECTORY`: Directory for logs (default is `/app/logs`).
- `HEADLESS_MODE`: Whether to run the scraper in headless mode (default is `True`).

## Using the Docker Image from Docker Hub

If you prefer not to build the image locally, you can pull it from Docker Hub:

```bash
docker pull nneji123/yc_scraper:latest
```

Then, you can run the container as described in the previous section.

## Note

Make sure to replace `your_username` and `your_password` with your actual Workatastartup credentials.

```
