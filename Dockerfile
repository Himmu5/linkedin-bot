# Build for Fargate with: docker build --platform linux/amd64 -t linkedin-bot .
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Optional: avoid baking secrets into the image
# Pass env at runtime with --env-file or -e

CMD ["python", "cli.py", "post"]