from none import on_command, CommandSession, permission as perm
from none.message import unescape
import aiocqhttp
import json


@on_command('inform',permission=perm.SUPERUSERS)
async def inform(session: CommandSession):
    group_id = session.get('group_id', prompt='想发通知的群号是？')
    if str(group_id) not in json.loads(session.bot.get_group_list()):
        session.send("你并未加入群组{}".format(group_id))
    # inform_all = session.get('inform_all', prompt='是否at全体？')
    content = session.get('content', prompt='内容是？')
    await session.bot.send_group_msg(roup_id=group_id, message=content)
    session.send('通知已发送')


@inform.args_parser
async def _(session: CommandSession):
    args = session.current_arg_text.trip()
    if session.current_key and len(args) == 1:
        session.args[session.current_key] = args[0]
    elif session.current_key and not len(args) == 1:
        session.get(session.current_key, prompt='参数过多请重新发送')
    elif len(args) == 1:
        key = 'group_id' if isinstance(args[0], int) else 'content'
        session.args[key] = args[0]
    elif len(args) > 1:
        if not args[0].isdigit() and not args[-1].isdigit():
            session.args['content'] = ' '.join(args)
        else:
            id_index = 0 if args[0].isdigit() else len(args)-1
            session.args['group_id'] = args[id_index]
            del(args[id_index])
            session.args['content'] = ' '.join(args)


