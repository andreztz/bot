import socket
import asyncio 

import psutil

COMMANDS = {}


def command(name):
    def decorator(func):
        COMMANDS[name] = func
    return decorator


async def is_mpv_running():
    result = await asyncio.to_thread(_check_mpv_running)
    return result


def _check_mpv_running():
    for proc in psutil.process_iter(["pid", "name", "cmdline"]):
        if (
            proc.info["name"] == "mpv"
            and "--player-operation-mode=pseudo-gui" in proc.info["cmdline"]
        ):
            return True
    return False


async def async_run(command):
    process = await asyncio.create_subprocess_shell(
        command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    # stdout, stderr = await process.communicate()
    # print(stdout.decode(), stderr.decode())


@command("volume")
async def volume_handler(bot, message, *args, **kwargs):

    cmd = None

    if args[0] == "inc":
        cmd = "amixer set Master 5%+"
    elif args[0] == "dec":
        cmd = "amixer set Master 5%-"
    elif args[0] == "mute":
        cmd = "amixer set Master toggle"
    elif args[0] == "set":
        cmd = f"amixer set Master {args[1]}"
    if cmd:
        asyncio.create_task(async_run(cmd))


@command("mpv")
async def mpv_command(bot, message, *args, **kwargs):
    SOCKET_PATH = "/tmp/bot_mpvsocket"

    def send(command):
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            s.connect(SOCKET_PATH)
            s.sendall(bytes(command, encoding="utf-8"))
            response = s.recv(1024)
            print(response.decode("utf-8"))
            bot.send_message(message["from"], "Executando comando no mpv")

    is_running = await is_mpv_running()

    if not is_running:
        command = f"mpv --input-ipc-server={SOCKET_PATH} --player-operation-mode=pseudo-gui {args[0]}"
        asyncio.create_task(async_run(command))
        bot.send_message(message["from"], "Iniciando")
        return

    if args[0] == "fullscreen":
        send("set fullscreen yes\n")
    elif args[0] == "stop":
        send(f"stop\n")
    else:
        send(f"loadfile {args[0]}\n")
