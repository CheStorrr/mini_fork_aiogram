from aiogram.types import TelegramObject, Message
from typing import Type, Dict, Any
from aiogram import Bot
from dataclasses import dataclass
from enum import Enum 

class EventType(Enum):
    MESSAGE = 'message'
    CALLBACK = 'callback'
    INLINE = 'inline'

@dataclass
class BaseContext:

    def __init__(
        self,
        event: TelegramObject,
        data: Dict[str, Any],
        event_name: str='message',
        **kw
    ):
        self.event = event
        self.data = data 
        self.event_name = event_name

    def set_bot(self, bot: Bot):
        self.bot = bot

    async def reply(self, text: str) -> Message:
        event: Message = self.event
        if EventType(self.event_name) == EventType.MESSAGE:
            return await event.reply(text=text)
        raise
        
    async def answer(self, text: str) -> Message:
        event: Message = self.event 
        if EventType(self.event_name) == EventType.MESSAGE:
            return await event.answer(text=text)

    @property 
    def message(self) -> Message:

        if EventType(self.event_name) == EventType.MESSAGE:
            return self.event 
        
        return None 
    
    @property
    def callback(self):

        if EventType(self.event_name) == EventType.CALLBACK:
            return self.event 
        
        return None 
    
    @property 
    def inline(self):

        if EventType(self.event_name) == EventType.INLINE:
            return self.event 
        
        return None 
    

    def __call__(self, *args, **kwargs):
        return self.__init__(*args, **kwargs)