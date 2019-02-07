# PyAtmo
Python Netatmo scripts

<b>Clone repo</b>
```
git clone https://github.com/mr3188/PyAtmo
```

<b>Create config file and edit</b>
```
cp PyAtmo_sample.conf PyAtmo.conf
cat PyAtmo.conf

[home]
# default home name
name = homeName

# Security configuration to access server data
[security]
username = <netatmo username>
password = <password>
client_id = <24 length alphanumeric vallue>
client_secret = <34 length alphanumeric value>
scope = read_station read_thermostat write_thermostat
```

<b>Run test Python script</b>
```
python3 testPyAtmo.py
```
