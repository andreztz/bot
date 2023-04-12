import asyncio
import re
import socket
import slixmpp

import psutil


COMMAND_REGEX = re.compile(r"^!(\w+)\s*(.*)$")
COMMANDS = {}


def command(name):
    def decorator(func):
        COMMANDS[name] = func
    return decorator

async def is_mpv_running():
    result = await asyncio.to_thread(_check_mpv_running)
    return result


def _check_mpv_running():
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        if proc.info['name'] == 'mpv' and '--player-operation-mode=pseudo-gui' in proc.info['cmdline']:
            return True
    return False


async def async_run(command):
    process = await asyncio.create_subprocess_shell(
        command, 
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    print(stdout.decode(), stderr.decode())


@command("mpv")
async def mpv_command(bot, message, *args, **kwargs):
    is_running = await is_mpv_running()
    if not is_running:
        command = f'mpv --player-operation-mode=pseudo-gui {args[0]}'
        asyncio.create_task(async_run(command))
        bot.send_message(message["from"], "Iniciando")
        return
    else:
        SOCKET_PATH = '/tmp/mpvsocket'

        if args[0] == "fullscreen":
            command = "set fullscreen yes\n"
        else:
            command = "loadfile {}\n".format(args[0])

        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            s.connect(SOCKET_PATH)
            s.sendall(bytes(command, encoding='utf-8'))
            response = s.recv(1024)
        print(response.decode('utf-8'))
        bot.send_message(message["from"], "Executando comando no mpv")


class Bot(slixmpp.ClientXMPP):

    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start_session)
        self.add_event_handler('message', self.message_handler)
        self.commands = COMMANDS

    async def start_session(self, event):
        self.send_presence()
        self.get_roster()

    async def message_handler(self, message):
        if message['type'] in ('chat', 'normal'):
            if match := COMMAND_REGEX.match(message["body"]):
                name = match.group(1)
                args = match.group(2).split()

                func = self.commands[name]

                if func:
                    try:
                        await func(self, message, *args)
                    except Exception as exc:
                        self.send_message(
                            message['from'],
                            f"Erro ao executar o comando '{name}': {exc}"
                        )

    def execute(self, command, args, msg):
        try:
            func = self.commands[command]
            func(self, msg, *args)
        except KeyError:
            self.send_message(msg["from"], "Command not found.")


if __name__ == '__main__':
    import json
    from pathlib import Path
    import logging
    import ssl

    here = Path(__file__).parent

    secrets = here.joinpath("secrets/users.json")
    users = json.loads(secrets.read_text())

    username = users[0]['username']
    password = users[0]['password']

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(levelname)-8s %(message)s'
    )

    bot = Bot(f'{username}@vmbox.lan/python-bot', password)
    bot.register_plugin('xep_0030') # Service Discovery
    bot.register_plugin('xep_0004') # Data Forms
    bot.register_plugin('xep_0060') # PubSub
    bot.register_plugin('xep_0199') # XMPP Ping
    bot.register_plugin('xep_0199') # Ping
    bot.use_tls = True

    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    bot.ssl_context = context
    bot.connect(address=('vmbox.lan', 5222))
    bot.process(forever=True)
