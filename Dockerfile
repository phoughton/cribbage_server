# Multi-stage build: First stage for building React app
FROM node:18-slim as react-builder

WORKDIR /app/react-ui

# Copy React app files
COPY react-ui/package*.json ./
RUN npm ci --only=production

COPY react-ui/ ./
RUN npm run build

# Second stage: Python Flask app
FROM python:3.11-slim-bullseye

WORKDIR /app

ENV PORT 5000
EXPOSE 5000

# Install Python dependencies
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Copy Python app files
COPY . .

# Copy React build from first stage
COPY --from=react-builder /app/react-ui/build ./react-ui/build

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
