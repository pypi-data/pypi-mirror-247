# Ref: https://github.com/gngpp/ninja/blob/main/doc/rest.http

import requests
from urllib.parse import urlparse, urlunparse
import os, uuid, json
from typing import Union

def get_account_status(backend_url:str, access_token:str):
    """Get account status from backend-api

    Args:
        backend_url (str): backend url
        access_token (str): access token at https://chat.openai.com/api/auth/session
    
    Returns:
        dict: account status
    
    Rest API:
        ### check account status
        GET http://{{host}}/backend-api/accounts/check
        Authorization: {{bearer_token}}
    """
    url = os.path.join(backend_url, "accounts/check")
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    return response.json()

def get_models(backend_url:str, access_token:str, history_and_training_disabled:bool=False):
    """Get models from backend-api

    Args:
        backend_url (str): backend url
        access_token (str): access token at https://chat.openai.com/api/auth/session
        history_and_training_disabled (bool, optional): history and training disabled. Defaults to False.
    
    Returns:
        dict: models
    
    Rest API:
        ### get models
        GET http://{{host}}/backend-api/models?history_and_training_disabled=false
        Authorization: {{bearer_token}}
    """
    url = os.path.join(backend_url, "models")
    params = {
        "history_and_training_disabled": history_and_training_disabled
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, params=params, headers=headers)
    return response.json()

def get_beta_features(backend_url:str, access_token:str):
    """Get beta features from backend-api

    Args:
        backend_url (str): backend url
        access_token (str): access token at https://chat.openai.com/api/auth/session
    
    Returns:
        dict: beta features
    
    Rest API:
        ### get beta features
        GET http://{{host}}/backend-api/settings/beta_features
        Authorization: {{bearer_token}}
    """
    url = os.path.join(backend_url, "settings/beta_features")
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    return response.json()

## dealing with chat

def get_chat_list( backend_url:str, access_token:str
                 , offset:int=0, limit:Union[int, None]=None, order:str="updated"):
    """Get chat list from backend-api

    Args:
        backend_url (str): backend url
        access_token (str): access token at https://chat.openai.com/api/auth/session
        offset (int, optional): start index. Defaults to 0.
        limit (int, optional): max number of chat. Defaults to 3.
        order (str, optional): order by. Defaults to "updated".
    
    Returns:
        dict: chat list
    
    Rest API:
        ### get conversation list
        GET http://{{host}}/backend-api/conversations?offset=0&limit=3&order=updated
        Authorization: {{bearer_token}}
    """
    url = os.path.join(backend_url, "conversations")
    params = {
        "offset": offset,
        "limit": limit,
        "order": order
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, params=params, headers=headers)
    return response.json()

def get_chat_by_id(backend_url:str, access_token:str, conversation_id:str):
    """Get chat by id from backend-api

    Args:
        backend_url (str): backend url
        access_token (str): access token at https://chat.openai.com/api/auth/session
        conversation_id (str): conversation id
    
    Returns:
        dict: chat
    
    Rest API:
        ### get conversation by id
        GET http://{{host}}/backend-api/conversation/5ae8355a-82a8-4ded-b0e4-ea5dc11b4a9f
        Authorization: {{bearer_token}}
    """
    url = os.path.join(backend_url, "conversation", conversation_id)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    return response.json()

def delete_chat(backend_url:str, access_token:str, conversation_id:str):
    """Delete chat by id

    Args:
        backend_url (str): backend url
        access_token (str): access token at https://chat.openai.com/api/auth/session
        conversation_id (str): conversation id
    
    Returns:
        dict: response
    
    Rest API:
        ### clear conversation by id
        PATCH http://{{host}}/backend-api/conversation/5ae8355a-82a8-4ded-b0e4-ea5dc11b4a9f
        Authorization: {{bearer_token}}
        Content-Type: application/json

        {
            "is_visible": false
        }
    """
    url = os.path.join(backend_url, "conversation", conversation_id)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    data = {
        "is_visible": False
    }
    response = requests.patch(url, headers=headers, data=json.dumps(data))
    return response.json()

