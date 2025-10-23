# Document API Deployment Instructions

## Prerequisites
- Python 3.7 or higher
- pip (Python package manager)
- Docker (for Docker deployment)
- Docker Compose (for easy Docker deployment)

## Installation Steps

1. **Clone or copy the application files** to your VM:
   ```
   D:\WORK\Streamlit\Production\API
   ```

2. **Configure environment variables**:
   - Ensure your `.env` file is properly configured with Qdrant credentials
   - The file should already contain the necessary configuration

## Deployment Options

### Option 1: Direct Python Deployment

1. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment**:
   ```bash
   # On Windows
   venv\Scripts\activate
   
   # On Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the API**:
   ```bash
   python app.py
   ```

### Option 2: Docker Development Deployment (Recommended for Development)

For development, where you want to make code changes and restart without rebuilding:

1. **Start the service in development mode**:
   ```bash
   docker-compose up -d
   ```

2. **Make code changes** to `app.py` or other files

3. **Restart the service without rebuilding**:
   ```bash
   docker-compose restart
   ```

### Option 3: Docker Production Deployment

For production deployment with better performance and security:

1. **Start the service in production mode**:
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

## Default Configuration
- Host: 127.0.0.1 (localhost) for direct deployment
- Host: 0.0.0.0 (all interfaces) for Docker deployment
- Port: 5000 (can be changed with PORT environment variable)

## Running as a Service

### On Windows (Direct Deployment):
Use the provided `start_service.bat` file or configure as a Windows service.

### On Linux (Direct Deployment):
Use the provided `document-api.service` file:
1. Copy to systemd directory:
   ```bash
   sudo cp document-api.service /etc/systemd/system/
   ```
2. Reload systemd:
   ```bash
   sudo systemctl daemon-reload
   ```
3. Enable the service:
   ```bash
   sudo systemctl enable document-api
   ```
4. Start the service:
   ```bash
   sudo systemctl start document-api
   ```

## API Endpoints

1. `GET /` - Home page with API information
2. `GET /health` - Health check endpoint
3. `GET /documents` - Get all documents grouped by company
4. `GET /documents/<company_name>` - Get documents for a specific company

## Access from n8n

Once deployed, you can access the API from your n8n VM using:
```
http://[YOUR_VM_IP]:5000/documents
```

For example, if your VM IP is 192.168.1.100:
```
http://192.168.1.100:5000/documents
```

### For Docker Deployment in Same Network:
If both containers are in the same Docker network, you can use the service name:
```
http://document-api:5000/documents
```

## Development Workflow

1. **Start development environment**:
   ```bash
   docker-compose up -d
   ```

2. **Make code changes** to `app.py` or other files

3. **Restart without rebuilding**:
   ```bash
   docker-compose restart
   ```

4. **View logs**:
   ```bash
   docker-compose logs -f
   ```

## Stopping the Services

### For Docker:
```bash
# Development mode
docker-compose down

# Production mode
docker-compose -f docker-compose.prod.yml down

# Restart only (without stopping)
docker-compose restart
```

### For Direct Deployment:
Stop the process with Ctrl+C or kill the process if running in background.