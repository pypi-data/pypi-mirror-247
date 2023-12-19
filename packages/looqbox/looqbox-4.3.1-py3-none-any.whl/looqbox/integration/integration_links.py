import datetime
import itertools
import json
import logging
import os
import warnings
from functools import partial
from typing import Any

import requests
import sys

from multimethod import multimethod

from looqbox.class_loader.class_loader import ClassLoader
from looqbox.global_calling import GlobalCalling
from looqbox.integration.entity import Entity
from looqbox.integration.looqbox_global import Looqbox
from looqbox.objects.api import ObjQuery
from looqbox.objects.visual.looq_message import ObjMessage
from looqbox.render.abstract_render import BaseRender
from looqbox.render.looqbox.base_looqbox_render import BrowserRender
from looqbox.utils.utils import load_json_from_relative_path
from looqbox.view.response_board import ResponseBoard
from looqbox.view.response_frame import ResponseFrame
from looqbox.view.view_functions import frame_to_board
from looqbox.view.view_functions import response_to_frame
from multipledispatch import dispatch
from looqbox.database.connections.connection_big_query import BigQueryConnection
from looqbox.database.connections.connection_jdbc_query_executor import QueryExecutorJDBCConnection
from looqbox.database.connections.connection_mongo import MongoConnection
from looqbox.database.database_functions import connect, sql_execute

__all__ = ["look_tag", "looq_test_question", "view", "get_sso_attributes", "user_id", "user_group_id", "user_login",
           "question_link", "get_entity", "get_partition", "get_keyword", "_response_json_form"]

# Calling global variable
if GlobalCalling.looq.home is not None:
    GlobalCalling.set_looq_attributes(Looqbox())


def _send_to_dev_link(url, response_board: ResponseBoard, show_json=False, visitor=None):
    """
    Function to test the return from scripts in Looqbox's interface

    :param url: Looqbox's client url
    :param response_board: Board resulting from the script
    :param show_json: Print JSON or not
    :return: A request from an api
    """

    if not visitor:
        visitor = BrowserRender()

    response_json = response_board.to_json_structure(visitor)

    if show_json is True:
        if isinstance(response_json, list) or isinstance(response_json, dict):
            print(json.dumps(response_json, indent=4))
        else:
            print(response_json)

    dev_link_header = build_request_header()

    try:
        link_request = requests.post(url, headers=dev_link_header, data=response_json)
    except requests.ConnectionError:
        logging.error("Page not found -> {0}".format(url))
        sys.exit(1)

    return link_request


def build_request_header() -> dict:
    header = {'x-rstudio-user': 'rstudio', 'Content-Type': 'application/json',
              "x-rstudio-pass": _get_rstudio_password()}

    return header


def _get_rstudio_password() -> str:
    from os import environ

    try:
        rstudio_pass = environ["RSTUDIO_PASS"]
    except:
        rstudio_pass = _get_rstudio_pass_locally()

    return rstudio_pass


def _get_rstudio_pass_locally() -> str:

    configuration_file = load_json_from_relative_path(GlobalCalling.looq.config_file)
    try:
        return configuration_file["RSTUDIO_PASS"]
    except KeyError as error:
        raise Exception(f"Missing RSTUDIO_PASS in local configuration file")

def _safe_get_first(_list):
    """Helper method to get the first element of a list -> defaults to None"""
    return next(iter(_list or []), None)


def _flatten_response(_list):
    """Helper method to flatten a given list or dict"""
    if not isinstance(_safe_get_first(_list), list):
        return _safe_get_first(_list)
    return list(itertools.chain(*_list))


def _get_tag(_tag, _subtag):
    """Get content inside requested entity - defaults to empty list"""
    if isinstance(_tag.get(_subtag), dict):
        return _tag.get(_subtag, {}).get("content")
    return _tag.get(_subtag)


def _extract_with_flattening(element, extract_variable="value"):
    """Extracts value and return the status of the extraction"""
    if isinstance(element, dict):
        element = element.get(extract_variable)
        # If the element is a list containing a single list inside of it, we flatten it
        if not isinstance(element, list):
            return element
        if len(element) == 1 and isinstance(_safe_get_first(element), list):
            return _safe_get_first(element)
        return element
    return element


def _extract(element, extract_variable="value"):
    """Extracts value and return the status of the extraction"""
    if isinstance(element, dict):
        return element.get(extract_variable)
    return element


def _is_list_of_dicts(response_list):
    return isinstance(response_list, list) and isinstance(_safe_get_first(response_list), dict)


