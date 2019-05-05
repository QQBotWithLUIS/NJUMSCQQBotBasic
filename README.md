# NJUMSCQQBotBasic
`基于酷Q和Microsoft LUIS的QQBOT`

`Developed by NJUMSC`



## 运行方式

1. 将GitHub库中的`master`分支Download ZIP到本地，之后解压文件夹，使用`PyCharm`[建议使用的IDE，理论上可以采用其他的IDE或文本编辑器，如Spyder]打开。

2. pip install如下的包[可以采用PyCharm中的`settings`选项来添加第三方库]：

   `nonebot`

   `azure-cognitiveservices-language-luis`

   `msgpack`

   `ujson`

   `xmltodict`

3. 下载`CoolQ`软件 [CoolQ官方下载地址](https://cqp.cc/t/23253#pid873447)。

4. 下载CoolQ插件`HTTP API` [HTTP API下载地址](https://cqp.cc/t/30748) 并且根据网页中的提示进行配置。
5. 进一步`配置CoolQ HTTP API`插件，[具体步骤参考网址](https://none.rclab.tk/guide/getting-started.html)，其中的`配置 CoolQ HTTP API 插件`一节中有较完整的叙述。
6. 打开`CoolQ`，登录账号。
7. 运行`bot.py`。
8. 向你用CoolQ登录的账号发送消息即可。