weiqi.gs
========
[weiqi.gs](https://weiqi.gs) is an open-source game server for the game of Go, also known as weiqi (围棋) or baduk (바둑).

weiqi.gs tries to be clean, simple and easy-to-use, while still providing all the basic features expected from a go server.

Development environment
-----------------------
Backend is written in python3.5, frontend in [Vue.js](https://vuejs.org/):
- `pip install -r requirements.txt`
- `npm install`

Besides the dependencies in `requirements.txt` and `package.json` you may also need to install some additional libraries first:
```bash
$ sudo apt-get install python3-dev libpq-dev libjpeg-dev
```

Before you can run the development server you will need to migrate the database. This step also needs to be run every time new DB migrations are created:
```bash
$ alembic upgrade head
```

To run the development server:
```bash
$ ./gulp.sh
```

After this the server will listen on http://localhost:8000 by default.

Rooms
-----
Initially the database will be empty, meaning that there are no rooms. To create a new default chat room:
```bash
$ ./main.py --create-room='Main Room'
```

Tests
-----
```bash
$ py.test --benchmark-skip weiqi
```

License
-------
GNU AGPLv3

Check the [LICENSE](https://gitlab.com/mibitzi/weiqi.gs/blob/master/LICENSE) file for more information.