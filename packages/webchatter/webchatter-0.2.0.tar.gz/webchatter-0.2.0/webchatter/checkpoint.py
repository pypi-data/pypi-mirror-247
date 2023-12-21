import os, json, warnings, time
from webchatter import WebChat
import tqdm, tqdm.notebook
from chattool import load_chats, Chat
from typing import List, Callable
# from chattool import load_chats

def try_sth(func:Callable, max_tries:int, interval:float, *args, **kwargs):
    """Try something.
    
    Args:
        func (Callable): The function to try.
        max_tries (int): The maximum number of tries.
        interval (float): The interval between tries.
    """
    while max_tries:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(e)
            max_tries -= 1
            time.sleep(interval)
    return None

def process_messages( msgs:List[str]
                    , checkpoint:str
                    , interval:int=5
                    , max_tries:int=-1
                    , isjupyter:bool=False
                    ):
    """Process the messages.
    
    Args:
        msgs (list): The messages.
        checkpoint (str): Store the checkpoint.


    Returns:
        list: The processed messages.
    """
    chats = load_chats(checkpoint)
    if len(chats) > len(msgs):
        warnings.warn(f"checkpoint file {checkpoint} has more chats than the data to be processed")
        return chats[:len(msgs)]
    chats.extend([None] * (len(msgs) - len(chats)))
    tq = tqdm.tqdm if not isjupyter else tqdm.notebook.tqdm
    # process chats
    webchat, chat = WebChat(), Chat()
    for ind in tq(range(len(chats))):
        if chats[ind] is not None: continue
        ans = try_sth(webchat.ask, max_tries, interval, msgs[ind])
        chat = Chat(msgs[ind])
        chat.assistant(ans)
        chat.save(checkpoint, mode='a', index=ind)
        chats[ind] = chat
    return chats

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