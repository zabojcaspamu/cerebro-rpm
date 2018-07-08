cerebro
------------

cerebro spec for rpm

.. note::
Option start cerebro in file /etc/sysconfig/cerebro

for example:

cat /etc/sysconfig/cerebro
```
-Dhttp.port=1234 -Dhttp.address=127.0.0.1
```

Repo with cerebro rpm

http://repo.zabojcaspamu.pl

Add to yum

```
yum-config-manager --add-repo http://repo.zabojcaspamu.pl
```
