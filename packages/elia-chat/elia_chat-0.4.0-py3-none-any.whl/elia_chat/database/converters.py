from datetime import datetime

from langchain.schema import BaseMessage, SystemMessage, AIMessage, HumanMessage

from elia_chat.database.models import ChatDao, MessageDao
from elia_chat.models import ChatData


def chat_data_to_chat_dao(chat_data: ChatData) -> ChatDao:
    return ChatDao(
        model=chat_data.model_name,
        started_at=datetime.fromtimestamp(chat_data.create_timestamp or 0),
    )


def chat_message_to_message_dao(chat_message: BaseMessage) -> MessageDao:
    return MessageDao(
        role=chat_message.type,
        content=chat_message.content,
        timestamp=datetime.fromtimestamp(
            chat_message.additional_kwargs.get("timestamp", 0)
        ),
        status=chat_message.additional_kwargs.get("status"),
        end_turn=chat_message.additional_kwargs.get("end_turn"),
        weight=chat_message.additional_kwargs.get("weight"),
        meta=chat_message.additional_kwargs.get("metadata"),
        recipient=chat_message.additional_kwargs.get("recipient"),
    )


def chat_dao_to_chat_data(chat_dao: ChatDao) -> ChatData:
    return ChatData(
        id=str(chat_dao.id),
        title=chat_dao.title,
        model_name=chat_dao.model,
        create_timestamp=chat_dao.started_at.timestamp()
        if chat_dao.started_at
        else None,
        messages=[
            message_dao_to_chat_message(message) for message in chat_dao.messages
        ],
    )


def message_dao_to_chat_message(message_dao: MessageDao) -> BaseMessage:
    ts = message_dao.timestamp.timestamp() if message_dao.timestamp else 0
    kwargs = {
        "content": message_dao.content,
        "additional_kwargs": {
            "timestamp": ts,
            "status": message_dao.status,
            "end_turn": message_dao.end_turn,
            "weight": message_dao.weight,
            "metadata": message_dao.meta,
            "recipient": message_dao.recipient,
        },
    }
    if message_dao.role == "system":
        return SystemMessage(**kwargs)
    elif message_dao.role == "ai":
        return AIMessage(**kwargs)
    elif message_dao.role == "human":
        return HumanMessage(**kwargs)
    else:
        raise ValueError(f"Invalid role {message_dao.role!r}")