def chat_completion( backend_url:str, access_token:str
                   , prompt:str
                   , current_message_id:str
                   , parent_message_id:str
                   , conversation_id:Union[str, None]=None
                   , model:str="text-davinci-002-render-sha"
                   , history_and_training_disabled:bool=False):
    """chat completion(create or edit)

    Args:
        backend_url (str): backend url
        access_token (str): access token at https://chat.openai.com/api/auth/session
        prompt (str): prompt
        current_message_id (str): current message id. You can use uuid.uuid4() to generate one.
        parent_message_id (str): parent message id.
        conversation_id (str, optional): conversation id. Defaults to None.
        model (str, optional): model. Defaults to "text-davinci-002-render-sha".
        history_and_training_disabled (bool, optional): disable history record in the website. Defaults to False.
    
    Returns:
        dict: chat
    
    Rest API:
        ### new conversation
        POST http://{{host}}/backend-api/conversation
        Authorization: {{bearer_token}}
        Content-Type: application/json
        Accept: text/event-stream
    
    {
        "action": "next",
        "messages": [
            {
            "id": "{{$guid}}",
            "author": {
                "role": "user"
            },
            "content": {
                "content_type": "text",
                "parts": [
                "new conversation"
                ]
            },
            "metadata": {}
            }
        ],
        "model": "text-davinci-002-render-sha-mobile",
        "parent_message_id": "{{$guid}}",
        "timezone_offset_min": -480,
        "history_and_training_disabled": false
    }
    """
    url = os.path.join(backend_url, "conversation")
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}',
        'Accept': 'text/event-stream'
    }
    messages = [
        {
            "id": current_message_id,
            "author": {"role": "user"},
            "content": {"content_type": "text", "parts": [prompt]},
        },
    ]
    data = {
        "action": "next",
        "messages": messages,
        "conversation_id": conversation_id,
        "parent_message_id": parent_message_id,
        "model": model,
        "history_and_training_disabled": history_and_training_disabled,
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    resps = response.text.split("data:")
    try:
        first_msg, last_msg = resps[1], resps[-3]
    except:
        raise Exception(f"Request failed with response: {response.text}")
    return json.loads(first_msg), json.loads(last_msg)


def get_share_links(backend_url:str, access_token:str, order:str="created"):
    """Get share links from backend-api

    Args:
        backend_url (str): backend url
        access_token (str): access token at https://chat.openai.com/api/auth/session
        order (str, optional): order by. Defaults to "created".
    
    Returns:
        dict: share links
    
    Rest API:
        ### get share link
        GET http://{{host}}/backend-api/shared_conversations?order=created
        Authorization: {{bearer_token}}
    """
    url = os.path.join(backend_url, "shared_conversations")
    params = {
        "order": order
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, params=params, headers=headers)
    return response.json()

def send_data_to_email(backend_url:str, access_token:str):
    """Send data to email

    Args:
        backend_url (str): backend url
        access_token (str): access token at https://chat.openai.com/api/auth/session
    
    Returns:
        dict: response
    
    Rest API:
        ### export data send to email
        POST http://{{host}}/backend-api/accounts/data_export
        Authorization: {{bearer_token}}
    """
    url = os.path.join(backend_url, "accounts/data_export")
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.post(url, headers=headers)
    return response.json()

def edit_chat_title(backend_url:str, access_token:str, conversation_id:str, title:str):
    """Edit chat title by id

    Args:
        backend_url (str): backend url
        access_token (str): access token at https://chat.openai.com/api/auth/session
        conversation_id (str): conversation id
        title (str): title
    
    Returns:
        dict: response
    
    Rest API:
        ### change conversation title by id
        PATCH http://{{host}}/backend-api/conversation/5ae8355a-82a8-4ded-b0e4-ea5dc11b4a9f
        Authorization: {{bearer_token}}
        Content-Type: application/json

        {
            "title": "New Test"
        }
    """
    url = os.path.join(backend_url, "conversation", conversation_id)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    data = {
        "title": title
    }
    response = requests.patch(url, headers=headers, data=json.dumps(data))
    return response.json()

def generate_chat_title(backend_url:str, access_token:str, conversation_id:str, message_id:str):
    """Generate chat title by id and message id

    Args:
        backend_url (str): backend url
        access_token (str): access token at https://chat.openai.com/api/auth/session
        conversation_id (str): conversation id
        message_id (str): message id
    
    Returns:
        dict: response
    
    Rest API:
        ### generate conversation title
        POST http://{{host}}/backend-api/conversation/gen_title/5ae8355a-82a8-4ded-b0e4-ea5dc11b4a9f
        Authorization: {{bearer_token}}
        Content-Type: application/json

        {
            "message_id": "1646facc-08a6-465f-ba08-58cec1e31ed6"
        }
    """
    url = os.path.join(backend_url, "conversation/gen_title", conversation_id)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    data = {
        "message_id": message_id
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

def get_conversation_limit(base_url:str, access_token:str):
    """Get conversation limit of gpt-4

    Args:
        base_url (str): base url
        access_token (str): access token at https://chat.openai.com/api/auth/session
    
    Returns:
        dict: conversation limit
    
    Rest API:
        ### get conversation limit
        GET http://{{host}}/public-api/conversation_limit
        Authorization: {{bearer_token}}
    """
    url = os.path.join(base_url, "public-api/conversation_limit")
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    return response.json()

## function inheriated from chattool

def is_valid_url(url: str) -> bool:
    """Check if the given URL is valid.

    Args:
        url (str): The URL to be checked.

    Returns:
        bool: True if the URL is valid; otherwise False.
    """
    parsed_url = urlparse(url)
    return all([parsed_url.scheme, parsed_url.netloc])

def normalize_url(url: str) -> str:
    """Normalize the given URL to a canonical form.

    Args:
        url (str): The URL to be normalized.

    Returns:
        str: The normalized URL.

    Examples:
        >>> normalize_url("http://api.example.com")
        'http://api.example.com'

        >>> normalize_url("api.example.com")
        'https://api.example.com'
    """
    url = url.replace("\\", '/') # compat to windows
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        # If no scheme is specified, default to https protocol.
        parsed_url = parsed_url._replace(scheme="https")
    return urlunparse(parsed_url).replace("///", "//")
