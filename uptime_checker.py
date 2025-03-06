#!/usr/bin/env python3
"""
Website Uptime Checker

This script periodically checks the availability of multiple websites,
logs downtime events, and handles errors appropriately.
"""

import argparse
import json
import logging
import os
import sys
import threading
import time
from datetime import datetime
from typing import Dict, Any, Optional, List

import requests
from requests.exceptions import RequestException, Timeout, ConnectionError, HTTPError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('uptime_log.txt'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Default configuration
DEFAULT_CONFIG = {
    "websites": [
        {
            "url": "https://www.google.com",
            "name": "Google",
            "interval": 60
        }
    ],
    "timeout": 10,   # seconds
    "max_retries": 3,
    "retry_delay": 5  # seconds
}


def load_config(config_path: str = "config.json") -> Dict[str, Any]:
    """
    Load configuration from a JSON file or use defaults if file doesn't exist.
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        Dictionary containing configuration parameters
    """
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                user_config = json.load(f)
                
                # Handle old config format (single website)
                if "url" in user_config and "websites" not in user_config:
                    # Convert old format to new format
                    website = {
                        "url": user_config["url"],
                        "name": user_config.get("name", user_config["url"]),
                        "interval": user_config.get("interval", 60)
                    }
                    user_config["websites"] = [website]
                
                # Ensure websites list exists
                if "websites" not in user_config:
                    user_config["websites"] = DEFAULT_CONFIG["websites"]
                
                logger.info(f"Loaded configuration from {config_path}")
                return user_config
        else:
            logger.info(f"Configuration file {config_path} not found. Using defaults.")
            return DEFAULT_CONFIG
    except json.JSONDecodeError:
        logger.error(f"Error parsing {config_path}. Using default configuration.")
        return DEFAULT_CONFIG
    except Exception as e:
        logger.error(f"Unexpected error loading configuration: {str(e)}. Using defaults.")
        return DEFAULT_CONFIG


def check_website(url: str, timeout: int) -> bool:
    """
    Check if a website is available by making an HTTP request.
    
    Args:
        url: The URL to check
        timeout: Request timeout in seconds
        
    Returns:
        True if website is up (returns 200 OK), False otherwise
        
    Raises:
        Various request exceptions that should be handled by the caller
    """
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()  # Raises an HTTPError for bad responses (4XX, 5XX)
    return True


def check_with_retry(url: str, timeout: int, max_retries: int, retry_delay: int) -> bool:
    """
    Check website availability with retry logic.
    
    Args:
        url: The URL to check
        timeout: Request timeout in seconds
        max_retries: Maximum number of retry attempts
        retry_delay: Delay between retries in seconds
        
    Returns:
        True if website is up, False if all retries failed
    """
    for attempt in range(max_retries):
        try:
            if attempt > 0:
                logger.info(f"[{url}] Retry attempt {attempt + 1}/{max_retries}")
            
            if check_website(url, timeout):
                if attempt > 0:
                    logger.info(f"[{url}] Successfully connected after {attempt + 1} attempts")
                return True
                
        except Timeout:
            logger.warning(f"[{url}] Request timed out after {timeout} seconds")
        except ConnectionError:
            logger.warning(f"[{url}] Failed to connect")
        except HTTPError as e:
            logger.warning(f"[{url}] HTTP error: {str(e)}")
        except RequestException as e:
            logger.warning(f"[{url}] Request failed: {str(e)}")
        except Exception as e:
            logger.warning(f"[{url}] Unexpected error: {str(e)}")
        
        # Don't sleep after the last attempt
        if attempt < max_retries - 1:
            time.sleep(retry_delay)
    
    return False


def log_downtime(url: str, name: str, error_msg: Optional[str] = None) -> None:
    """
    Log a downtime event to the log file.
    
    Args:
        url: The URL that is down
        name: The name of the website
        error_msg: Optional error message to include
    """
    message = f"DOWNTIME DETECTED: {name} ({url}) is unreachable"
    if error_msg:
        message += f" - Error: {error_msg}"
    
    logger.error(message)


def monitor_website(website: Dict[str, Any], config: Dict[str, Any], stop_event: threading.Event) -> None:
    """
    Monitor a single website in a separate thread.
    
    Args:
        website: Website configuration
        config: Global configuration
        stop_event: Threading event to signal when to stop monitoring
    """
    url = website["url"]
    name = website.get("name", url)
    interval = website.get("interval", 60)
    
    timeout = config.get("timeout", 10)
    max_retries = config.get("max_retries", 3)
    retry_delay = config.get("retry_delay", 5)
    
    logger.info(f"Starting monitoring for {name} ({url}) with interval {interval} seconds")
    
    consecutive_failures = 0
    
    while not stop_event.is_set():
        try:
            logger.debug(f"[{name}] Checking {url}...")
            
            if check_with_retry(url, timeout, max_retries, retry_delay):
                logger.info(f"[{name}] Website {url} is UP")
                consecutive_failures = 0
            else:
                consecutive_failures += 1
                log_downtime(url, name, f"Failed after {max_retries} attempts. Consecutive failures: {consecutive_failures}")
            
            # Sleep for the specified interval or until stop_event is set
            stop_event.wait(timeout=interval)
            
        except Exception as e:
            logger.error(f"[{name}] Unexpected error in monitoring thread: {str(e)}")
            # Sleep a bit to avoid tight error loops
            stop_event.wait(timeout=5)


def main() -> None:
    """Main function to run the uptime checker."""
    parser = argparse.ArgumentParser(description="Website Uptime Checker")
    parser.add_argument("--url", help="URL to check (adds to websites list)")
    parser.add_argument("--interval", type=int, help="Check interval in seconds for command-line URL")
    parser.add_argument("--config", default="config.json", help="Path to configuration file")
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Get the list of websites to monitor
    websites = config.get("websites", [])
    
    # Add command-line URL if provided
    if args.url:
        website = {
            "url": args.url,
            "name": args.url,
            "interval": args.interval if args.interval else 60
        }
        websites.append(website)
    
    if not websites:
        logger.error("No websites configured for monitoring. Exiting.")
        return
    
    logger.info(f"Starting Website Uptime Checker")
    logger.info(f"Monitoring {len(websites)} websites")
    
    # Create a stop event for graceful shutdown
    stop_event = threading.Event()
    
    # Create and start monitoring threads
    threads = []
    for website in websites:
        thread = threading.Thread(
            target=monitor_website,
            args=(website, config, stop_event),
            daemon=True
        )
        threads.append(thread)
        thread.start()
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    
    except KeyboardInterrupt:
        logger.info("Monitoring stopped by user")
        # Signal all threads to stop
        stop_event.set()
        
        # Wait for threads to finish (with timeout)
        for thread in threads:
            thread.join(timeout=2)
            
        logger.info("All monitoring threads stopped")
    
    except Exception as e:
        logger.error(f"Unexpected error in main thread: {str(e)}")
        stop_event.set()


if __name__ == "__main__":
    main() 
