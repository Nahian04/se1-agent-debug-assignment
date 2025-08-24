import logging
import os
import re
from logging.handlers import TimedRotatingFileHandler
from zipfile import ZipFile
from datetime import datetime, timedelta

LOG_DIR = "logs"

os.makedirs(LOG_DIR, exist_ok=True)
ARCHIVE_DIR = os.path.join(LOG_DIR, "archive")
os.makedirs(ARCHIVE_DIR, exist_ok=True)

def archive_weekly_logs():
    """Archive logs older than 7 days into weekly zip files."""
    today = datetime.today()
    cutoff_date = today - timedelta(days=7)  # keep last 7 days

    # Collect all log files (exclude already zipped files)
    log_files = [
        f for f in os.listdir(LOG_DIR)
        if f.startswith(("info.log", "error.log")) and not f.endswith(".zip")
    ]

    # Map each log to its date
    date_file_map = {}
    date_pattern = re.compile(r"\d{4}-\d{2}-\d{2}")
    for f in log_files:
        match = date_pattern.search(f)
        if match:
            file_date = datetime.strptime(match.group(), "%Y-%m-%d")
            if file_date < cutoff_date:
                date_file_map.setdefault(file_date, []).append(os.path.join(LOG_DIR, f))

    # Group logs by week
    sorted_dates = sorted(date_file_map.keys())
    while sorted_dates:
        week_start = sorted_dates[0]
        week_end = week_start + timedelta(days=6)

        # Collect files for this week
        week_files = []
        to_remove = []
        for d in sorted_dates:
            if week_start <= d <= week_end:
                week_files.extend(date_file_map[d])
                to_remove.append(d)

        for d in to_remove:
            sorted_dates.remove(d)

        if week_files:
            zip_name = f"{week_start.strftime('%Y-%m-%d')}_to_{week_end.strftime('%Y-%m-%d')}.zip"
            zip_path = os.path.join(ARCHIVE_DIR, zip_name)

            with ZipFile(zip_path, "w") as zipf:
                for file in week_files:
                    zipf.write(file, arcname=os.path.basename(file))
                    os.remove(file)  # delete original log file

class WeeklyArchivingTimedRotatingFileHandler(TimedRotatingFileHandler):
    """TimedRotatingFileHandler that triggers weekly log archiving after rollover."""

    def doRollover(self):
        super().doRollover()
        archive_weekly_logs()  # Archive old logs weekly

def get_logger(name: str = __name__):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Capture all, filter via handlers

    # Prevent adding duplicate handlers if logger already configured
    if logger.hasHandlers():
        return logger

    # Common formatter
    formatter = logging.Formatter(
        fmt="%(asctime)s - [%(levelname)s] - [%(name)s] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # INFO + WARNING handler
    info_handler = WeeklyArchivingTimedRotatingFileHandler(
        filename=os.path.join(LOG_DIR, "info.log"),
        when="midnight",
        interval=1,
        backupCount=7,
        encoding="utf-8"
    )
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(formatter)
    info_handler.suffix = "%Y-%m-%d"
    info_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    info_handler.addFilter(lambda record: record.levelno < logging.ERROR)

    # ERROR handler
    error_handler = WeeklyArchivingTimedRotatingFileHandler(
        filename=os.path.join(LOG_DIR, "error.log"),
        when="midnight",
        interval=1,
        backupCount=7,
        encoding="utf-8"
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    error_handler.suffix = "%Y-%m-%d"
    error_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}$")

    # Add handlers
    logger.addHandler(info_handler)
    logger.addHandler(error_handler)

    return logger
