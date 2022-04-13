import json
import logging
from enum import Enum

logger = logging.getLogger()
logger.setLevel(logging.INFO)


# Define an ENUM with REST specific
class HTTP(Enum):
    HTTP_METHOD = 'httpMethod'
    QUERY_PARAMETERS = 'queryStringParameters'
    HEADERS = 'headers'
    BODY = 'body'
    STATUS_CODE = 'statusCode'

    def __str__(self):
        return self.value


# Define an ENUM with REST response codes
class RESPONSE_CODE(Enum):
    OK = 200
    BAD_REQUEST = 404
    METHOD_NOT_ALLOWED = 405


# Define a dict of operations called by the AWS Lambda function.
OPERATIONS = {
    'add': lambda first_operand, second_operand: first_operand + second_operand,
    'substract': lambda first_operand, second_operand: first_operand - second_operand,
}


def http_method_dict(method):
    return {
        'POST': lambda operation, first_operand, second_operand: OPERATIONS[operation](first_operand, second_operand)
    }.get(method, None)  # None will be returned as default if http method is not found


def response_error(code, message):
    return {
        str(HTTP.STATUS_CODE): str(code),
        str(HTTP.BODY): json.dumps({'message': f"{message}", 'code': f"Status code: {str(code)}."})
    }


def lambda_handler(event, context):
    """
    AWS lambda handler with a REST event.
    Executes an operation with two numbers and returns the result.

    :param event: The event that contains a http request.
    :param context: The context of the called function.
    :return: The result of the specified operation.
    """
    logger.info('Event: %s', json.dumps(event))

    http_method = event.get(str(HTTP.HTTP_METHOD))
    body = event.get(str(HTTP.BODY))

    method = http_method_dict(http_method)
    if method is None:
        return response_error(RESPONSE_CODE.METHOD_NOT_ALLOWED, 'The method specified is not allowed')

    request_body = json.loads(body)
    if request_body is None:
        return response_error(RESPONSE_CODE.BAD_REQUEST, 'Bad request.')

    result = method(request_body.get('operation'), request_body.get('x'), request_body.get('y'))

    logger.info('Calculated result of %s', result)

    response = {
        str(HTTP.STATUS_CODE): RESPONSE_CODE.OK.value,
        str(HTTP.BODY): json.dumps({'result': result})
    }
    return response