def _extract_values(response, to_extract="value"):
    # First we need to ensure that the response is a list
    if not isinstance(response, list):
        return response
    # Secondly, we ensure that every element is a dict
    if any(not isinstance(element, dict) for element in response):
        return response
    # Next we need to verify if it contains one or more elements before extracting it
    list_len = len(response)
    # Let's partially load the extract value functions with the parameter to extract
    flatten_extract = partial(_extract_with_flattening, extract_variable=to_extract)
    extract = partial(_extract, extract_variable=to_extract)
    # If the list has only one element, we should extract it and return it flattened
    if list_len == 1:
        response_list = list(map(extract, response))
        # If the child is a list, we flatten it
        if isinstance(_safe_get_first(response_list), list):
            return list(itertools.chain(*response_list))
        return _safe_get_first(response_list)
    # Else we return extract it and flatten each element as required
    return list(map(flatten_extract, response))


@multimethod
def _new_look_tag(tag: str, par_json: dict, subtag: list, default: Any, only_value: bool):
    if default is None:
        default = [None] * len(subtag)

    if len(subtag) != len(default):
        raise ValueError("Subtag and default must have the same length")
    response = []
    for i in range(len(subtag)):
        result = _new_look_tag(tag, par_json, subtag[i], default[i], only_value)
        response.append(result)

    if not only_value:
        response = _flatten_response(response)
    return response


@multimethod
def _new_look_tag(tag: str, par_json: dict, subtag: str, default: Any, only_value: bool):
    """Function to return the look tag using the new JSON format (Version 2)"""

    # Load extraction options from file
    options_json_path = "configs/tag_extraction_options.json"
    extraction_options_path = os.path.join(os.path.dirname(__file__), options_json_path)
    extract_options = load_json_from_relative_path(extraction_options_path)

    # Pre-filter the given tag - e.g. entities, partitions ...
    _tag = par_json.get(tag, par_json)
    # Find the content inside the requested entity
    response = _get_tag(_tag, subtag)

    # If response is None and default is None, return None
    if response is None:
        return default

    # If requested only value, extract it for each element.
    if only_value and _is_list_of_dicts(response):
        to_extract = extract_options.get(tag, "value")
        response_list = _extract_values(response, to_extract)
        response = response_list

    return response


def _old_look_tag(tag, par_json, default):
    if isinstance(tag, list):
        tags_list = [content for tag_value in tag for content in par_json[tag_value]]
        return tags_list
    return par_json.get(tag, default)


def look_tag(tag, par_json, default=None, only_value=True, _deprecated=True):
    """
    Function to search for a specific tag inside the JSON sent by the parser

    :param tag: Name to be found
    :param par_json: JSON from parser
    :param default: Default value to be returned
    :param only_value: If True return only the value of the tag, if the value is False the function will return all
    the JSON structure link to this tag
    :param _deprecated: If True, will show a warning message
    :return: A JSON structure or a single value
    """

    if _deprecated:
        warnings.warn("look_tag is deprecated, use get_entity instead", DeprecationWarning, stacklevel=2)

    if tag == "$comparative":
        return have_comparative(par_json)
    return _new_look_tag("entities", par_json, tag, default, only_value)


def have_comparative(par_json):
    return "$comparative" in par_json["entities"].keys()


def get_entity(entity, par_json, entity_default=None, only_value=False,
               should_evaluate_date_boundaries = False, as_dict = True,
               as_token = False) -> None|Entity|list[dict]|list[str|int]:
    """
    Function to search for a specific entity inside the JSON sent by the parser

    :param entity: entity to be found
    :param par_json: JSON from parser
    :param entity_default: Default value to be returned
    :param only_value: if True will only return the entity value
    :param should_evaluate_date_boundaries: placeholder for the next version of looqbox package
    :param as_dict: if the entity should be return as a dict
    :param as_token: placeholder for the next version of looqbox package
    :return: A Map structure or a single value
    """

    nlp_values = _new_look_tag("entities", par_json, entity, entity_default, False)

    if nlp_values is None or nlp_values == entity_default:
        return nlp_values

    entities = [Entity(segment= entity_token.get("segment"), text= entity_token.get("text"),
                    value= entity_token.get("value"), name=entity) for entity_token in nlp_values]

    if only_value:
        return [entity_obj.values for entity_obj in entities] if len(entities) > 1 else entities[0].values
    elif as_dict:
        return [entity_obj.to_dict() for entity_obj in entities] if len(entities) > 1 else entities[0].to_dict()
    else:
        return [entity_obj for entity_obj in entities] if len(entities) > 1 else entities[0]


