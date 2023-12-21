"""Main module."""

from typing import Union
import os, uuid, json
import webchatter
from .request import (
    get_account_status, get_models, get_beta_features,
    get_chat_list, get_chat_by_id, 
    chat_completion, delete_chat,
)

class Node():
    def __init__(self, node:dict, name:str="", depth:int=0):
        """Initialize the class.
        
        Args:
            node (dict): The node.
        """
        self._node = self.simplify(node)
        self._message, self._parent, self._children, self._node_id = (
            self.node['message'], self.node['parent'], self.node['children'], self.node['id'])
        self.name, self.depth = name, depth
    
    @property
    def node(self):
        """Get the node."""
        return self._node
    
    @property
    def message(self):
        """Get the message."""
        return self._message
    
    @property
    def parent(self):
        """Get the parent."""
        return self._parent
    
    @property
    def children(self):
        """Get the children."""
        return self._children
    
    @property
    def node_id(self):
        """Get the node id."""
        return self._node_id
    
    @staticmethod
    def simplify(node:dict):
        """Simplify the node."""
        # message
        msg = node.get("message")
        if isinstance(msg, dict): msg = msg['content']['parts'][0]
        # parent id
        parent = node.get('parent')
        # children id
        children = node.get("children")
        if not children:children = []
        # node id
        node_id = node.get("id") or node['message']['id']
        return {
            "id": node_id,
            "message": msg,
            "parent": parent,
            "children": children}
    
    def __repr__(self):
        """Representation."""
        children = [child[:8] for child in self.children]
        parent = self.parent[:8] if self.parent else "tree"
        name = self.name + "-" if self.name else ""
        return f"<Node: {name}{parent} -|- {children}"
    
    def __str__(self):
        """String."""
        return self.__repr__()
    
    def __eq__(self, other):
        """Equal."""
        return self.node == other.node

