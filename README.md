# TEXAS HOLD EM
There are 2 python applications in the project:
1. server: Texas server application (REST APIs)
2. client: client application for the Texas server


# How it works
- Start the Server (default port: 5000)
- the server's main entry point is a registration API (/registration) where the clients can register themself
- the clients have to provide 2 REST API endpoint for the game:
- CLIENT API1: /ping (GET) - this is used for healthcheck from the server
- CLIENT API2: /phase (POST) - when the server sends the actual state of the actual Play
    - request:
```
{
    "player_card": ["8D", "3H"],
    "cards_on_table": [],
    "players": [
        {
            "name": "client1",
            "coin": 10000
        },
        {
            "name": "client2",
            "coin": 10000
        }
    ],
    "pot": 0,
    "phase": "PRE_FLOP",
    "round": "NORMAL"
}
```
   - response:
```
{
    "action": "RAISED",
    "raised_coins": 100
}
```


# Client usage

#
