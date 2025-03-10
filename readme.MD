
# Mini fork aiogram

Мелкий форк, изменяющий передачу эвентов в хандлеры и миддлвари. 

!!У вас заранее должен быть установлен Aiogram > 3.15

установка в проект: 
```sh
git clone https://github.com/CheStorrr/mini_fork_aiogram
```

Пример использования: 

```py
from fork import BaseContext, Dispatcher, Router 
from aiogram import Bot, F
import asyncio


class MyContext(BaseContext):
    attr1 = "string"
    attr2 = 123

bot = Bot(token="YOUR_TOKEN")
dp = Dispatcher(context_=MyContext)

@dp.message(F.text)
async def echo(ctx: MyContext):
    print(ctx.attr1) # out: string
    await ctx.reply(ctx.message.text)


async def main():
    await dp.start_polling(bot)

asyncio.run(main())
```


Использование в middleware: 

```py
from fork import BaseContext, Dispatcher
from aiogram import BaseMiddleware

class Service: # Ваш сервис или, возможно, сессия к базе данных
    ...

class MyContext(BaseContext):
    attr1 = "string"
    attr2 = 123
    service: Service


dp = Dispatcher(context_=MyContext)

class Middleware(BaseMiddleware):
    async def __call__(
        self,
        handler,
        event: MyContext,
        data
    ):
        print(ctx.attr1) # out: string
        ctx.service = Service() # Инициализируем ваш сервис
        await handler(event, data)


```