def get_partition(partition, par_json, partition_default=None, only_value=False):
    """
    Function to search for a specific partition inside the JSON sent by the parser

    :param partition: partition to be found
    :param par_json: JSON from parser
    :param partition_default: Default value to be returned
    :param only_value: if True will only return the partition value
    :return: A Map structure or a single value
    """

    return _new_look_tag("partitions", par_json, partition, partition_default, only_value)


def get_keyword(keyword, par_json, keyword_default=None, only_value=False):
    """
    Function to search for a specific keyword inside the JSON sent by the parser

    :param keyword: keyword to be found
    :param par_json: JSON from parser
    :param keyword_default: Default value to be returned
    :param only_value: if True will only return the keyword value
    :return: A Map structure or a single value
    """
    return _new_look_tag("keywords", par_json, keyword, keyword_default, only_value)


def _response_json(parser_json, function_call, second_call=False):
    """
    Function called by the python kernel inside the looqbox server. This function get the return in the main script
    and treat it to return a board to the frontend

    :param parser_json: JSON from parser
    :param function_call: Main function to be called inside the kernel. Default: looq_response
    :return: A ResponseBoard object
    """

    if isinstance(parser_json, str):
        par = json.loads(parser_json)
    else:
        par = parser_json

    user_info = par.get("user", {})
    GlobalCalling.looq.decimal_separator = user_info.get("decSeparator", ",")
    GlobalCalling.looq.date_format = user_info.get("dateFormat", "dd/mm/yyyy")
    GlobalCalling.looq.language = user_info.get("language")
    GlobalCalling.looq.user.login = user_info.get("login")
    GlobalCalling.looq.user.id = user_info.get("id")

    if "$query" in par and par["$query"] and not second_call:

        response = _response_query(par, function_call, second_call, simple=False)
    else:
        response = function_call(par)
        is_board = isinstance(response, ResponseBoard)
        is_frame = isinstance(response, ResponseFrame)
        is_list = isinstance(response, list)

        if not is_frame and not is_board and is_list:
            response = frame_to_board(response)
        elif not is_frame and not is_board:
            looq_object = response_to_frame(response)
            response = frame_to_board(looq_object)
        elif is_frame:
            response = frame_to_board(response)

    device_type = _get_device_type(par)
    app_type = _get_app_type(par)

    visitor = _render_factory(device_type, app_type)

    board_json = response.to_json_structure(visitor)

    return board_json


def _get_device_type(par: dict) -> str:
    device = par.get("deviceType", "desktop").lower()
    return device


def _get_app_type(par: dict) -> str:
    app_type = par.get("appType", "browser").lower()
    return app_type


def _get_feature_flags(par: dict) -> dict:
    feature_flags = par.get("featureFlags", {})
    return feature_flags


def _get_domains(par: dict) -> dict:
    domains = par.get("domains", {})
    return domains


def _get_question(par: dict) -> str:
    question = par.get("question")
    return question


def _render_factory(device_type: str, app_type: str = "") -> BaseRender:
    render_class = {
        "desktop": {
            "browser": "looqbox.render.looqbox.looqbox_desktop_render.DesktopBrowserRender",
            "whatsapp": "looqbox.render.chatbot.whatsapp_render.WhatsAppRender",
            "teams": "looqbox.render.chatbot.teams_render.TeamsRender",
            "chatbot": "looqbox.render.chatbot.base_chatbot_render.BaseChatbotRender"
        },
        "mobile": {
            "browser": "looqbox.render.looqbox.looqbox_mobile_render.MobileBrowserRender",
            "whatsapp": "looqbox.render.chatbot.whatsapp_render.WhatsAppRender",
            "teams": "looqbox.render.chatbot.teams_render.TeamsRender",
            "chatbot": "looqbox.render.chatbot.base_chatbot_render.BaseChatbotRender"
        }
    }

    # Default render is browser
    render_class = render_class.get(device_type.lower(), {}).get(
        app_type.lower(), "looqbox.render.looqbox.looqbox_desktop_render.DesktopBrowserRender"
    )
    class_path, class_name = render_class.rsplit(".", 1)
    return ClassLoader(class_name, class_path).call_class()


