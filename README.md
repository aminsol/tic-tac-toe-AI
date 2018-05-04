# Tic Tac Toe AI

Socket-based client-server Tic Tac Toe game with an AI player in Python.
The AI uses reinforcement learning and min/max algorithm to learn and play the game. 

The provided database is almost fully trained. However, if you want to see how the AI learns you can empty `longterm` table.

## Configuration

1- Run a mysql server

2- Create a database with the name of `tictactoe`.

3- Create a user with name of `tictactoe` and set the password to `tic`.

4- Give user `tictactoe` all the permissions for `tictactoe`.

5- import `tictactoe.sql` to `tictactoe` database.

## Run

```
ttt_server.py 3413
ttt_AI_loop.py 127.0.0.1 3413
ttt_client_gui.py
```

## Authors

* Amin Soltani
* Josh Beckman
* Tyler Stickler

## Credits

* Chen Yumin founder of CharmySoft

### References 

https://github.com/chen-yumin/tic-tac-toe-in-python

