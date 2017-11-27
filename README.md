# B2-bkup

B2-bkup is a python tool to automate the 3-3-1 backup solution using Backblaze.

It provides a server-client architecture, and is customizable.


## How It Works

Need to run First Time Setup Execution on server with the following command:
```sh
$ python master.py --ftsu
```

And to run First Time Setup Execution on minion with the following command:
```sh
$ python minion.py --ftsu
```

## Usage

Add to crontab `...`:

```sh
$ python3 ...
```

Add `blah` section to `config.ini`:

```diff
+ api:
+ username:
```


## Config

B2-kup blah blah

`...` section to `...`:

   ```
     Blah
   ```


## Built With

* [Python](https://www.python.org/download/releases/3.0/) - Python


## Authors

* **TJ Balon** - *Initial work* - [balon](https://git.tangoworldwide.net/balon)

* **Matt Topor** - *Initial work* - [polak](https://git.tangoworldwide.net/polak)


## License

This project is to be determined...

## Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration
* etc
