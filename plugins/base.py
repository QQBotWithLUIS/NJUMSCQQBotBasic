from aiocqhttp.exceptions import ActionFailed
from nonebot import *
from nonebot import permission as perm
from nonebot.command.argfilter import extractors, validators, controllers

from function.argparse import ArgumentParser
from function.weather import query_weather

prompt = '若想使用该指令，可输入\'<指令名> -h/--help\'获知用法'
prompt_super = '若想使用该指令，可输入\'<指令名> -h/--help\'获知用法(本指令管理员可用)'


@on_command('天气', only_to_me=True)
async def weather(session: CommandSession):
    info = (session.get_optional('message') or session.current_arg).split(' ')
    try:
        if len(info) == 1:
            await session.finish(query_weather(info[0]))
        else:
            await session.finish(query_weather(info[0], info[1]))
    except CQHttpError:
        await session.finish("非常抱歉，查询失败了呢")


@on_command('私信', only_to_me=True, shell_like=True, permission=perm.PRIVATE_FRIEND)
async def private_msg(session: CommandSession):
    parser = ArgumentParser(session=session,
                            prompt=prompt,
                            usage='私信 [-h] -t <目标QQ号> -m <消息>')
    parser.add_argument('-t', '--to', type=int, help="私信发送对象的QQ号")
    parser.add_argument('-m', '--msg', help='私信内容')
    args = parser.parse_args(session.argv)

    if not args.to:
        to = session.get(
            'to', prompt='想要发私信给谁呢？(请输入发送对象的QQ号)',
            arg_filters=[
                extractors.extract_text,  # 取纯文本部分
                controllers.handle_cancellation(session),
                str.strip,  # 去掉两边空白字符
                # 正则匹配输入格式
                validators.match_regex(r'^\d+', '格式错误，请重新输入')
            ])
    else:
        to = args.to

    if not args.msg:
        msg = session.get(
            'msg', prompt='想发送的消息是什么呢？',
            arg_filters=[
                extractors.extract_text,  # 取纯文本部分
                controllers.handle_cancellation(session),
                str.strip  # 去掉两边空白字符
            ])
    else:
        msg = args.msg

    if not to or not msg:
        await session.finish("参数不足")
    else:
        bot = get_bot()
        try:
            await bot.send_private_msg(user_id=to, message=msg)
            await session.finish("发送成功")
        except ActionFailed:
            await session.finish('发送失败')


@on_command('发送群消息', only_to_me=True, shell_like=True, permission=perm.PRIVATE_FRIEND)
async def group_msg(session: CommandSession):
    parser = ArgumentParser(session=session,
                            prompt=prompt,
                            usage='发送群消息 [-h] -t <目标QQ号> -m <消息>')
    parser.add_argument('-t', '--to', type=int, help='目标群组的QQ号')
    parser.add_argument('-m', '--msg', help='消息内容')
    args = parser.parse_args(session.argv)
    if not args.to:
        to = session.get(
            'to', prompt='想要发送给哪个群呢？(请输入发送对象的QQ号)',
            arg_filters=[
                extractors.extract_text,  # 取纯文本部分
                controllers.handle_cancellation(session),
                str.strip,  # 去掉两边空白字符
                # 正则匹配输入格式
                validators.match_regex(r'^\d+', '格式错误，请重新输入')
            ])
    else:
        to = args.to

    if not args.msg:
        msg = session.get(
            'msg', prompt='想发送的消息是什么呢？',
            arg_filters=[
                extractors.extract_text,  # 取纯文本部分
                controllers.handle_cancellation(session),
                str.strip  # 去掉两边空白字符
            ])
    else:
        msg = args.msg

    if not to or not msg:
        await session.finish("参数不足")
    else:
        bot = get_bot()
        try:
            await bot.send_group_msg(group_id=to, message=msg)
            await session.finish("发送成功")
        except ActionFailed:
            await session.finish('发送失败')


@on_command('获取本号好友列表', only_to_me=True, permission=perm.SUPERUSER)
async def get_friend_list(session: CommandSession):
    bot = get_bot()
    try:
        l = await bot._get_friend_list()
        await session.finish(str(l))
    except ActionFailed as e:
        await session.finish('抱歉，查询失败')


@on_command('获取本号群列表', only_to_me=True, permission=perm.SUPERUSER)
async def get_group_list(session: CommandSession):
    bot = get_bot()
    try:
        l = await bot.get_group_list()
        await session.finish('\n'.join(format_group_list(l)))
    except ActionFailed:
        await session.finish('抱歉，查询失败')


