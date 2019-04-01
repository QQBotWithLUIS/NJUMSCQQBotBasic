from nonebot import *
from nonebot import permission as perm
from nonebot.argparse import ArgumentParser
from nonebot.command.argfilter import extractors, validators, controllers
from nonebot.message import unescape

from function.weather import query_weather


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


@on_command('天气', only_to_me=False)
async def weather(session: CommandSession):
    info = (session.get_optional('message') or session.current_arg).split(' ')
    try:
        if len(info) == 1:
            await session.send(query_weather(info[0]))
        else:
            await session.send(query_weather(info[0], info[1]))
    except Exception as e:
        await session.send("非常抱歉，查询失败了呢")


@on_command('私信', only_to_me=True, shell_like=True)
async def private_msg(session: CommandSession):
    parser = ArgumentParser(session=session)
    parser.add_argument('-T', '--to', default=None)
    parser.add_argument('-M', '--msg', default=None)
    args = parser.parse_args(session.argv)
    # if not args.to:
    #     to = session.get(
    #         'to', '想要发送给谁呢？(请输入发送对象的QQ号)',
    #         arg_filters=[
    #             extractors.extract_text,  # 取纯文本部分
    #             controllers.handle_cancellation(session),
    #             str.strip,  # 去掉两边空白字符
    #             # 正则匹配输入格式
    #             validators.match_regex(r'^\d+', '格式错误，请重新输入')
    #         ])
    # else:
    #     to = args.to
    #
    # if not args.msg:
    #     msg = session.get(
    #         'msg', '想发送的消息是什么呢？',
    #         arg_filters=[
    #             extractors.extract_text,  # 取纯文本部分
    #             controllers.handle_cancellation(session),
    #             str.strip  # 去掉两边空白字符
    #         ])
    # else:
    #     msg = args.msg

    if not args.to or not args.msg:
        await session.send("参数不足")
    else:
        bot = get_bot()
        await bot.send_private_msg(user_id=int(args.to), message=args.msg)
        await session.send("发送成功")


@on_command('发送群消息', only_to_me=True, shell_like=True)
async def group_msg(session: CommandSession):
    parser = ArgumentParser(session=session)
    parser.add_argument('-T', '--to')
    parser.add_argument('-M', '--msg')
    args = parser.parse_args(session.argv)
    # if not args.to:
    #     to = session.get(
    #         'to', '想要发送给哪个群呢？(请输入发送对象的QQ号)',
    #         arg_filters=[
    #             extractors.extract_text,  # 取纯文本部分
    #             controllers.handle_cancellation(session),
    #             str.strip,  # 去掉两边空白字符
    #             # 正则匹配输入格式
    #             validators.match_regex(r'^\d+', '格式错误，请重新输入')
    #         ])
    # else:
    #     to = args.to
    #
    # if not args.msg:
    #     msg = session.get(
    #         'msg', '想发送的消息是什么呢？',
    #         arg_filters=[
    #             extractors.extract_text,  # 取纯文本部分
    #             controllers.handle_cancellation(session),
    #             str.strip  # 去掉两边空白字符
    #         ])
    # else:
    #     msg = args.msg

    if not args.to or not args.msg:
        await session.send("参数不足")
    else:
        bot = get_bot()
        await bot.send_group_msg(group_id=int(args.to), message=args.msg)
        await session.send("发送成功")


@on_command('获取好友列表', only_to_me=True, permission=perm.SUPERUSER)
async def get_friend_list(session: CommandSession):
    bot = get_bot()
    info = await bot._get_friend_list()
    await session.send(str(info))


@on_command('获取群信息', only_to_me=True, shell_like=True, permission=perm.SUPERUSER)
async def get_group_info(session: CommandSession):
    parser = ArgumentParser(session=session)
    parser.add_argument('-T', '--target')
    args = parser.parse_args(session.argv)
    bot = get_bot()
    if not args.target:
        await session.send("参数不足")
    else:
        info = await bot._get_group_info(group_id=int(args.target))
        await session.send(str(info))
    # else:


#     await session.send("未指定群号")


@on_command("获取群成员信息", only_to_me=True, shell_like=True, permission=perm.SUPERUSER)
async def get_group_member_info(session: CommandSession):
    parser = ArgumentParser(session=session)
    parser.add_argument('-G', '--group_id')
    parser.add_argument('-U', '--user_id')
    args = parser.parse_args(session.argv)
    if not args.user_id or not args.group_id:
        await session.send('参数不足')
    else:
        bot = get_bot()
        info = await bot.get_group_member_info(user_id=int(args.user_id), group_id=int(args.group_id))
        await session.send(str(info))


@on_command("command_help", only_to_me=True)
async def get_command_help(session: CommandSession):
    h1 = "\'私信\' --to/-T [发送对象id] --msg/-M [消息]"
    h2 = "\'发送群消息\' --to/-T [发送群组id] --msg/-M [消息]"
    h3 = "\'获取好友列表\'"
    h4 = "\'获取群信息\' --target/-T [目标群组id]"
    h5 = "\'获取群成员信息\' --group_id/-G [群组id] --user_id/-U [目标id]"
    h6 = "\'天气\' [城市名] ([县名])"
    await session.send('\n'.join([h1, h2, h3, h4, h5, h6]))
