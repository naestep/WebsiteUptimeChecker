# Website Uptime Checker

A Python script that periodically checks the availability of a website, logs downtime events, and handles errors appropriately.

## Features

- Periodically checks website availability (default: every 60 seconds)
- Logs downtime events with timestamps
- Implements retry logic (up to 3 attempts by default)
- Handles common errors (timeouts, connection failures, HTTP errors)
- Configurable via command-line arguments or a configuration file

## Project Structure

```
website-uptime-monitor/
├── uptime_checker.py  # Main script
├── uptime_log.txt     # Log file (auto-generated)
├── config.json        # User settings
├── requirements.txt   # Dependencies
├── README.md          # Project documentation
```

## Installation

1. Clone this repository or download the files
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

You can configure the uptime checker in two ways:

### 1. Configuration File (config.json)

Create or modify the `config.json` file with the following structure:

```json
{
    "url": "https://www.example.com",
    "interval": 60,
    "timeout": 10,
    "max_retries": 3,
    "retry_delay": 5
}
```

Parameters:
- `url`: The website URL to monitor
- `interval`: Check interval in seconds
- `timeout`: Request timeout in seconds
- `max_retries`: Maximum number of retry attempts
- `retry_delay`: Delay between retries in seconds

### 2. Command-Line Arguments

You can override the configuration file settings using command-line arguments:

```bash
python uptime_checker.py --url https://www.example.com --interval 30 --config custom_config.json
```

Available arguments:
- `--url`: URL to check (overrides config file)
- `--interval`: Check interval in seconds (overrides config file)
- `--config`: Path to configuration file (default: config.json)

## Usage

### Basic Usage

```bash
python uptime_checker.py
```

This will start monitoring the URL specified in the config.json file (or the default URL if no config file exists).

### Custom URL

```bash
python uptime_checker.py --url https://www.example.com
```

### Custom Interval

```bash
python uptime_checker.py --interval 30
```

### Custom Configuration File

```bash
python uptime_checker.py --config my_config.json
```

## Log Output Example

The script logs information to both the console and the `uptime_log.txt` file. Example log output:

```
2023-07-15 14:30:00 - INFO - Starting Website Uptime Checker
2023-07-15 14:30:00 - INFO - Monitoring URL: https://www.example.com
2023-07-15 14:30:00 - INFO - Check interval: 60 seconds
2023-07-15 14:30:01 - INFO - Website https://www.example.com is UP
2023-07-15 14:31:01 - INFO - Website https://www.example.com is UP
2023-07-15 14:32:01 - WARNING - Failed to connect to https://www.example.com
2023-07-15 14:32:06 - INFO - Retry attempt 2/3
2023-07-15 14:32:06 - WARNING - Failed to connect to https://www.example.com
2023-07-15 14:32:11 - INFO - Retry attempt 3/3
2023-07-15 14:32:11 - WARNING - Failed to connect to https://www.example.com
2023-07-15 14:32:11 - ERROR - DOWNTIME DETECTED: https://www.example.com is unreachable - Error: Failed after 3 attempts. Consecutive failures: 1
```

## Stopping the Script

To stop the script, press `Ctrl+C` in the terminal where it's running.

## License

This project is open source and available under the [MIT License](LICENSE). 
