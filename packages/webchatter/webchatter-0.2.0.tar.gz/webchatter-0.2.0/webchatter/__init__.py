"""Top-level package for WebChatter."""

__author__ = """Rex Wang"""
__email__ = '1073853456@qq.com'
__version__ = '0.2.0'

import os, dotenv, requests
from typing import Union
from . import request
from .webchatter import WebChat, Node
from .checkpoint import process_messages
from pprint import pprint

def load_envs(env:Union[None, str, dict]=None):
    """Read the environment variables for the API call"""
    global access_token, base_url, backend_url
    # update the environment variables
    if isinstance(env, str):
        # load the environment file
        dotenv.load_dotenv(env, override=True)
    elif isinstance(env, dict):
        for key, value in env.items():
            os.environ[key] = value
    # initialize the variables
    ## access token
    access_token = os.getenv("OPENAI_ACCESS_TOKEN")
    ## base url
    base_url = os.getenv("API_REVERSE_PROXY")
    if base_url is not None:
        base_url = request.normalize_url(base_url)
    ## backend url
    backend_url = os.getenv("WEB_REVERSE_PROXY")
    if backend_url is None and base_url is not None:
        backend_url = os.path.join(base_url, "backend-api")
    if backend_url is not None:
        backend_url = request.normalize_url(backend_url)
    return True

def save_envs(env_file:str):
    """Save the environment variables for the API call"""
    global access_token, base_url, backend_url
    with open(env_file, "w") as f:
        f.write(f"OPENAI_ACCESS_TOKEN={access_token}\n")
        f.write(f"API_REVERSE_PROXY={base_url}\n")
        f.write(f"WEB_REVERSE_PROXY={backend_url}\n")
    return True

# load the environment variables
load_envs()

def debug_log( net_url:str="https://www.baidu.com"
             , timeout:int=5
             , message:str="hello world! 你好！"
             , test_response:bool=True):
    """Debug the API call

    Args:
        net_url (str, optional): The url to test the network. Defaults to "https://www.baidu.com".
        timeout (int, optional): The timeout for the network test. Defaults to 5.
        test_usage (bool, optional): Whether to test the usage status. Defaults to True.
        test_response (bool, optional): Whether to test the hello world. Defaults to True.
    
    Returns:
        bool: True if the debug is finished.
    """
    # Network test
    try:
        print("\nChecking your network:")
        requests.get(net_url, timeout=timeout)
        print("Network is available.")
    except:
        print("Warning: Network is not available.")
        return False

    ## Base url
    print("\nCheck your base url:")
    print(base_url)

    ## Backend url
    print("\nCheck your backend url:")
    print(backend_url)

    ## acount status
    print("\nCheck your account status:")
    chat = WebChat()
    pprint(chat.account_status())


    print("\nDebug is finished.")
    return True
