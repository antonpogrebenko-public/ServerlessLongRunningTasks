## Architecture

The application consists of the following components:

- FastAPI application running on AWS Lambda
- SNS Topic for system events (SQS or RabbitMQ can be used as well)
- DynamoDB table for task state management (Use Redis for in-memory storage)
- Serverless framework for infrastructure management

## Prerequisites

- Python 3.12
- AWS Account with appropriate permissions
- Serverless Framework
- AWS CLI configured

## Infrastructure

The application uses the following AWS services:

- **API Gateway**: Handles HTTP requests
- **Lambda**: Runs the FastAPI application and event listeners
- **SNS**: Message broker for system events
- **DynamoDB**: Stores task states
- **SSM Parameter Store**: Stores configuration values

## Project Structure

```
├── serverless.yml         # Serverless framework configuration
├── src/
│   ├── app.py            # FastAPI application entry point
│   ├── views/
│   │   └── example.py    # API route handlers
│   ├── listeners/
│   │   └── system_event_listener.py  # SNS event consumer
│   └── data_access/
│       └── models.py     # DynamoDB models
```

## Setup

1. Install dependencies (use requirements-dev.txt if you don't use Powertools for AWS Lambda layer):
```bash
pip install -r requirements.txt
```

2. Configure SSM parameters:
```bash
# For staging environment
aws ssm put-parameter --name "/staging/v1/sns/system_event_topic_name" --value "your-topic-name" --type String
aws ssm put-parameter --name "/staging/v1/sns/system_event_topic_arn" --value "your-topic-arn" --type String
aws ssm put-parameter --name "/staging/v1/tables/long_running_tasks_table" --value "your-table-name" --type String
```

3. Install Serverless dependencies:
```bash
npm install
```

4. Deploy:
```bash
serverless deploy --stage staging
```

## API Endpoints

### POST v1/example/process-task

Initiates a long-running task and returns a task ID for status tracking.

**Request Body:**
```json
{
    "data": {
        // Task-specific data
    }
}
```

**Response:**
```json
{
    "task_id": "uuid-string"
}
```

## Task Processing Flow

1. Client makes a request to the API endpoint
2. API creates a task ID and publishes a message to SNS
3. SNS listener processes the message asynchronously
4. Task state is stored in DynamoDB with a 1-hour TTL
5. Client can poll for task status using the task ID

## Development

To run locally:

```bash
python src/app.py
```

This will start the FastAPI application on `http://localhost:4000`

## Configuration

The application uses the following environment variables:

- `API_STAGE`: Deployment stage (staging/prod)
- `POWERTOOLS_SERVICE_NAME`: Service name for AWS Lambda Powertools
- `POWERTOOLS_LOG_LEVEL`: Log level for AWS Lambda Powertools

## Deployment

The application supports multiple stages:
- staging
- prod

To deploy to a specific stage:

```bash
serverless deploy --stage staging --region us-east-1
```

## Features

- CORS enabled for all origins with HTTP/HTTPS
- OpenAPI documentation available at `/v1/openapi.json`
- Automatic request/response compression
- ARM64 architecture for better performance/cost ratio
- 15-minute timeout for background tasks
- 30-second timeout for API requests
- Automatic TTL for task results (1 hour)

## Dependencies

- FastAPI: Web framework
- Mangum: AWS Lambda adapter for ASGI applications
- AWS Lambda Powertools: Logging and utilities
- PynamoDB: DynamoDB ORM
- Arrow: DateTime handling
- Nest AsyncIO: Async support for Lambda environment

## CI/CD
To trigger a deployment using GitLab CI/CD, uncomment everything in `.gitlab-ci.yml` file.

