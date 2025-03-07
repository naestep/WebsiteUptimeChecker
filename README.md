# Website Uptime Checker

A Python script that periodically checks the availability of multiple websites, logs downtime events, and handles errors appropriately.

## Features

- Monitors multiple websites concurrently using threading
- Each website can have its own check interval
- Logs downtime events with timestamps
- Implements retry logic (up to 3 attempts by default)
- Handles common errors (timeouts, connection failures, HTTP errors)
- Configurable via a JSON configuration file
- Docker support for containerized deployment

## Project Structure

```
website-uptime-monitor/
├── uptime_checker.py  # Main script
├── config.json        # User settings
├── requirements.txt   # Dependencies
├── Dockerfile        # Docker configuration
├── docker-compose.yml # Docker Compose configuration
├── logs/             # Log directory (created automatically)
└── README.md         # Project documentation
```

## Installation

### Standard Installation

1. Clone this repository or download the files
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Docker Installation

1. Clone this repository
2. Make sure you have Docker and Docker Compose installed
3. Build and run the container:

```bash
docker-compose up -d
```

## Configuration

### Configuration File (config.json)

The configuration file uses the following structure:

```json
{
    "websites": [
        {
            "url": "https://www.google.com",
            "name": "Google",
            "interval": 60
        },
        {
            "url": "https://www.github.com",
            "name": "GitHub",
            "interval": 30
        }
    ],
    "timeout": 10,
    "max_retries": 3,
    "retry_delay": 5
}
```

#### Website Configuration

Each website in the `websites` array can have the following properties:

- `url`: The website URL to monitor (required)
- `name`: A friendly name for the website (optional, defaults to URL)
- `interval`: Check interval in seconds (optional, defaults to 60)

#### Global Settings

- `timeout`: Request timeout in seconds
- `max_retries`: Maximum number of retry attempts
- `retry_delay`: Delay between retries in seconds

## Usage

### Standard Usage

```bash
python uptime_checker.py
```

This will start monitoring all websites specified in the config.json file.

### Using a Custom Configuration File

```bash
python uptime_checker.py --config my_config.json
```

### Docker Usage

1. Start the container:
```bash
docker-compose up -d
```

2. View logs:
```bash
# View container logs
docker-compose logs -f

# View uptime logs
tail -f logs/uptime_log.txt
```

3. Stop the container:
```bash
docker-compose down
```

### Customizing Docker Configuration

1. The config.json file is mounted as a volume, so you can modify it without rebuilding the container
2. Logs are persisted in the ./logs directory
3. The container automatically restarts unless explicitly stopped

## Log Output Example

The script logs information to both the console and the log file. Example log output:

```
2023-07-15 14:30:00 - INFO - Starting Website Uptime Checker
2023-07-15 14:30:00 - INFO - Monitoring 3 websites
2023-07-15 14:30:00 - INFO - Starting monitoring for Google (https://www.google.com) with interval 60 seconds
2023-07-15 14:30:00 - INFO - Starting monitoring for GitHub (https://www.github.com) with interval 30 seconds
2023-07-15 14:30:00 - INFO - Starting monitoring for Example (https://www.example.com) with interval 120 seconds
2023-07-15 14:30:01 - INFO - [Google] Website https://www.google.com is UP
2023-07-15 14:30:01 - INFO - [GitHub] Website https://www.github.com is UP
```

## Stopping the Service

### Standard Mode
To stop the script, press `Ctrl+C` in the terminal where it's running. The script will gracefully shut down all monitoring threads.

### Docker Mode
```bash
docker-compose down
```

## License

This project is open source and available under the [MIT License](LICENSE). 
