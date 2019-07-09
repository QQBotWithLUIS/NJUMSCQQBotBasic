from argparse import *

from nonebot.command import CommandSession


class ParserExit(RuntimeError):
    def __init__(self, status=0, message=None):
        self.status = status
        self.message = message


class ArgumentParser(ArgumentParser):
    """
    An ArgumentParser wrapper that does some customization
    """

    def __init__(self, *args, **kwargs):
        self.session = kwargs.pop('session', None)
        self.prompt = kwargs.pop('prompt', None)
        super().__init__(*args, **kwargs)

    # 防止在stdI/O里输出
    def _print_message(self, *args, **kwargs):
        pass

    def exit(self, status=0, message=None):
        raise ParserExit(status=status, message=message)

    # 去除冗余的信息
    def error(self, message):
        self.exit(2, message)

    def parse_args(self, args=None, namespace=None):
        def finish(msg):
            if self.session and isinstance(self.session, CommandSession):
                self.session.finish(msg)

        if not args:
            finish(self.prompt)
        else:
            try:
                return super().parse_args(args=args, namespace=namespace)
            except ParserExit as e:
                if e.status == 0:  # 如果为 -h/--help
                    finish(super().format_help())
                else:  # 如果格式不正确
                    finish('参数不足或不正确，请使用 -h/--help 参数查询使用帮助。\n详细信息: ' + e.message)
