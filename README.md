# Flask MySQL DevSecOps Application

A modern Flask REST API with MySQL database integration, featuring a complete DevSecOps pipeline with automated security scanning, testing, and deployment.

## Project Overview

This project demonstrates best practices for building secure, production-ready Python web applications with:
- **Flask API**: RESTful endpoints for CRUD operations on items
- **MySQL Database**: Persistent storage with SQLAlchemy ORM
- **Docker Containerization**: Multi-container setup with docker-compose
- **DevSecOps Pipeline**: Automated security scanning, testing, and deployment
- **Comprehensive Testing**: Unit and integration tests with pytest

## Features

### API Endpoints
- `GET /api/health` - Health check with database connectivity verification
- `GET /api/` - API information and available endpoints
- `GET /api/items` - Retrieve all items
- `GET /api/items/<id>` - Retrieve specific item
- `POST /api/items` - Create new item
- `PUT /api/items/<id>` - Update item
- `DELETE /api/items/<id>` - Delete item

### Database
- MySQL 8.0 container with automatic schema creation
- SQLAlchemy ORM for type-safe queries
- Automatic timestamps (created_at, updated_at)

### Security Pipeline
1. **Linting**: Hadolint for Dockerfile best practices
2. **Secret Scanning**: Gitleaks to detect exposed credentials
3. **SAST**: Bandit for Python security analysis
4. **Testing**: Pytest with comprehensive test coverage
5. **Build**: Docker image creation with version tagging
6. **CVE Scanning**: Trivy for vulnerability detection
7. **SBOM Generation**: Syft for software Bill of Materials
8. **Deployment**: Docker-compose orchestration
9. **Health Checks**: Automated endpoint verification
10. **DAST**: OWASP ZAP for dynamic security testing

## Project Structure

```
flask-mysql-app/
├── app/
│   ├── __init__.py           # Application factory
│   ├── main.py               # API routes/blueprints
│   ├── models.py             # SQLAlchemy models
│   └── database.py           # Database initialization
├── tests/
│   ├── __init__.py
│   └── test_api.py           # Pytest test suite
├── .github/
│   └── workflows/
│       └── pipeline.yml      # GitHub Actions CI/CD
├── Dockerfile                # Container image
├── docker-compose.yml        # Multi-container orchestration
├── CICD.sh                   # Local pipeline script
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Local Development

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- Git

### Setup

1. **Clone the repository**:
   ```bash
   cd /home/insa/projects/flask-mysql-app
   ```

2. **Start the application**:
   ```bash
   docker-compose up -d
   ```
   This will start:
   - MySQL database on port 3306
   - Flask API on port 9002

3. **Verify deployment**:
   ```bash
   curl http://localhost:9002/api/health
   ```

### Testing

Run the full test suite locally:
```bash
pip install -r requirements.txt
pytest tests/test_api.py -v
```

## CI/CD Pipeline

### GitHub Actions
Push to `main` branch automatically triggers the workflow (`.github/workflows/pipeline.yml`).

The workflow runs on a self-hosted runner and includes:
- Dockerfile linting
- Secret scanning
- Python SAST analysis
- Unit and integration tests
- Docker image build
- CVE vulnerability scanning
- SBOM generation
- Deployment with docker-compose
- Health checks
- Dynamic security testing with ZAP
- Artifact uploads (SBOM, DAST reports)

### Local Pipeline Execution
Run the entire pipeline locally:
```bash
chmod +x CICD.sh
./CICD.sh
```

## API Examples

### Create an Item
```bash
curl -X POST http://localhost:9002/api/items \
  -H "Content-Type: application/json" \
  -d '{"name": "My Item", "description": "Item description"}'
```

### Get All Items
```bash
curl http://localhost:9002/api/items
```

### Get Specific Item
```bash
curl http://localhost:9002/api/items/1
```

### Update Item
```bash
curl -X PUT http://localhost:9002/api/items/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Name"}'
```

### Delete Item
```bash
curl -X DELETE http://localhost:9002/api/items/1
```

## Database

### MySQL Credentials
- **Host**: db (within docker-compose network)
- **User**: app_user
- **Password**: app_password
- **Database**: app_db
- **Port**: 3306

### Access MySQL CLI
```bash
docker exec -it flask-mysql-db mysql -u app_user -p app_db
```

## Monitoring & Logs

### View Application Logs
```bash
docker-compose logs -f app
```

### View Database Logs
```bash
docker-compose logs -f db
```

### Check Container Status
```bash
docker-compose ps
```

## Troubleshooting

### Container won't start
```bash
docker-compose logs app
docker-compose down --volumes
docker-compose up -d
```

### Database connection issues
Ensure the database is healthy before the app starts:
```bash
docker-compose ps db
```

### Port already in use
Change port mappings in `docker-compose.yml` if port 9002 or 3306 are already in use.

## Security Considerations

- MySQL credentials should be managed via environment variables in production
- Use `.env` file for local development (add to `.gitignore`)
- Consider using secrets management tools (AWS Secrets Manager, HashiCorp Vault, etc.)
- Enable HTTPS/TLS for production deployments
- Implement API authentication (JWT, OAuth2)
- Regular dependency updates with `pip-audit`

## Technologies Used

- **Framework**: Flask 3.0.0
- **ORM**: Flask-SQLAlchemy 3.1.1
- **Database**: MySQL 8.0
- **Testing**: Pytest 8.0.0
- **Container**: Docker & Docker Compose
- **Security**: Hadolint, Gitleaks, Bandit, Trivy, Syft, OWASP ZAP

## License

MIT

## Support

For issues or questions, please open an issue on GitHub or contact the development team.
