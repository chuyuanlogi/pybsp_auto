# requirements

* python 3.7 or later
* adbutils
* pillow 9.3.0 or later

## install packages

* adbutil

```shell
pip3 install adbutils
```

* pillow

```shell
pip install --upgrade pillow
```

# how to use

* list all test modules

```shell
python main.py -l (or --list)
```

the response should be:
```shell
starting test on: 2022-11-09 15:43:23
mix
```

* run test script

```shell
python main.py -r mix (or --run mix)
```

# how to create a new test
implementing...