def _response_query(par, function_call, second_call, simple=False):
    response_execution_error = False
    # start_time = datetime.datetime.now()
    try:
        response = _response_json(json.dumps(par), function_call, second_call=True)
    except:
        response_execution_error = True
    # total_sql_time = datetime.datetime.now() - start_time

    global_queries = GlobalCalling.looq.query_list.get(GlobalCalling.looq.session_id)
    queries_qt = len(global_queries)

    # If the global hasn't any query save
    if queries_qt == 0:
        message = ObjMessage("No query found in this response")
        response = ResponseFrame([message])
    else:
        response = ResponseFrame(stacked=True)
        # Reversing the list to change the appearing order in the looqbox frame
        global_queries.reverse()
        # For each query we save an objMessage inside a responseFrame
        total_time = _calculate_query_total_time(global_queries)
        response.content.insert(0, ObjQuery(queries=global_queries, total_time=str(total_time)))
        response = ResponseBoard([response])

    return response


def _calculate_query_total_time(global_queries):
    total_time = datetime.timedelta()
    batch_time = [datetime.timedelta()]
    # TODO refactor of total_time calculation
    for query in range(len(global_queries)):
        query_time = datetime.datetime.strptime(global_queries[query].get("time"), "%H:%M:%S.%f").time()
        query_time_delta = datetime.timedelta(
            hours=query_time.hour,
            minutes=query_time.minute,
            seconds=query_time.second,
            microseconds=query_time.microsecond
        )
        if global_queries[query]["mode"] == "single":
            total_time += query_time_delta
        else:
            batch_time.append(query_time_delta)
            if _add_batch_time(global_queries, query):
                total_time += max(batch_time)
                batch_time = [datetime.timedelta()]
    return total_time


def _add_batch_time(global_queries, query):
    return query == len(global_queries) - 1 or (
            query < len(global_queries) - 1 and global_queries[query + 1]["mode"] == "single")


def _check_test_parameter(parameters, par_name):
    """
    Function to check if the parameter_name(par_name) is on the parameter's keys

    :param parameters: Parameters send in looq_test_question
    :param par_name: Desire name to be found in key
    :return: The value of the par_name in parameter or None
    """
    par_return = None

    if hasattr(parameters, par_name):
        par_return = parameters[par_name]

    return par_return


def looq_test_question(test_function=None, parameters=None, show_json=False, user=None, host=None):
    """
    Function to simulate parser parameters. Using this developers can test their scripts using entities.

    :param parameters: Entities and its values
    :param show_json: Show final json or not
    :param user: User that the result will be sent
    :param host: Host that the result will be sent
    """
    # test when the process of response is correct
    if test_function is None:
        raise Exception("Function to be tested not been informed")

    if user is None:
        user = GlobalCalling.looq.user.login

    if host is None:
        host = GlobalCalling.looq.client_host

    if GlobalCalling.looq.test_mode is False:
        return None

    if isinstance(parameters, str):
        parameters = json.loads(parameters)

    GlobalCalling.looq.user_id = _check_test_parameter(parameters, "user_id")
    GlobalCalling.looq.user_group_id = _check_test_parameter(parameters, "user_group_id")
    GlobalCalling.looq.user_login = _check_test_parameter(parameters, "user_login")
    GlobalCalling.looq.feature_flags = _get_feature_flags(parameters)
    GlobalCalling.looq.domains = _get_domains(parameters)
    GlobalCalling.looq.question = _get_question(parameters)
    device_type = _get_device_type(parameters)
    app_type = _get_app_type(parameters)

    visitor = _render_factory(device_type, app_type)

    if "$query" in parameters and parameters["$query"]:
        response = _response_query(parameters, test_function, second_call=False)
    else:
        initial_response_time = datetime.datetime.now()
        response = test_function(parameters)
        total_response_time = datetime.datetime.now() - initial_response_time

    if GlobalCalling.looq.publish_test is None or GlobalCalling.looq.publish_test is True:
        start_post_time = datetime.datetime.now()
        view(response, show_json, user, host, visitor)
        if "$query" in parameters and parameters["$query"]:
            print("Query Published")
        else:
            total_publish_time = datetime.datetime.now() - start_post_time
            print("Response time: " + str(total_response_time))
            print("Publish time: " + str(total_publish_time))
            print("Total time...:" + str(total_publish_time + total_response_time))


