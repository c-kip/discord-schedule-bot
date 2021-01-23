# Base Image
FROM python:3.6.8

# Create app directory
WORKDIR /usr/src/app

# Install app dependencies
# COPY requirements.txt .
RUN pip install -U python-dotenv
RUN pip install -U discord.py

# Copy source code and static files
COPY . .
RUN chmod +x main.py

# Run app
CMD [ "python", "./main.py" ]