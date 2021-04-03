import logging

from schema import And, Schema

logger = logging.getLogger(__name__)


def is_float(value):
    """Validate if value is float
    Args:
        value(str): Value to validate
    return:
        bool: True in case it is a float
    """
    try:
        float(value)
    except ValueError:
        return False
    else:
        return True


# Schema for reponse in case for str input
conf_schema_response_str = Schema(
    {
        'original': str,
        'content': str,
        'depth': int,
        'time_execution': And(str, lambda s: is_float(s))
    }
)


# Schema for reponse in case for list input
conf_schema_response_list = Schema(
    {
        'original': list,
        'content': list,
        'depth': int,
        'time_execution': And(str, lambda s: is_float(s))
    }
)
