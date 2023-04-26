import re
from slixmpp.clientxmpp import ClientXMPP
from commands import COMMANDS

COMMAND_REGEX = re.compile(r"^!(\w+)\s*(.*)$")


class Bot(ClientXMPP):

    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.add_event_handler("session_start", self.start_session)
        self.add_event_handler("message", self.message_handler)
        self.commands = COMMANDS

    async def start_session(self, event):
        self.send_presence()
        self.get_roster()

    async def message_handler(self, message):
        if message["type"] in ("chat", "normal"):
            if match := COMMAND_REGEX.match(message["body"]):
                command_name = match.group(1)
                args = match.group(2).split()
                await self.execute(command_name, args, message)

    async def execute(self, command, args, message):
        try:
            func = self.commands[command]
            await func(self, message, *args)
        except KeyError:
            self.send_message(message["from"], "Command not found.")


if __name__ == "__main__":
    import json
    from pathlib import Path
    import logging
    import ssl

    here = Path(__file__).parent

    secrets = here.joinpath("secrets/users.json")
    users = json.loads(secrets.read_text())

    username = users[0]["username"]
    password = users[0]["password"]

    logging.basicConfig(level=logging.DEBUG, format="%(levelname)-8s %(message)s")

    bot = Bot(f"{username}@vmbox.lan/python-bot", password)
    bot.register_plugin("xep_0030")  # Service Discovery
    bot.register_plugin("xep_0004")  # Data Forms
    bot.register_plugin("xep_0060")  # PubSub
    bot.register_plugin("xep_0199")  # XMPP Ping
    bot.use_ssl = True

    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    bot.ssl_context = context
    bot.connect(address=("vmbox.lan", 5222))
    bot.process(forever=True)
