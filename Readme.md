Image Moderation API
A FastAPI-based Image Moderation API with a React frontend, using MongoDB for token and usage tracking, containerized with Docker.
Prerequisites

Docker and Docker Compose
Git
Node.js (for local frontend development, optional)
Python 3.11 (for local backend development or testing, optional)

Setup

Clone the repository:
git clone https://github.com/faizan17579/image_moderation
cd image-moderation-api


Copy the environment file:
cp .env.example .env


Build and start the services:
docker-compose up --build


Access the services:

Backend API: http://localhost:7000
Frontend UI: http://localhost:3000
MongoDB: mongodb://localhost:27017
API Docs: http://localhost:7000/docs



API Endpoints

POST /auth/tokens: Create a new token (admin-only).
Body: {"isAdmin": boolean}
Response: {"token": string}


GET /auth/tokens: List all tokens (admin-only).
Response: Array of {"token": string, "isAdmin": boolean, "createdAt": datetime}


DELETE /auth/tokens/{token}: Delete a token (admin-only).
Response: {"message": "Token deleted"}


POST /moderate: Upload an image for moderation.
Body: Form-data with file (image)
Response: {"result": {"is_safe": boolean, "categories": {string: float}}}



Usage

Open the frontend at http://localhost:3000.
Enter a bearer token (generate one via POST /auth/tokens using an admin token).
Upload an image to receive a moderation report.

Git Workflow

main: Production-ready branch.
Create feature branches (e.g., feature/add-auth) for development.
Submit pull requests (PRs) to main for code reviews.
CI pipeline (in .github/workflows/ci.yml) runs linting (flake8, eslint) and tests (pytest).

Testing
Run backend tests:
cd backend
pip install -r requirements.txt
pytest

Tests are located in backend/app/tests/ and cover authentication and moderation endpoints.
Image Moderation
The analyze_image function in backend/app/routers/moderate.py is a placeholder. To integrate a real model:

AWS Rekognition: Add boto3 to requirements.txt and implement the client in analyze_image. Example:import boto3
def analyze_image(image: UploadFile) -> ModerationResult:
    client = boto3.client('rekognition')
    response = client.detect_moderation_labels(Image={'Bytes': image.file.read()})
    categories = {label['Name']: label['Confidence'] / 100 for label in response['ModerationLabels']}
    return ModerationResult(is_safe=len(categories) == 0, categories=categories)

Update .env with AWS credentials and add to docker-compose.yml environment.
NSFW.js: Deploy a Node.js service with NSFW.js and call it from moderate.py via HTTP.

Notes

Ensure MongoDB is running before starting the backend.
The frontend uses Tailwind CSS for styling and Axios for API calls.
Replace the placeholder moderation logic with a real model for production use.

