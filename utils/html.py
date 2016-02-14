import requests
import logging

logger = logging.getLogger("entivaluator")


def check_json_response(response):
    """
    A helper function for checking http responses
    :param response: requests.Response
    :return: list or dict
    """
    if response and response.status_code == 200:
        return response.json()
    return []


def post_request(url, payload, headers):
    """
    A helper function for posting data to evaluators
    :param url: str: entity linker's url
    :param payload: list or dict containing data
    :param headers: dict custom headers to be sent
    :return requests.response
    """

    try:
        response = requests.post(url, data=payload, headers=headers)
        return response
    except requests.exceptions.RequestException as ex:
        logger.warning("Failed to submit data to %s and got a : %s ", url, ex)
