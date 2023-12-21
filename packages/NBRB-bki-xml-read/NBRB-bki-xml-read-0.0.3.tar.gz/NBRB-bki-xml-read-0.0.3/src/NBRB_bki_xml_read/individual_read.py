'''
Functions that allows to read information for 
individual client.
'''

from NBRB_bki_xml_read.common_tools import dict_reading_decorator, sub_dict_reader

@dict_reading_decorator
def read_client(client_dict, keys_separator="/"):
    '''
    Read bki information starting from the "client" field.
    
    Arguments
    -----------
        client_dict :    (dict) dictionary which can be created
                         from infromation between <client> tag
                         of bki.xml
        keys_separator : (str) describe symbols that will separate keys
                         of input dictionaries in the result dictionary.
    Returns
    ----------
        (dict) flat dictionary that contains 
        infromation between <clint> tag from bki.xml. 
    '''
    res = {
        "client" + keys_separator + key:val
        for field_name in [
            "titul",
            "registrationplace",
            "range",
            "scoring",
            "RequestNumber7Days",
            "RequestNumber30Days"
        ]
        for key, val in sub_dict_reader(
            client_dict, field_name,
            keys_separator = keys_separator
        ).items()
    }

    # requestnumber is only field in clint info
    # that can be displayed as just number
    if ("requestnumber" in client_dict):
        res[f"client{keys_separator}requestnumber"] =\
            client_dict["requestnumber"]
    
    return res

@dict_reading_decorator
def read_result(result_dict, keys_separator="/"):
    '''
    Read the response from bki starting from the "result" field.

    Arguments
    -----------
        result_dict :    (dict) dictionary which can be created
                         from infromation between <result> tag
                         of bki.xml
        keys_separator : (str) describe symbols that will separate keys
                         of input dictionaries in the result dictionary.
    Returns
    ----------
        (dict) flat dictionary that contains 
        infromation between <result> tag from bki.xml. 
    '''
    
    res = {
        **sub_dict_reader(
            result_dict, "completecode", 
            keys_separator = keys_separator
        ),
        **(
            read_client(result_dict["client"], keys_separator = keys_separator)
            if "client" in result_dict.keys() else {}
        )
    }

    return {"result" + keys_separator + key:val for key, val in res.items()}