def view(looq_object=None, show_json=False, user=GlobalCalling.looq.user.login,
         host=GlobalCalling.looq.client_host, visitor=None):
    if looq_object is None:
        actual_datetime = datetime.datetime.now()

        if looq_object is None:
            looq_object = ObjMessage(text="teste " + str(actual_datetime), type="alert-success")

    is_board = isinstance(looq_object, ResponseBoard)
    is_frame = isinstance(looq_object, ResponseFrame)
    is_list = isinstance(looq_object, list)

    if not is_frame and not is_board and is_list:
        looq_object = frame_to_board(looq_object)
    elif not is_frame and not is_board:
        looq_object = response_to_frame(looq_object)
        looq_object = frame_to_board(looq_object)
    elif is_frame:
        looq_object = frame_to_board(looq_object)
    url = host + "/api/devlink/" + user
    _send_to_dev_link(url, looq_object, show_json, visitor)
    print("looq.view: published for user", user, "in", host)


def _response_json_form(form_json, session_json, looq_process_form):
    """
    Function that will receive a form sent by the front. This function will read the parameters and execute then
    inside the looq_process_form in the other script.
    """

    if isinstance(session_json, str):
        par = json.loads(session_json)
    else:
        par = session_json

    user_info = par.get("user", {})
    GlobalCalling.looq.decimal_separator = user_info.get("decSeparator", ",")
    GlobalCalling.looq.date_format = user_info.get("dateFormat", "dd/mm/yyyy")
    GlobalCalling.looq.language = user_info.get("language")
    GlobalCalling.looq.user.login = user_info.get("login")
    GlobalCalling.looq.user.id = user_info.get("id")

    response = looq_process_form(form_json, session_json)

    is_board = isinstance(response, ResponseBoard)
    is_frame = isinstance(response, ResponseFrame)
    is_list = isinstance(response, list)

    if not is_frame and not is_board and is_list:
        response = frame_to_board(response)
    elif not is_frame and not is_board:
        looq_object = response_to_frame(response)
        response = frame_to_board(looq_object)
    elif is_frame:
        response = frame_to_board(response)

    device_type = _get_device_type(session_json)
    app_type = _get_app_type(session_json)

    visitor = _render_factory(device_type, app_type)

    board_json = response.to_json_structure(visitor)

    return board_json


def get_sso_attributes(par):
    """
    Get the user SSO information from parser

    :return: The JSON of userSsoAttributes in parser return
    """
    sso_attributes = None

    if par is None:
        par = {"apiVersion": 1}

    if "apiVersion" not in par.keys() or par["apiVersion"] is None:
        sso_attributes = par["userSsoAttributes"]

    elif par["apiVersion"] == 1:
        sso_attributes = par["userSsoAttributes"]

    elif par["apiVersion"] >= 2:
        sso_attributes = par["user"]["ssoAttributes"]

    return sso_attributes


def question_link(question, link_text):
    """
    Creates a link to a question.

    :param str question: Question.
    :param str link_text: Text of the link.
    :return: A link string.
    """
    return "<question-link query='" + question + "'>" + link_text + "</question-link>"


def user_id(par: dict = None) -> str:
    """
    Get the user id from options(par is None) or from parser.

    Examples:
    --------
    >>> user_id(par)

    :return: The id string.
    """
    if par is None:
        return GlobalCalling.looq.user.id
    else:
        return par.get('user').get('id')


def user_login(par: dict = None) -> str:
    """
    Get the user login from options(par is None) or from parser.

    Examples:
    --------
    >>> user_login(par)

    :return: The login string.
    """
    if par is None:
        return GlobalCalling.looq.user.login
    else:
        return par.get('user').get('login')


def user_group_id(par: dict = None) -> str:
    """
    Get the user group id from options(par is None) or from parser.

    Examples:
    --------
    >>> user_group_id(par)

    :return: The group id string.
    """
    if par is None:
        return GlobalCalling.looq.user.group
    else:
        return par.get('user').get('groupId')


def _test_connection(connection_name: str) -> str:
    try:
        connection = connect(connection_name)
        execute_test_query(connection)
        is_connection_functional = True
    except Exception as connection_error:
        is_connection_functional = False
        raise connection_error

    return str(is_connection_functional).upper()


@dispatch(QueryExecutorJDBCConnection)
def execute_test_query(connection: QueryExecutorJDBCConnection) -> None:
    test_query = "Select 1"
    sql_execute(connection, test_query)


@dispatch(BigQueryConnection)
def execute_test_query(connection: BigQueryConnection) -> None:
    test_query = "Select 1"
    sql_execute(connection, test_query)


@dispatch(MongoConnection)
def execute_test_query(connection: MongoConnection) -> None:
    test_query = {"collection": "test",
                  "query": {},
                  "fields": {"_id": 1},
                  "limit": 1
                  }
    sql_execute(connection, test_query)
