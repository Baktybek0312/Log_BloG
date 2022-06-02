import loguru

logger = loguru.logger
logger.remove()
logger.add(
    'file.log',
    format="{time} - {level} - ({extra[request_id]}) {message} ",
    level="DEBUG",
    enqueue=True
)
logger.debug('Error')
logger.info('Information message')
logger.warning('Warning')


def divide(a, b):
    logger.debug(f"Dividing {a} / {b} ...")
    result = a / b
    logger.debug(f"Result is {result}")
