from aiogram import Dispatcher, Router
from aiogram.dispatcher.event.telegram import TelegramEventObserver
from aiogram.dispatcher.middlewares.manager import MiddlewareManager
from aiogram.fsm.strategy import FSMStrategy
from aiogram.dispatcher.event.bases import UNHANDLED
from .base_context import BaseContext 
from typing import Type
import functools


class MiddlewareManagaer(MiddlewareManager):

    def __init__(self, event_type: str):
        super().__init__()
        self.event_type = event_type

    @staticmethod
    def wrap_middlewares(
        middlewares, handler, event_name: str, context: type[BaseContext]
    ):
        
        @functools.wraps(handler)
        def handler_wrapper(event, kwargs):
            base_context = None 

            try:
                event.text

                base_context: Type[BaseContext] = context(
                    event=event,
                    data=kwargs,
                    event_name=event_name
                )
                base_context.set_bot(kwargs['bot'])
            except:
                base_context = event 

            return handler(base_context, **kwargs)

        middleware = handler_wrapper
        for m in reversed(middlewares):
            middleware = functools.partial(m, middleware)  # type: ignore[assignment]
        return middleware

class TelegramEventObserverr(TelegramEventObserver):

    def __init__(self, router, event_name, context):
        super().__init__(router, event_name)
        self.context = context
        self.middleware = MiddlewareManagaer(event_type=event_name)
        

    async def trigger(self, event, **kwargs):
        for handler in self.handlers:
            kwargs["handler"] = handler
            result, data = await handler.check(event, **kwargs)
            if result:
                kwargs.update(data)
                try:
                    wrapped_inner = self.outer_middleware.wrap_middlewares(
                        self._resolve_middlewares(),
                        handler.call,
                    )
                    return await wrapped_inner(event, kwargs)
                except Exception as e:
                    print(str(e))
                    continue

        return UNHANDLED
    
    def wrap_outer_middleware(
        self, callback, event, data
    ):
        wrapped_outer = self.middleware.wrap_middlewares(
            self.outer_middleware,
            callback,
            self.event_name,
            self.context
        )
        return wrapped_outer(event, data)
    
    def __call__(self, *filters, flags = None, **kwargs):
        result = super().__call__(*filters, flags=flags, **kwargs)
        return result
    
    def register(self, callback, *filters, flags = None, **kwargs):
        callback = super().register(callback, *filters, flags=flags, **kwargs)


class Router(Router):
    def __init__(self, *, context_: Type[BaseContext] = None, name = None, ):
        super().__init__(name=name)
        self.message = self.observers['message'] = TelegramEventObserverr(router=self, event_name='message', context=context_)



class Dispatcher(Dispatcher):

    def __init__(self, *, storage = None, fsm_strategy = FSMStrategy.USER_IN_CHAT, events_isolation = None, disable_fsm = False, name = None, context_: Type[BaseContext] = BaseContext, **kwargs):
        super().__init__(storage=storage, fsm_strategy=fsm_strategy, events_isolation=events_isolation, disable_fsm=disable_fsm, name=name, **kwargs)
        self.message = self.observers['message'] = TelegramEventObserverr(router=self, event_name='message', context=context_)

