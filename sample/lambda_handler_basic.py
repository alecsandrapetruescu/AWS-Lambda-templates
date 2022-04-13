import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Define a dict of operations called by the AWS Lambda function.
OPERATIONS = {
    'add': lambda x, y: x + y,
    'substract': lambda x, y: x - y,
}


def lambda_handler(event, context):
    """
    AWS lambda handler with a basic event.
    Executes an operation with two numbers and returns the result.

    :param event: The event that contains the parameters sent.
    :param context: The context of the called function.
    :return: The result of the specified operation.
    """
    logger.info('Event: %s', event)

    result = OPERATIONS[event['action']](event['x'], event['y'])
    logger.info('Calculated result of %s', result)

    response = {'result': result}
    return response