@on_command('获取群资料', only_to_me=True, shell_like=True, permission=perm.SUPERUSER)
async def get_group_info(session: CommandSession):
    parser = ArgumentParser(session=session,
                            prompt=prompt_super,
                            usage='获取群消息 [-h] -t <目标群号> (本指令管理员可用)')
    parser.add_argument('-t', '--target', help='想要获取其资料的群QQ号')
    args = parser.parse_args(session.argv)
    bot = get_bot()
    try:
        info = await bot._get_group_info(group_id=int(args.target))
        await session.finish(format_group_info(info))
    except ActionFailed:
        session.finish('抱歉，查询失败')


@on_command("获取群成员信息", only_to_me=True, shell_like=True, permission=perm.SUPERUSER)
async def get_group_member_info(session: CommandSession):
    parser = ArgumentParser(session=session,
                            prompt=prompt_super,
                            usage='获取群成员信息 [-h] -g <目标群号> -u <目标成员QQ号> (本指令管理员可用)')
    parser.add_argument('-g', '--group_id', type=int, help='目标成员所在的群QQ号')
    parser.add_argument('-u', '--user_id', type=int, help='目标成员的QQ号')
    args = parser.parse_args(session.argv)
    if not args.group_id:
        group_id = session.get(
            'group_id', prompt='目标群组是哪一个呢？(请输入目标群组的QQ号)',
            arg_filters=[
                extractors.extract_text,  # 取纯文本部分
                controllers.handle_cancellation(session),
                str.strip,  # 去掉两边空白字符
                # 正则匹配输入格式
                validators.match_regex(r'^\d+', '格式错误，请重新输入')
            ])
    else:
        group_id = args.group_id

    if not args.user_id:
        user_id = session.get(
            'user_id', prompt='目标成员是哪一位呢(请输入目标成员的QQ号)？',
            arg_filters=[
                extractors.extract_text,  # 取纯文本部分
                controllers.handle_cancellation(session),
                str.strip  # 去掉两边空白字符
            ])
    else:
        user_id = args.user_id

    if not user_id or not group_id:
        await session.finish('参数不足')
    else:
        bot = get_bot()
        try:
            info = await bot.get_group_member_info(user_id=user_id, group_id=group_id)
            await session.finish(str(info))
        except ActionFailed:
            session.finish('抱歉，查询失败')


@on_command("command_help", only_to_me=True, aliases=['帮助', '指令帮助'])
async def get_command_help(session: CommandSession):
    is_superuser = await perm.check_permission(session.bot, session.ctx, perm.SUPERUSER)
    h0 = "本人工智能提供以下可使用的指令:"
    he = " 指令执行过程中可发送'取消'停止执行 "
    h1 = "1. \'私信\' --to/-t <发送对象id> --msg/-m <消息>"
    h2 = "2. \'发送群消息\' --to/-t <发送群组id> --msg/-m <消息>"
    h3 = "3. \'天气\' <城市名> (<县名>)"
    h4 = "4. \'获取本号好友列表\'(不稳定)"
    h5 = "5. \'获取本号群列表\'"
    h6 = "6. \'获取群资料\' --target/-t <目标群组id>"
    h7 = "7. \'获取群成员信息\' --group_id/-g <目标群组号> --user_id/-u <目标成员QQ号>"
    # 根据权限发送相应的帮助信息
    if is_superuser:
        await session.send('\n'.join([h0, h1, h2, h3, h4, h5, h6, h7, he]))
    else:
        await session.send('\n'.join([h0, h1, h2, h3, he]))


# @on_command("test", only_to_me=True)
# async def test_command(session: CommandSession):
#     res = await get_friend_numbers(session.bot)
#     await session.send(str(res))


def format_friend_list(friend_group_list: list):
    res = []


def format_group_list(group_list: list):
    res = list(map(lambda x: '群号: ' + str(x['group_id']) + ', 群名称: ' + str(x['group_name']), group_list))
    return res


def format_group_info(group_info: dict):
    admins = group_info['admins']
    admins_formatted = list(
        map(lambda x: '昵称: ' + x['nickname'] + ', 身份: ' + x['role'] + ', QQ号: ' + str(x['user_id']), admins))

    res = '群号: {}\n群名称: {}\n管理员数目: {}\n管理员: {}\n创建时间: {}(待处理)\n当前成员数: {}\n最大成员数: {}'.format(
        group_info['group_id'], group_info['group_name'], group_info['admin_count'], admins_formatted,
        group_info['create_time'], group_info['member_count'], group_info['max_member_count'])
    return res


# 获取所有群的QQ号
async def get_group_numbers(bot: NoneBot):
    return list(map(lambda x: x['group_id'], await bot.get_group_list()))


# 获取所有好友的QQ号
async def get_friend_numbers(bot: NoneBot):
    group_list = await bot._get_friend_list()
    res = []
    id_group = list(map(lambda g: list(map(lambda i: i['user_id'], g['friends'])), group_list))
    # 懒运算，不使用map的结果不会进行操作，因此使用list来强制进行操作
    list(map(res.extend, id_group))
    return res
