from aiogram.filters import BaseFilter 
from typing import Optional, Type
from .base_context import BaseContext

class Text(BaseFilter):
    def __init__(
        self, 
        text: Optional[str], 
        list_: Optional[list[str]] = None,
        in_: Optional[bool] = False,
        lower: bool = True,
        split: Optional[int] = None
    ):
        super().__init__()
        self.text = text
        self.list = list_
        self.in_ = in_ 
        self.lower = lower
        self.split = split 

    async def __call__(
        self,
        ctx: BaseContext
    ) -> bool:
        print('called filter')
        if not ctx.message: 
            print('not message')
            return False
        
        if not ctx.message.text:
            print('not message text')
            return False 
        
        text = ctx.message.text
        print('message text:', text)

        if self.lower:
            text = text.lower()
        
        if self.list:
            return text in self.list
        
        if self.in_:
            return self.text in text 
        
        if self.split:
            return text.split()[self.split] == text
        
        if self.text:
            return self.text == text
        
        return True

class F:
    
    text = Text