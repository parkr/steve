# steve

Mail time. Mail time! MAIL TIME!!! We just got a letter!

![Oh yeah.](http://25.media.tumblr.com/tumblr_m8k7u4B9FT1r7vxcmo1_500.gif)

## Installation

Run `server.py` in the background and add the following to your `nginx.conf`:

```nginx
server {
  listen 80;
  server_name my_server.com;

  location / {
    proxy_pass        http://localhost:8888;
    proxy_set_header  X-Real-IP  $remote_addr;
  }
}
```

## Usage

Set the `forward()` rule in your MailGun preferences:

```text
forward("http://my_server.com/messages/store")
```

On your server, just run the following and you're good to go:

```bash
~/code/steve$ ./server.py
# => [I 130714 21:08:29 pid:11] Checking pidfile '/var/run/steve.8888.pid'
```

## License

MIT
