import sys
from .chat import Chat, AKPool
from arts.moduledb import ModuleDB, File
from arts import openai2


mdb = ModuleDB(openai2, depth=3)['chat_in_cmd']
apikeys: File = mdb['apikeys']['data_1']
apikeys.setdefault('list', [])
record: File = mdb['records']['chat_1']
record.setdefault('messages', [])


def chat_in_cmd(apikeys:list, newchat=False, model='gpt-4', MsgMaxCount=30):
    if model in ('gpt-4',):
        print(f"\n\033[0m您已进入命令行聊天模式, 当前使用'{model}'模型, 请确保您的apikey支持该模型.", end='')
    else:
        print(f"\n\033[0m您已进入命令行聊天模式, 当前使用'{model}'模型.", end='')
    gpt = Chat(api_key=AKPool(apikeys), model=model, MsgMaxCount=MsgMaxCount)
    if not newchat:
        gpt.add_dialogs(*record['messages'])
    while True:
        user = input('\n\n\033[32;1m:')
        print('\033[0m')
        for x in gpt.stream_request(user):
            print(x, end='', flush=True)
        record['messages'] = gpt.fetch_messages()


命令提示 = '''指令集:
openai2 add_apikey <apikey> | 添加1个apikey              | 如需添加多个, 可执行多次
openai2 read_apikeys        | 查看所有apikey             |
openai2 clear_apikeys       | 清除所有apikey             |

openai2 chat                | 继续上次的对话              | 使用 gpt-4 模型
openai2 newchat             | 清空对话记录, 然后开始新对话 | 使用 gpt-4 模型

openai2 chat35              | 继续上次的对话              | 使用 gpt-3.5-turbo 模型
openai2 newchat35           | 清空对话记录, 然后开始新对话 | 使用 gpt-3.5-turbo 模型
'''


def ParseCmd():
    kws = sys.argv[1:]
    if kws:
        kw = kws[0].lower()
        
        # 添加apikey
        if kw in ('add_apikey', 'set_apikey') and len(kws) > 1:
            apikeys['list'].append( kws[1] )
            apikeys.save()
            print('添加 apikey 成功.')

        # 继续上次的对话
        elif kw == 'chat':
            chat_in_cmd(apikeys['list'], newchat=False)
        
        # 清空对话记录, 然后开始新对话
        elif kw == 'newchat':
            chat_in_cmd(apikeys['list'], newchat=True)
        
        # 查看所有apikey
        elif kw in ('read_apikeys', 'read_apikey'):
            for x in apikeys['list']:
                print(x)
        
        # 清除所有apikey
        elif kw == 'clear_apikeys':
            apikeys['list'] = []
            print('已清除所有 apikey .')

        # 继续上次的对话
        elif kw == 'chat35':
            chat_in_cmd(apikeys['list'], newchat=False, model='gpt-3.5-turbo', MsgMaxCount=20)
        
        # 清空对话记录, 然后开始新对话
        elif kw == 'newchat35':
            chat_in_cmd(apikeys['list'], newchat=True, model='gpt-3.5-turbo', MsgMaxCount=20)
        
        else:
            print(命令提示)
    else:
        print(命令提示)