class WebChat():
    """WebChat class."""
    def __init__( self
                , base_url: Union[str, None] = None
                , backend_url: Union[str, None] = None
                , access_token: Union[str, None] = None
                , chat_id: Union[str, None] = None
                , node_id: Union[str, None] = None):
        """Initialize the class.

        Args:
            base_url (Union[str, None], optional): The base url for the API. Defaults to None.
            backend_url (Union[str, None], optional): The backend url for the API. Defaults to None.
            access_token (Union[str, None], optional): The access token for the API. Defaults to None.
            chat_id (Union[str, None], optional): The conversation id for the API. Defaults to None.
            node_id (Union[str, None], optional): The parrent message id for the API. Defaults to None.
        """
        self._base_url = base_url or webchatter.base_url
        self._access_token = access_token or webchatter.access_token
        self.backend_url = backend_url or webchatter.backend_url or os.path.join(self.base_url, "backend-api")
        assert self.backend_url is not None, "The backend url and base url are not set!"
        assert self.access_token is not None, "The access token is not set!"
        self._chat_id = chat_id
        # Tree structure
        self._node_id = node_id # the answer node
        if chat_id is not None:
            self._init_chat(chat_id, node_id)
        else:
            self._root_id, self._tree_id, self._que_id = None, None, None
            self._mapping = {}
    
    @property
    def chat_log(self):
        """Get the chat log."""
        node_id, mapping = self.node_id, self.mapping
        chat_log = []
        while node_id is not None:
            chat_log.append(mapping[node_id].message)
            node_id = mapping[node_id].parent
        # remove the root node and tree node
        chat_log = chat_log[-3::-1]
        chat_log_with_role = []
        for ind, log in enumerate(chat_log):
            if ind % 2 == 0:
                chat_log_with_role.append({"role": "user", "content":log})
            else:
                chat_log_with_role.append({"role": "assistant", "content":log})
        return chat_log_with_role
        
    def account_status(self):
        """Get the account status."""
        url, token = self.backend_url, self.access_token
        try:
            resp = get_account_status(url, token)
            return resp['account_plan']
        except:
            raise Exception(f"Request failed with response: {resp}")
    
    def valid_models(self):
        """Get the models."""
        url, token = self.backend_url, self.access_token
        try:
            resp = get_models(url, token)
        except:
            raise Exception(f"Request failed with response: {resp}")
        return [model['category'] for model in resp["categories"]]
    
    def beta_features(self):
        """Get the beta features."""
        url, token = self.backend_url, self.access_token
        return get_beta_features(url, token)
    
    def chat_list(self, offset:int=0, limit:int=3, order:str="updated"):
        """Get the chat list."""
        url, token = self.backend_url, self.access_token
        resp = get_chat_list(url, token, offset=offset, limit=limit, order=order)
        try:
            return [{'conversation_id':item['id'],'title': item['title']} for item in resp['items']]
        except:
            raise Exception(f"Request failed with response: {resp}")
    
    def num_of_chats(self):
        """Get the number of chats."""
        url, token = self.backend_url, self.access_token
        resp = get_chat_list(url, token, limit=1)
        try:
            return resp['total']
        except:
            raise Exception(f"Request failed with response: {resp}")
    
    def ask( self, message:str
           , keep:bool=True):
        """Continue the chat."""
        url, token = self.backend_url, self.access_token
        # first call: create a conversation
        if self.chat_id is None:
            # create four nodes
            tree_id, que_id = str(uuid.uuid4()), str(uuid.uuid4())
            root_resp, ans_resp = chat_completion(url, token, message, que_id, tree_id
                                                 , history_and_training_disabled=not keep)
            if not keep: return Node(ans_resp).message
            # update parent and children for these nodes
            root_resp['children'], root_resp['parent'] = [que_id], tree_id
            ans_resp['children'], ans_resp['parent'] = [], que_id
            root_node = Node(root_resp, name="root")
            tree_node = Node({
                "id": tree_id, "message": None,
                "children": [root_node.node_id], "parent":None})
            ans_node = Node(ans_resp, name="A1")
            que_node = Node({
                "id": que_id, "message": message,
                "children": [ans_node.node_id], "parent": root_node.node_id}
                , name="Q1")
            # update conversation id
            self._chat_id = ans_resp['conversation_id']
            # update mapping and tree ids
            self._tree_id, self._root_id = tree_id, root_node.node_id
            self._node_id, self._que_id = ans_node.node_id, que_node.node_id
            self._mapping = {
                tree_id: tree_node, root_node.node_id: root_node,
                ans_node.node_id: ans_node, que_node.node_id: que_node}
        else: # update ans_node and que_node
            que_id, pre_ans_id = str(uuid.uuid4()), self.node_id
            _, ans_resp = chat_completion(url, token, message, que_id, pre_ans_id, self.chat_id)
            ans_resp['parent'] = que_id
            ans_node = Node(ans_resp)
            ans_id = ans_node.node_id
            que_node = Node({
                "id": que_id, "message": message,
                "children": [ans_id], "parent": pre_ans_id})
            # add children to the previous node
            self._mapping[pre_ans_id].children.append(que_id)
            # update node id and que id
            self._node_id, self._que_id = ans_id, que_id
            # update mapping
            self._mapping[ans_id], self._mapping[que_id] = ans_node, que_node
        # return the answer
        return ans_node.message

    def mapping_by_id(self, chat_id:Union[str, None]=None):
        """Get the mapping by id."""
        url, token = self.backend_url, self.access_token
        chat_id = chat_id or self.chat_id
        assert chat_id is not None, "The chat id is not set!"
        resp = get_chat_by_id(url, token, chat_id)
        try:
            return {key: Node(node) for key, node in resp['mapping'].items()}
        except:
            raise Exception(f"Request failed with response: {resp}")
    
    def chat_by_id(self, chat_id:str, node_id:Union[str, None]=None):
        """Get the chat by id."""
        chat = WebChat(self.base_url, self.backend_url, self.access_token)
        chat._init_chat(chat_id, node_id)
        return chat
    
    def _init_chat(self, chat_id:str, node_id:Union[str, None]=None):
        """Initialize the chat."""
        url, token = self.backend_url, self.access_token
        resp = get_chat_by_id(url, token, chat_id)
        try:
            if node_id is None: node_id = resp['current_node']
            mapping = {}
            for key, val in resp['mapping'].items():
                node = Node(val)
                mapping[key] = node
                if node.parent is None: tree_id = key
                if node_id in node.children: que_id = key
            root_id = mapping[tree_id].children[0]
            self._root_id, self._tree_id = root_id, tree_id
            self._que_id, self._node_id = que_id, node_id
            self._mapping = mapping
        except:
            raise Exception(f"Request failed with response: {resp}")

    def regenerate(self, message:Union[str, None]=None):
        """Regenerate the chat."""
        # TODO
    
    def goback(self):
        """Go back to the parrent node."""
        # TODO
    
    def goto(self, node_id:str):
        """Go to the parrent node."""
        # TODO

    def save( self, file:str
            , mode:str='a'
            , index:int=0
            , chat_log_only:bool=True
            , store_mapping:bool=False
            , ):
        """Save the chat."""
        assert mode in ['a', 'w'], "saving mode should be 'a' or 'w'"
        # make path if not exists
        pathname = os.path.dirname(file).strip()
        if pathname != '': os.makedirs(pathname, exist_ok=True)
        
        if chat_log_only:
            data = {
                "index": index,
                "chat_log": self.chat_log,
            }
        else:
            data = {
                "index": index,
                "chat_id": self.chat_id,
                "node_id": self.node_id,
                "access_token_hash": hash(self.access_token),
                "mapping": self.mapping if store_mapping else None,
                "chat_log": self.chat_log,
            }
        with open(file, mode, encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False) + '\n')
        return
    
    def load(self, path:str, check_mapping:bool=False):
        """Load the chat."""
        with open(path, 'r', encoding='utf-8') as f:
            data = json.loads(f.read())
        chat_id, node_id = data.get('chat_id'), data.get('node_id')
        assert chat_id is not None, "The chat id is not set!"
        # TODO: support more modes
        return self.chat_by_id(chat_id, node_id)
    
    def print_log(self):
        """Print the chat log."""
        sep = '\n' + '-'*15 + '\n'
        for item in self.chat_log:
            print(f"{sep}{item['role']}{sep}{item['content']}\n")
        return True
    
    def __repr__(self):
        """Representation."""
        return "<WebChat: {}>".format(self.chat_id or "None")
    
    def __str__(self):
        """String."""
        return self.__repr__()

    @property
    def base_url(self):
        """Get the base url."""
        return self._base_url
    
    @base_url.setter
    def base_url(self, new_url:str):
        """Set the base url."""
        self.backend_url = os.path.join(new_url, "backend-api")

    @property
    def access_token(self):
        """Get the access token."""
        return self._access_token
    
    @access_token.setter
    def access_token(self, _):
        """Set the access token."""
        raise AttributeError("The access token cannot be changed. Try to create another chat instead.")
    
    @property
    def chat_id(self):
        """Get the conversation id."""
        return self._chat_id
    
    @chat_id.setter
    def chat_id(self, _):
        """Set the conversation id."""
        raise AttributeError("The conversation id cannot be changed. Try to create another chat instead.")
    
    @property
    def node_id(self):
        """Get the node id."""
        return self._node_id
    
    @node_id.setter
    def node_id(self, _:str):
        """Set the node id."""
        raise AttributeError("The node id cannot be changed. Please use `self.goto` instead.")
    
    @property
    def root_id(self):
        """Get the root id."""
        return self._root_id
    
    @property
    def tree_id(self):
        """Get the tree id."""
        return self._tree_id

    @property
    def mapping(self):
        """Get the mapping."""
        return self._mapping