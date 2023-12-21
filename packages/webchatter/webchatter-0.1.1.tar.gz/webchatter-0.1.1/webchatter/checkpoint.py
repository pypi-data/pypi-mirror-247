import os, json
from webchatter import WebChat
import tqdm, tqdm.notebook
import time
# from chattool import load_chats

def process_messages( msgs
                    , checkpoint:str
                    , time_interval:int=5
                    , max_tries:int=-1
                    , isjupyter:bool=False
                    , interval_rate:float=1
                    ):
    """Process the messages.
    
    Args:
        msgs (list): The messages.
        checkpoint (str): Store the checkpoint.

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
    chat = WebChat()
    with open(checkpoint, 'a', encoding='utf-8') as f:
        for ind in tq(range(offset, len(msgs))):
            wait_time = time_interval
            while max_tries:
                try:
                    msg = msgs[ind]
                    ans = chat.ask(msg, keep=False)
                    data = {"index":ind + offset, "chat_log":{"user":msg, "assistant":ans}}
                    f.write(json.dumps(data) + '\n')
                    break
                except Exception as e:
                    print(ind, e)
                    max_tries -= 1
                    time.sleep(wait_time)
                    wait_time = wait_time * interval_rate
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