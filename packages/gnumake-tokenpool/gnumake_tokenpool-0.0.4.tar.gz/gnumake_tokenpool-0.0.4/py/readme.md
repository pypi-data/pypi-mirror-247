# gnumake-tokenpool/py

python jobclient and jobserver for the GNU make tokenpool protocol

## install

install from [github](https://github.com/milahu/gnumake-tokenpool)

```
pip install git+https://github.com/milahu/gnumake-tokenpool
```

or install from [pypi](https://pypi.org/project/gnumake-tokenpool/)

```
pip install gnumake-tokenpool
```

## usage

```py
import gnumake_tokenpool

jobClient = gnumake_tokenpool.JobClient()

token = jobClient.acquire()

# do some work

jobClient.release(token)
```

see also [test/jobclient/test.py](test/jobclient/test.py)
