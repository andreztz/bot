import slixmpp


class MyBot(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start_session)
        self.add_event_handler('message', self.message)

    async def start_session(self, event):
        self.send_presence()
        self.get_roster()


    async def message(self, msg):
        print(msg)


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

    xmpp = MyBot(f'{username}@vmbox.lan/python-bot', password)
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0004') # Data Forms
    xmpp.register_plugin('xep_0060') # PubSub
    xmpp.register_plugin('xep_0199') # XMPP Ping
    xmpp.register_plugin('xep_0199') # Ping

    xmpp.use_tls = True
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    xmpp.ssl_context = context
    xmpp.connect(address=('vmbox.lan', 5222))
    xmpp.process(forever=True)
