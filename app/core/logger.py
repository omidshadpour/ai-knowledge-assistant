import logging
import os

os.makedirs("logs" , exist_ok= True)

def get_logger(name :str) -> logging.Logger:

    logger = logging.getLogger(name)

    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    file_handler = logging.FileHandler("logs/app.log" , encoding = "utf-8")
    file_handler.setLevel(logging.DEBUG)


    formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        datefmt = "%Y-%m-%d %H:%M:%S"
    )

    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger