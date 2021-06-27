import json

import pytest
from fastapi import status
from fastapi.exceptions import RequestValidationError
from pydantic import errors, ValidationError
from pydantic.error_wrappers import ErrorWrapper
from starlette.testclient import TestClient

from calculator import calculator, CalculationRequestModel


@pytest.fixture(scope='module')
def test_app():
    client = TestClient(calculator)
    yield client


@pytest.fixture()
def get_request_data_dict():
    """ Fixture to create request parameters """
    def _get_request_dict(number1, number2):
        return {'number1': number1, 'number2': number2}
    return _get_request_dict


@pytest.fixture()
def get_json_error_from_calc_model():
    """ Fixture to create a response error list from CalculationRequestModel """
    def _get_request_model_error(test_values: dict) -> list:
        """
        Creates fake request error response
        :param test_values: dict with request items
        :return: list details of error like it will be from api call
        """
        request_json_error = None
        try:
            CalculationRequestModel(**test_values)
        except ValidationError as ex:
            request_error = RequestValidationError([ErrorWrapper(ex, "body")])
            request_json_error = json.loads(request_error.json())
        return request_json_error
    return _get_request_model_error


# Positive scenarios
def test_positive_values(test_app, get_request_data_dict):
    test_data = get_request_data_dict(1, 2)
    response = test_app.post('/calc', json=test_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'result': 1 + 2}


def test_two_long_long_values(test_app, get_request_data_dict):
    test_data = get_request_data_dict(9223372036854775807, 9223372036854775807)

    response = test_app.post('/calc', json=test_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'result': 9223372036854775807 + 9223372036854775807}

# Negative scenarios
def test_one_zero_values(test_app, get_request_data_dict, get_json_error_from_calc_model):
    test_data = get_request_data_dict(0, 1)

    response = test_app.post('/calc', json=test_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()['detail'] == get_json_error_from_calc_model(test_data)


def test_negative_values(test_app, get_request_data_dict, get_json_error_from_calc_model):
    test_data = get_request_data_dict(-1, -2)

    response = test_app.post('/calc', json=test_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()['detail'] == get_json_error_from_calc_model(test_data)


def test_null_values(test_app, get_request_data_dict, get_json_error_from_calc_model):
    test_data = get_request_data_dict(None, None)

    response = test_app.post('/calc', json=test_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()['detail'] == get_json_error_from_calc_model(test_data)


def test_string_values(test_app, get_request_data_dict, get_json_error_from_calc_model):
    test_data = get_request_data_dict('a', 'b')

    response = test_app.post('/calc', json=test_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()['detail'] == get_json_error_from_calc_model(test_data)


def test_float_numbers(test_app, get_request_data_dict, get_json_error_from_calc_model):
    test_data = get_request_data_dict(1.1, 2.3)

    response = test_app.post('/calc', json=test_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()['detail'] == get_json_error_from_calc_model(test_data)


def test_infinity(test_app, get_request_data_dict, get_json_error_from_calc_model):
    test_data = get_request_data_dict(float('inf'), float('inf'))

    response = test_app.post('/calc', json=test_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()['detail'] == get_json_error_from_calc_model(test_data)


def test_missing_parameter(test_app, get_json_error_from_calc_model):
    test_data = {"number1": 1}

    response = test_app.post('/calc', json=test_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()['detail'] == get_json_error_from_calc_model(test_data)
    







