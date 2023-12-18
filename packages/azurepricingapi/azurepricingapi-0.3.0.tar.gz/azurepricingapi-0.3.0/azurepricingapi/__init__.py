from .index import Filter
from .index import Pricing

__author__ = 'Ravi Rana'
__version__ = '0.3.0'

def get_pricing(filter: list) -> list:
    """
    Get pricing information based on the provided filter.

    This function uses the Filter and Pricing classes to validate the filter,
    create a filter string, and send a request to the Azure Pricing API to
    retrieve pricing information.

    Parameters:
    -----------
        filter (list): A list containing a dictionary with filter values.

    Returns:
    --------
        list: A list of items containing pricing information.

    Raises:
    -------
        Exception: If there is an issue with validating the filter, creating the
                   filter string, sending the request, or processing the response.

    Note:
    -----
        This function is a convenience wrapper that uses the Filter and Pricing
        classes. It validates the filter, creates a filter string, and retrieves
        pricing information from the Azure Pricing API. Any exceptions raised
        during the process are propagated to the caller.
    """
    
    FILTER = Filter()
    try:
        if(FILTER._validate_filter(filter)):    
            FILTER._create_filter_string(filter)
            filter_string = FILTER._create_filter_string(filter)
            PRICING = Pricing(filter_string)
            items = PRICING._send_request()
            return items
        
    except Exception as e:
        raise Exception(str(e))
    
    return []