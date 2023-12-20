from enum import Enum


class FastapiConfigKeyEnum(Enum):
    is_json_api = 'is_json_api'
    error404_context_data_func = 'error404_context_data_func'
    error500_context_data_func = 'error500_context_data_func'
    error501_context_data_func = 'error501_context_data_func'
