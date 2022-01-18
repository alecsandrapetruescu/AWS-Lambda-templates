import pytest
import logging

import lambda_handler_basic

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Event list
event_list = [
    {'event': {'action': 'add', 'x': 1, 'y': 1}, 'context': {}, 'expected': 2},
    {'event': {'action': 'substract', 'x': 1, 'y': 1}, 'context': {}, 'expected': 0}
]


@pytest.mark.parametrize('event, context, expected', [
    (event_list[0]['event'], event_list[0]['context'], event_list[0]['expected']),
    (event_list[1]['event'], event_list[1]['context'], event_list[1]['expected'])
])
def test_basic(event, context, expected):
    """
    Test the execution of the function by providing a list of parameters as a dict

    :param event: The event containing a dict with parameters
    :param context: The context to be used by the function
    :param expected: The expected result of the function
    """
    response = lambda_handler_basic.lambda_handler(event, context)
    logger.info('Response: ', response)
    assert response['result'] == expected
