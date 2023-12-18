"""
Raises:
    ValueError: _description_

Returns:
    _type_: _description_
"""
import requests

class PhoneNumberValidator:
    """
    Checks if a phone number is valid or not
    """
    def __init__(self, api_key: str) -> None:
        """
        Initializes an instance of the class.

        Parameters:
            api_key (str): The API key to authenticate requests.

        Returns:
            None
        """
        self.api_key = api_key
        self.api_url = "https://api.numlookupapi.com/v1/validate/"

    def validate(self, phone_number: str, country_code: str = None) -> bool:
        """
        Validates a phone number using an API call.

        Args:
            phone_number (str): The phone number to be validated.
            country_code (str, optional): The country code of the phone number. Defaults to None.

        Returns:
            bool: True if the phone number is valid, False otherwise.

        Raises:
            ValueError: If the phone number is empty.
            HTTPError: If there is an error with the API call.

        """
        if not phone_number:
            raise ValueError("Phone number cannot be empty")
        response = self._make_api_call(phone_number, country_code)
        if response.ok:
            return response.json()["valid"]
        else:
            response.raise_for_status()

    def _make_api_call(self, phone_number: str, country_code: str = None) -> requests.Response:
        """
        Makes an API call using the provided phone number and optional country code.

        Args:
            phone_number (str): The phone number to use for the API call.
            country_code (str, optional): The country code to use for the API call.
              Defaults to None.

        Returns:
            requests.Response: The response object from the API call.
        """
        params = {"api_key": self.api_key}
        if country_code:
            params["country_code"] = country_code
        response = requests.get(self.api_url + phone_number, params=params, timeout=10)
        return response
