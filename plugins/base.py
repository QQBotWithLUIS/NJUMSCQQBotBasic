from none import on_command, CommandSession, permission as perm
from none.message import unescape


@on_command('echo', only_to_me=False)
async def echo(session: CommandSession):
    await session.send(session.get_optional('message') or session.current_arg)


@on_command('say', permission=perm.SUPERUSER)
async def _(session: CommandSession):
    await session.send(
        unescape(session.get_optional('message') or session.current_arg))


@on_command('inform', permission=perm.SUPERUSER)
async def inform(session: CommandSession):
    await session.send(session.get_optional('message') or session.current_arg)

