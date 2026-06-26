# 🔗 URL Shortener

A REST API built with **FastAPI** that shortens URLs with support for custom short codes, click tracking, and automatic link expiry.

Built as a learning project to explore FastAPI, Pydantic, and Docker.

---

## Features

- **Shorten any URL** — generates a random 6-character short code
- **Custom short codes** — pick your own code (e.g. `/google`)
- **Click tracking** — tracks how many times a link has been visited
- **Link expiry** — auto-deletes links after N days
- **Persistent storage** — saves all links to a local `urls.json` file
- **Interactive docs** — FastAPI auto-generates Swagger UI at `/docs`

---

## Project Structure

```
url-shortener/
├── main.py        # FastAPI app and all endpoints
├── models.py      # Pydantic models for request/response validation
├── storage.py     # JSON read/write logic
├── urls.json      # Auto-created on first run
├── Dockerfile     # Docker configuration
└── requirements.txt
```

---

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/shorten` | Shorten a URL |
| `GET` | `/{short_code}` | Redirect to original URL |
| `GET` | `/{short_code}/stats` | View click stats |
| `DELETE` | `/{short_code}` | Delete a short link |

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/Santoosh13/url-shortener.git
cd url-shortener
```

### 2. Create and activate a virtual environment

```bash
python -m venv url-short

# Mac/Linux
source url-short/bin/activate

# Windows
url-short\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the server

```bash
uvicorn main:app --reload
```

Visit **`http://localhost:8000/docs`** to explore and test all endpoints interactively.

---

## API Usage

### Shorten a URL

```bash
POST /shorten
```

```json
{
  "url": "https://www.google.com",
  "custom_code": "google",
  "expiry_days": 7
}
```

Response:

```json
{
  "short_code": "google",
  "short_url": "http://localhost:8000/google",
  "original_url": "https://www.google.com",
  "expires_on": "2026-06-25T11:05:16"
}
```

### Redirect

```
GET /google  →  redirects to https://www.google.com
```

### View Stats

```bash
GET /google/stats
```

```json
{
  "short_code": "google",
  "original_url": "https://www.google.com",
  "click_count": 5,
  "created_at": "2026-06-18T11:05:16",
  "expires_on": "2026-06-25T11:05:16"
}
```

### Delete a Link

```bash
DELETE /google  →  204 No Content
```

---

## Running with Docker 🐳

The project has been containerized using Docker. The Docker image is hosted privately on Docker Hub at `santoosh13/url-shortener-1`.

### Build the image locally

```bash
docker build -t url-shortener .
```

### Run a container from the image

```bash
docker run -p 8000:8000 url-shortener
```

### Useful Docker commands used in this project

```bash
# Build the image
docker build -t url-shortener .

# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# List all images
docker images

# Stop a container
docker stop <container_id>

# Remove a container
docker rm <container_id>
```

Visit **`http://localhost:8000/docs`** after running the container to test the API.

---

## Tech Stack

| | Tool |
|---|---|
| Framework | FastAPI |
| Validation | Pydantic |
| Server | Uvicorn |
| Storage | JSON file |
| Containerization | Docker |

---

## What I Learned

- Building REST APIs with FastAPI
- Data validation using Pydantic models
- Separation of concerns across multiple files
- HTTP status codes (201, 204, 307, 404, 409, 410)
- Persistent storage with JSON
- Containerizing a Python app with Docker
- Git branching and pushing to GitHub

---

## Author

**Santoosh13** — [GitHub](https://github.com/Santoosh13)
