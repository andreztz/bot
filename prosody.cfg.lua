daemonize = true
pidfile = "/run/prosody/prosody.pid"
storage = "internal"

plugin_paths = {
    "/usr/lib/prosody/modules",
    "/usr/local/lib/prosody/modules"
}

admins = { "admin@vmbox.lan" }

modules_enabled = {
  "disco";
  "roster";
  "saslauth";
  "tls";
  "dialback";
  "posix";
  "c2c";
}

allow_registration = false

ssl = {
  key = "/etc/prosody/certs/vmbox.lan.key";
  certificate = "/etc/prosody/certs/vmbox.lan.crt";
}

VirtualHost "vmbox.lan"
    authentication = "internal_plain"

log = {
  { levels = { min = "debug" }, to = "console"};
}
