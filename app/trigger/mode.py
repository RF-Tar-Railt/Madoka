from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain
from loguru import logger

from app.core.config import Config
from app.trigger.trigger import Trigger
from app.util.control import Permission
from app.util.decorator import permission_required


class ChangeMode(Trigger):
    async def process(self):
        config = Config()
        if self.msg[0] == '.mode':
            await self.change_mode()
        if config.ONLINE and config.DEBUG:
            self.as_last = True

    @permission_required(level=Permission.MASTER)
    async def change_mode(self):
        config = Config()
        if config.ONLINE:
            if config.DEBUG:
                await self.do_send(MessageChain.create([
                    Plain('>> 已退出DEBUG模式！\r\n>> 服务端进入工作状态！')
                ]))
                logger.info('>> 已退出DEBUG模式！  >> 服务端进入工作状态！')
            else:
                await self.do_send(MessageChain.create([
                    Plain('>> 已进入DEBUG模式！\r\n>> 服务端进入休眠状态！')
                ]))
                logger.info('>> 已进入DEBUG模式！  >> 服务端进入休眠状态！')
        config.change_debug()
        self.as_last = True
