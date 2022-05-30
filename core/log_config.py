import loguru


logger = loguru.logger
logger.remove()
logger.add(
    'file.log',
    format="{time} - {level} - ({extra[request_id]}) {message} ",
    level="DEBUG",
    enqueue=True
)


def divide(a, b):
    logger.debug(f"Dividing {a} / {b} ...")
    result = a / b
    logger.debug(f"Result is {result}")



