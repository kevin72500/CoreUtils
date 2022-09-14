from loguru import logger
logger.add("khandytool_log.log", rotation="50MB", encoding="utf-8", enqueue=True, compression="zip", retention="10 days")