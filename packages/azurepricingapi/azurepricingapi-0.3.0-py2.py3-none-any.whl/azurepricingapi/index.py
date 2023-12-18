from urllib import response
import requests


class Filter:
    
    """
    A utility class for validating and creating filter strings for Azure Pricing API.

    ...

    Attributes:
    -----------
        filterKeys (list): List of valid filter keys supported by the Azure Pricing API.
        apiEndpoint (str): The base URL of the Azure Pricing API.
        priceTypes (list): List of valid pricing types.

    Methods:
    --------
        _validate_filter(filter: list) -> bool:
            Validates the filter values against predefined criteria.
            Checks for adherence to expected keys and validates specific conditions.

    Note:
    -----
        The class assumes that filter values are provided as a list containing a dictionary.
        It provides methods to validate the filter and create filter query strings for API requests.
    """
    
    def __init__(self):
        self.filterKeys = ["armRegionName","location","meterId","meterName","productId","skuId","productName","skuName","serviceName","serviceId","serviceFamily","priceType","armSkuName"]
        self.apiEndpoint = "https://prices.azure.com/api/retail/prices"
        self.priceTypes = ["DevTestConsumption", "Consumption", "Reservation"]
        
    def _validate_filter(self, filter: list[dict]) -> bool:
        
        """
        Validates the filter values against predefined criteria.

        This function checks if the filter values adhere to the expected keys
        and validates specific conditions, such as the presence of valid keywords
        and pricing types.

        ...

        Parameters:
        -----------
            filter (list): A list containing a dictionary with filter values.

        Returns:
        --------
            bool: True if the filter is validated; False otherwise.

        Raises:
        -------
            Exception: If an invalid keyword or pricing option is detected.

        Note:
        -----
            The method assumes that the filter is a list containing a dictionary.
            It sets the 'flag' variable to True initially and updates it to False
            if any validation check fails.
        """
        
        flag = True
        for key, item in filter[0].items():
            if key not in self.filterKeys:
                raise Exception("Keyword Not Found")
                flag = False
            if key == "priceType" and item not in self.priceTypes:
                raise Exception("Invalid Pricing Option")
                flag = False
            
        return flag

    def _create_filter_string(self, filter:list) -> str:
        
        """
        Creates a filter query string based on the provided filter values.

        This function takes a list containing a dictionary with filter values and
        constructs a query string for filtering data using the Azure Pricing API.

        ...

        Parameters:
        -----------
            filter (list): A list containing a dictionary with filter values.

        Returns:
        --------
            str: The constructed filter query string.

        Note:
        -----
            The method assumes that the filter is a list containing a dictionary.
            It iterates over the dictionary items, constructing filter conditions,
            and joins them into a query string for use with the Azure Pricing API.
        """
        
        filter_string = "?$filter="
        
        for key, value in filter[0].items():
            if key == list(filter[0])[-1]:
                filter_string = filter_string + key + ' eq ' + f'\'{value}\''
            else:
                filter_string = filter_string + key + ' eq ' + f'\'{value}\'' + ' and '

        query_string = self.apiEndpoint + filter_string
        return query_string


class Pricing:
    
    """
    A class for retrieving pricing information from the Azure Pricing API.

    ...

    Attributes:
    -----------
        query (str): The query string for the Azure Pricing API.

    Methods:
    --------
        _send_request() -> list:
            Sends a GET request to the specified URL and retrieves pricing information.
            Returns a list of items from the response.

    Raises:
    -------
        Exception: If there is an issue with the request.

    Returns:
    --------
        list: A list of items containing pricing information.

    Note:
    -----
        The class is designed to handle paginated responses. The `_send_request` method
        continues making requests to the next page until no more pages are available.
    """

    def __init__(self, query: str) -> None:
        self.query = query

    def _send_request(self) -> list:
        """
            Sends a GET request to the specified URL and retrieves pricing information.

            Returns a list of items from the response.

            ...

            Raises:
            -------
                Exception: If there is an issue with the request.

            Returns:
            --------
                list: A list of items containing pricing information.

            Note:
            -----
                This method is designed to handle paginated responses. It continues
                making requests to the next page until no more pages are available.
        """
        
        url = self.query
        Items = []
        
        while True:
            try:
                response = requests.get(url)
                response.raise_for_status()
                json_response = response.json()
                Items.extend(json_response["Items"])
            except requests.exceptions.RequestException as e:
                raise Exception(str(e))
            
            if json_response.get("NextPageLink"):
                url = json_response["NextPageLink"]
            else:
                break

        return Items
    