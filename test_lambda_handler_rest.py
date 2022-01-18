import json

import pytest
import logging

import lambda_handler_rest

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Event list
event_list = [
    {
        'event': {
            'httpMethod': 'POST',
            'body': json.dumps({'operation': 'add', 'x': 1, 'y': 1})
        },
        'context': {},
        'expected': 200
    },
    {
        'event': {
            'httpMethod': 'POST',
            'body': json.dumps({'operation': 'substract', 'x': 1, 'y': 1})
        },
        'context': {},
        'expected': 200
    }
]


@pytest.mark.parametrize('event, context, expected', [
    (event_list[0]['event'], event_list[0]['context'], event_list[0]['expected']),
    (event_list[1]['event'], event_list[1]['context'], event_list[1]['expected'])
])
def test_basic(event, context, expected):
    """
    Test the execution of the function by providing a list of parameters as a "REST" dict

    :param event: The event containing a dict with parameters
    :param context: The context to be used by the operation
    :param expected: The expected result of the operation
    """
    response = lambda_handler_rest.lambda_handler(event, context)
    logger.info('Response: ', response)
    assert response['statusCode'] == expected
