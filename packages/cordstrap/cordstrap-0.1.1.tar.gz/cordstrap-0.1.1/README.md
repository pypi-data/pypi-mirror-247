# Cordstrap

Bootstrap your Discord servers

## Usage

1. Install `cordstrap` from source:

```sh
git clone https://github.com/interrrp/cordstrap --depth 1
cd cordstrap
python3 -m pip install .
```

2. Set up your `server.cordstrap.yaml` (see [example](./server.cordstrap.yaml))

3. Run `cordstrap`:

```sh
cordstrap BOT_TOKEN GUILD_ID
```

...where `BOT_TOKEN` is your Discord bot token and `GUILD_ID` is the ID of the
guild (a.k.a. "server") you want to bootstrap.
