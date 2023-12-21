import os, json
from webchatter import WebChat
import tqdm, tqdm.notebook
# from chattool import load_chats

def process_messages(msgs, checkpoint:str, mode:str="delete", isjupyter:bool=False):
    """Process the messages.
    
    Args:
        msgs (list): The messages.
        checkpoint (str): Store the checkpoint.
        mode (str, optional): One of the three mode: delete, repeat, newchat. Defaults to "delete".

    Returns:
        list: The processed messages.
    """
    offset = 0
    if os.path.exists(checkpoint):
        with open(checkpoint, 'r', encoding='utf-8') as f:
            processed = f.read().strip().split('\n')
        if len(processed) >= 1 and processed[0] != '':
            offset = len(processed)
    tq = tqdm.tqdm if not isjupyter else tqdm.notebook.tqdm
    with open(checkpoint, 'a', encoding='utf-8') as f:    
        for ind in tq(range(offset, len(msgs))):
            msg = msgs[ind]
            chat = WebChat()
            ans = chat.ask(msg, keep=False)
            data = {"index":ind + offset, "chat_log":{"user":msg, "assistant":ans}}
            f.write(json.dumps(data) + '\n')
    return True

def process_chats(chats, checkpoint:str):
    """Process the chats.
    
    Args:
        chats (list): The chats.
        checkpoint (str): Store the checkpoint.

    Returns:
        list: The processed chats.
    """
    # TODO
    return chats