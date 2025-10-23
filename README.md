# Document API for Qdrant

A REST API service to retrieve document information from Qdrant, grouping documents by company.

## Features

- RESTful API endpoints for document retrieval
- Group documents by company metadata
- Health check endpoint
- CORS support for cross-origin requests
- Docker support for easy deployment
- Environment-based configuration

## API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `GET /documents` - Get all documents grouped by company
- `GET /documents/<company_name>` - Get documents for a specific company

## Deployment

The API can be deployed in multiple ways:

1. **Direct Python deployment**
2. **Docker container**
3. **Docker Compose (development and production modes)**

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## Configuration

The service is configured using environment variables in a `.env` file. See `.env.example` for required variables.

## Requirements

- Python 3.7+
- Flask
- Qdrant client
- Docker (for containerized deployment)

## License

MIT