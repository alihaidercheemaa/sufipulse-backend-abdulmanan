# SufiPulse Backend

## Security Notice
This application is configured to run on localhost only for security reasons. This prevents unauthorized external access to the server.

## Running the Application

### Development (Local Only)
```bash
# Using the local runner (recommended for development)
python run_local.py

# Or using uvicorn directly
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

### With Docker (Restricted to localhost)
```bash
# Build the Docker image
docker build -t sufi-pulse-backend .

# Run the container (only accessible from localhost)
docker run -p 8000:8000 sufi-pulse-backend
```

## Configuration

The application is configured to:
- Bind only to localhost (127.0.0.1)
- Accept connections only from local origins (CORS restricted)
- Use environment variables for sensitive data

## Environment Variables

Copy the `.env.example` to `.env` and fill in the appropriate values:

```bash
cp .env.example .env
```

Required environment variables:
- `DATABASE_URL`: PostgreSQL database connection string
- `JWT_SECRET`: Secret key for JWT token signing
- `GOOGLE_CLIENT_ID`: Google OAuth client ID
- `RESEND_API_KEY`: API key for Resend email service
- `FROM_EMAIL`: Email address to send emails from (e.g., connect@sufipulse.com)
- `YOUTUBE_API_KEY`: YouTube Data API key

## Security Features

- Server binds only to localhost (127.0.0.1)
- CORS restricted to local origins only
- Sensitive data stored in environment variables
- Proper authentication and authorization mechanisms