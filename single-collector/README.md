# News Collector

![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![Docker](https://img.shields.io/badge/docker-compatible-blue.svg)
![aiohttp](https://img.shields.io/badge/aiohttp-3.8.4-blue.svg)
![asyncpg](https://img.shields.io/badge/asyncpg-0.27.0-blue.svg)
![beautifulsoup4](https://img.shields.io/badge/beautifulsoup4-4.12.2-blue.svg)
![pydantic](https://img.shields.io/badge/pydantic-1.10.7-blue.svg)
![APScheduler](https://img.shields.io/badge/APScheduler-3.10.1-blue.svg)

News Collector is an asynchronous Python script for collecting, processing, and storing news from telegram news agencies.

## Features

- 🔄 Asynchronous news collection
- 🧹 News text cleaning and processing
- 🏷️ Automatic news categorization
- 📊 News embedding generation
- 📝 News summary creation
- 🗓️ Scheduled operation (hourly)
- 🐳 Docker support

## Requirements

- Python 3.9+
- PostgreSQL
- Docker (optional)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/news-collector.git
   cd news-collector
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root directory and add the following environment variables:
   ```
   DB_NAME=your_database_name
   DB_USER=your_database_user
   DB_PASS=your_database_password
   DB_HOST=your_database_host
   DB_PORT=your_database_port
   ```

## Usage

### Running the script

To run the script, execute:

```
python main.py
```

The script will run every hour to collect and process new news.

### Using Docker

1. Build the Docker image:
   ```
   docker-compose build
   ```

2. Run the containers:
   ```
   docker-compose up -d
   ```

## Project Structure

```
news-collector/
│
├── api/
│   └── client.py
├── db/
│   └── database.py
├── models/
│   └── news_item.py
├── news/
│   ├── parser.py
│   └── processor.py
├── .env
├── docker-compose.yaml
├── Dockerfile
├── main.py
├── README.md
└── requirements.txt
```

## Module Descriptions

- `api/client.py`: Client for interacting with news service APIs
- `db/database.py`: Database connection and operation management
- `models/news_item.py`: Data model for news articles
- `news/parser.py`: Parser for extracting news from HTML
- `news/processor.py`: News processor (categorization, embedding generation, etc.)
- `main.py`: Main script managing the news collection process

## Contributing

We welcome contributions to the project! Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

✈️ [telegram](https://t.me/data_silence) 
📬 [email](mailto:enjoy@data-silence.com)
