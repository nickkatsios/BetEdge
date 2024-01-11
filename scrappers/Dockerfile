# Use a Python base image
FROM python:3.10

# Update package lists
RUN apt-get update

# Install firefox 
RUN apt-get install -y firefox-esr

# Install MySQL client to execute SQL scripts
RUN apt-get install -y default-mysql-client

# Install Poetry
RUN pip install poetry

# Set working directory inside the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY ./pyproject.toml ./poetry.lock ./

# Install dependencies
RUN poetry install

# Copy project files to the container
COPY . /app

# Command to run the application
CMD ["poetry", "run", "python3", "main_scrape.py" , "--logging" , "--headless" , "--browser", "firefox"]
