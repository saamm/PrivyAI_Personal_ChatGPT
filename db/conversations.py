# this file contains core services for managing conversations in the database.
# It allows creating new conversations, adding messages, and retrieving conversations.
# Each conversation is identified by a unique ID and contains a title, messages, and a timestamp of the last interaction.
# The messages are stored as a list of dictionaries, each containing the role (user/assistant), content, and timestamp.
# 

import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, Any

from pymongo import DESCENDING
from db.mongo import get_collection

# here we get the conversations collection from the mongo module
conversations = get_collection("conversations")
# ensure an index on last_interacted for efficient retrieval
conversations.create_index([("last_interacted", DESCENDING)])


# ----- helpers ------ 
# get the current UTC time
def now_utc():
    return datetime.now(timezone.utc)

# generate a new unique conversation ID
def create_new_conversation_id() -> str:
    return str(uuid.uuid4())

# ----- core services -----
# create a new conversation with an optional title and first message
def create_new_conversation(title: Optional[str] = None, role: Optional[str] = None, content: Optional[str] = None) -> str:
    conv_id = create_new_conversation_id()
    ts = now_utc()
    doc = {
        "_id": conv_id,
        "title": title or "Untitled Conversation",
        "messages": [],
        "last_interacted": ts,
    }
    if role and content:
        doc["messages"].append({"role": role, "content": content, "ts": ts})
        # insert_one to add the new conversation document to the collection
    conversations.insert_one(doc)
    # return the unique conversation ID
    return conv_id

# add a message to an existing conversation identified by conv_id
# this part of code pushes a new message to the messages array and updates the last_interacted timestamp
def add_message(conv_id: str, role: str, content: str) -> bool:
    ts = now_utc()
    res = conversations.update_one(
        {"_id": conv_id},
        {
            "$push": {"messages": {"role": role, "content": content, "ts": ts}},
            "$set": {"last_interacted": ts},
        },
    )
    return res.matched_count == 1

# retrieve a conversation by its unique ID and update its last_interacted timestamp
def get_conversation(conv_id: str) -> Optional[Dict[str, Any]]:
    ts = now_utc()
    # find_one_and_update to get the conversation document and update the last_interacted timestamp
    doc = conversations.find_one_and_update(
        {"_id": conv_id},
        {"$set": {"last_interacted": ts}},
        return_document=True,
    )
    return doc

# retrieve all conversations with their IDs and titles, sorted by last_interacted timestamp
def get_all_conversations() -> Dict[str, str]:
    cursor = conversations.find({}, {"title": 1}).sort("last_interacted", DESCENDING)
    return {doc["_id"]: doc["title"] for doc in cursor}



# --- Example usage ---

# For a new conversation (with the first message):
# conv_id = create_new_conversation(title="Intro to Deep Learning", role="user", content="What is DL?")
# add_message(conv_id, "assistant", "Answer for DL query")
# print(get_conversation(conv_id))
# print(get_all_conversations())
#
# # For an existing conversation:
# add_message(conv_id, "user", "What is ML?")
# add_message(conv_id, "assistant", "Answer for ML query")
# print(get_conversation(conv_id))
# print(get_all_conversations())
#
# # # For a new conversation (with a different title and first message):
# conv_id2 = create_new_conversation(title="Intro to Generative AI", role="user", content="What is Generative AI?")
# add_message(conv_id2, "assistant", "Answer for Generative AI query")
# print(get_conversation(conv_id2))
# print(get_all_conversations())