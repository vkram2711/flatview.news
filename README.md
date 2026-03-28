# flatview.news

A web app that uses LLMs to translate news from foreign sources that may be underreported by your national media. Read global news in Arabic, English, French, German, Japanese, Spanish, or Ukrainian — all translated on the fly by GPT-4o-mini.

## Preview

![photo_2026-03-29_03-07-20](https://github.com/user-attachments/assets/b52e4e4c-4b8a-4a42-a154-6831234abae4)

## How it works

1. **News ingestion** — articles are fetched from [GNews](https://gnews.io/) and full content is extracted via [WorldNewsAPI](https://worldnewsapi.com/).
2. **Language detection** — each article's language is detected automatically.
3. **Translation** — articles are translated into all supported languages using OpenAI GPT-4o-mini via LangChain, processed in async batches.
4. **Serving** — a Flask API serves articles with their translations from MongoDB. The React frontend lets users pick a language and browse the feed.

## Tech stack

| Layer | Technology |
|---|---|
| Frontend | React 18, Auth0, Stripe, React Router |
| Backend | Python / Flask |
| Database | MongoDB Atlas (via MongoEngine) |
| AI | OpenAI GPT-4o-mini, LangChain |
| News sources | GNews API, WorldNewsAPI |
| Feedback | Notion API |
| Auth | Auth0 |
| Payments | Stripe |

## Supported languages

Arabic, English, French, German, Japanese, Spanish, Ukrainian

---

## Getting started

### Prerequisites

- Python 3.9+
- Node.js 18+
- A MongoDB Atlas cluster
- API keys for: OpenAI, GNews, WorldNewsAPI, Notion (optional), Auth0, Stripe (optional)

### 1. Clone the repository

```bash
git clone https://github.com/your-username/flatview.news.git
cd flatview.news
```

### 2. Configure environment variables

**Backend:**

```bash
cp backend/.env.example backend/.env
# fill in your values
```

**Frontend:**

```bash
cp frontend/.env.example frontend/.env
# fill in your values
```

See the [Environment variables](#environment-variables) section for descriptions of each variable.

### 3. Run locally

**Backend:**

```bash
cd backend
pip install -r requirements.txt
python app.py
```

The API will be available at `http://localhost:5000`.

**Frontend:**

```bash
cd frontend
npm install
npm start
```

The app will open at `http://localhost:3000`.

### 4. Load news

To fetch articles and run translations:

```bash
cd backend
python load_news.py
```

---

## Run with Docker

```bash
# Copy and fill in environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Build and start both services
docker compose up --build
```

The frontend will be available at `http://localhost:80` and the backend API at `http://localhost:5000`.

---

## Environment variables

### Backend (`backend/.env`)

| Variable | Description |
|---|---|
| `MONGO_URI` | Full MongoDB Atlas connection string |
| `OPENAI_API_KEY` | OpenAI API key for translations |
| `NEWS_API_KEY` | [GNews](https://gnews.io/) API key |
| `NEWS_SCRAPPER_API_KEY` | [WorldNewsAPI](https://worldnewsapi.com/) key for full article extraction |
| `NOTION_API_KEY` | Notion integration token (for feedback storage) |
| `NOTION_DATABASE_ID` | ID of the Notion database to store feedback in |
| `FLASK_DEBUG` | Set to `true` to enable Flask debug mode (development only) |
| `PORT` | Port to run the backend on (default: `5000`) |

### Frontend (`frontend/.env`)

| Variable | Description |
|---|---|
| `REACT_APP_API_BASE_URL` | URL of the backend API (e.g. `http://localhost:5000`) |
| `REACT_APP_AUTH0_DOMAIN` | Auth0 tenant domain |
| `REACT_APP_AUTH0_CLIENT_ID` | Auth0 application client ID |
| `REACT_APP_STRIPE_PUBLISHABLE_KEY` | Stripe publishable key (starts with `pk_`) |

---

## API reference

### `GET /top_news`

Returns a list of articles in the requested language.

**Query parameters:**

| Parameter | Default | Description |
|---|---|---|
| `language` | `en` | Language code (`ar`, `en`, `fr`, `de`, `ja`, `es`, `uk`) |

**Response:**

```json
{
  "original_articles": [
    {
      "_id": "...",
      "title": "Article title (translated)",
      "description": "Short description (translated)",
      "image_url": "https://...",
      "publish_date": "2024-01-01T00:00:00",
      "language": "fr",
      "source": { "name": "Le Monde", "url": "https://..." }
    }
  ]
}
```

### `GET /article/<article_id>`

Returns the full article content, translated into the requested language.

**Query parameters:** same `language` param as above.

### `POST /feedback`

Submits user feedback to the Notion database.

**Request body:**

```json
{
  "feedback": "Great app!",
  "rating": 5,
  "contact": "user@example.com"
}
```

---

## Project structure

```
flatview.news/
├── backend/
│   ├── app.py               # Flask application and API routes
│   ├── load_news.py         # Script to fetch and translate news
│   ├── notion_utils.py      # Notion API integration (feedback)
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── .env.example
│   ├── mongo/
│   │   ├── models.py        # MongoEngine document models
│   │   └── mongo_utils.py   # MongoDB connection setup
│   └── utils/
│       ├── news_utils.py    # News fetching and storage
│       ├── translation_utils.py  # LLM translation pipeline
│       └── json_utils.py    # JSON parsing helpers
├── frontend/
│   ├── src/
│   │   ├── App.js           # Root component, Auth0 + Stripe setup
│   │   ├── NewsFeed.js      # Article list view
│   │   ├── Article.js       # Single article view
│   │   ├── ArticlesContext.js  # Global state (articles, language)
│   │   ├── CustomDropdown.js   # Language selector
│   │   └── ...
│   ├── Dockerfile
│   ├── nginx.conf
│   └── .env.example
├── docker-compose.yml
└── README.md
```

## License

MIT
