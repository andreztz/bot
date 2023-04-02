#!/user/bin/env python

import json
import subprocess
import sys 

from pathlib import Path


here = Path(__file__).parent
secrets = here.joinpath("secrets/users.json")
users = json.loads(secrets.read_text())

domain = sys.argv[1]

for user in users:
    command = [
        "sudo",
        "prosodyctl",
        "register",
        f"{user['username']}",
        f"{domain}",
        f"{user['password']}"
    ]
    lcommand = ' '.join(command)
    print(f"Running: {lcommand}")
    result = subprocess.run(command, stdout=subprocess.DEVNULL)
    if result.returncode != 0:
        print(f"'{lcommand}' command failed, with exit code: {result.returncode}.")
