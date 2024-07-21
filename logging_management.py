"""
BLUEPRINT TO UNDERSTAND IT BETTER
LLD LOGGING SYSTEM

Classes:
1. LogLevel (Enum): Represents the log level.
   - Values: DEBUG, INFO, WARNING, ERROR, FATAL

2. LogAppender (Abstract Class): Base class for log appenders.   - Methods: append(log_message)

3. ConsoleAppender: Prints log messages to console.   - Inherits: LogAppender
   - Methods: append(log_message)

4. FileAppender: Writes log messages to a file.   - Inherits: LogAppender
   - Attributes: file_path
   - Methods: __init__(file_path), append(log_message)

6. LogMessage: Represents a log message.
   - Attributes: level, message, timestamp
   - Methods: __init__(level, message), __str__()

7. LoggerConfig: Configuration for the logger.
   - Attributes: log_level, log_appender
   - Methods: __init__(log_level, log_appender)

8. Logger: Singleton class for logging.
   - Attributes: _instance, config
   - Methods: __init__(), get_instance(), set_config(config), log(level, message), debug(message), info(message), warning(message), error(message), fatal(message)

Usage:
- Initialize logger instance with Logger.get_instance().
- Log messages using debug, info, warning, error, fatal methods.
- Change configuration with set_config(config).

C+P
"""

from enum import Enum
from abc import ABC, abstractmethod
import psycopg2
import time

# Enum for log levels
class LogLevel(Enum):
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    FATAL = 5

# Abstract base class for log appenders
class LogAppender(ABC):
    @abstractmethod
    def append(self, log_message):
        pass

# Console appender implementation
class ConsoleAppender(LogAppender):
    def append(self, log_message):
        print(log_message)

# File appender implementation
class FileAppender(LogAppender):
    def __init__(self, file_path):
        self.file_path = file_path
    
    def append(self, log_message):
        with open(self.file_path, "a") as file:
            file.write(str(log_message) + "\n")

# Log message class
class LogMessage:
    def __init__(self, level, message):
        self.level = level
        self.message = message
        self.timestamp = int(time.time() * 1000)
    
    def get_level(self):
        return self.level
    
    def get_message(self):
        return self.message
    
    def get_timestamp(self):
        return self.timestamp
    
    def __str__(self):
        return f"[{self.level}] {self.timestamp} - {self.message}"
    
# Logger configuration class
class LoggerConfig:
    def __init__(self, log_level, log_appender):
        self.log_level = log_level
        self.log_appender = log_appender
    
    def get_log_level(self):
        return self.log_level
    
    def get_log_appender(self):
        return self.log_appender
    
# Singleton Logger class
class Logger:
    _instance = None
    
    @staticmethod
    def get_instance():
        if Logger._instance is None:
            Logger()
        return Logger._instance
    
    def __init__(self):
        if Logger._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Logger._instance = self
            self.config = LoggerConfig(LogLevel.INFO, ConsoleAppender())
        
    def set_config(self, config):
        self.config = config
    
    def log(self, level, message):
        if level.value >= self.config.get_log_level().value:
            log_message = LogMessage(level, message)
            self.config.get_log_appender().append(log_message)
    
    def debug(self, message):
        self.log(LogLevel.DEBUG, message)
    
    def info(self, message):
        self.log(LogLevel.INFO, message)
    
    def warning(self, message):
        self.log(LogLevel.WARNING, message)
    
    def error(self, message):
        self.log(LogLevel.ERROR, message)
    
    def fatal(self, message):
        self.log(LogLevel.FATAL, message)

# Demo class to show logging in action
class LoggingFrameworkDemo:
    @staticmethod
    def run():
        logger = Logger.get_instance()
        
        # Logging with default configuration
        logger.debug("This is a debug message")
        logger.info("This is an information message")
        logger.warning("This is a warning message")
        logger.error("This is an error message")
        logger.fatal("This is a fatal message")
        
        # Changing log level and appender
        config = LoggerConfig(LogLevel.DEBUG, FileAppender("app.log"))
        logger.set_config(config)
        
        logger.debug("This is a debug message")
        logger.info("This is an information message")

if __name__ == "__main__":
    LoggingFrameworkDemo.run()
