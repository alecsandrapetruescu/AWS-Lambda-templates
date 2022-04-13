from http import HTTPStatus
import json

import pytest
import logging

from sample import lambda_handler_rest

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
        'expected': {
            'statusCode': HTTPStatus.OK.value,
            'body': {
                'result': 2
            }
        }
    },
    {
        'event': {
            'httpMethod': 'POST',
            'body': json.dumps({'operation': 'substract', 'x': 1, 'y': 1})
        },
        'context': {},
        'expected': {
            'statusCode': HTTPStatus.OK.value,
            'body': {
                'result': 0
            }
        }
    },
    {
        'event': {
            'httpMethod': 'POST',
            # 'body': ''
        },
        'context': {},
        'expected': {
            'statusCode': HTTPStatus.BAD_REQUEST.value,
            'body': {
                'code': HTTPStatus.BAD_REQUEST.value,
                'message': HTTPStatus.BAD_REQUEST.phrase,
                'description': HTTPStatus.BAD_REQUEST.description
            }
        }
    },
    {
        'event': {
            'httpMethod': 'POST',
            'body': '{}'
        },
        'context': {},
        'expected': {
            'statusCode': HTTPStatus.BAD_REQUEST.value,
            'body': {
                'code': HTTPStatus.BAD_REQUEST.value,
                'message': HTTPStatus.BAD_REQUEST.phrase,
                'description': HTTPStatus.BAD_REQUEST.description
            }
        }
    },
    {
        'event': {
            'httpMethod': 'GET',
        },
        'context': {},
        'expected': {
            'statusCode': HTTPStatus.METHOD_NOT_ALLOWED.value,
            'body': {
                'code': HTTPStatus.METHOD_NOT_ALLOWED.value,
                'message': HTTPStatus.METHOD_NOT_ALLOWED.phrase,
                'description': HTTPStatus.METHOD_NOT_ALLOWED.description
            }
        }
    }
]


@pytest.mark.parametrize('event, context, expected', [
    (event_list[0]['event'], event_list[0]['context'], event_list[0]['expected']),
    (event_list[1]['event'], event_list[1]['context'], event_list[1]['expected']),
    (event_list[2]['event'], event_list[2]['context'], event_list[2]['expected']),
    (event_list[3]['event'], event_list[3]['context'], event_list[3]['expected']),
    (event_list[4]['event'], event_list[4]['context'], event_list[4]['expected'])
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
    assert response['statusCode'] == expected['statusCode']
    if response['statusCode'] == HTTPStatus.OK.value:
        assert json.loads(response['body'])['result'] == expected['body']['result']
    else:
        response_dictionary = json.loads(response['body'])
        assert response_dictionary['code'] == expected['body']['code']
        assert response_dictionary['message'] == expected['body']['message']
        assert response_dictionary['description'] == expected['body']['description']
