# IoT 2021 - Project

## Python Virtual Environment

We will use a Python Virtual Environment for not messing up with the entire OS files. 

```shell
python3 -m venv venv
```

Use the virtual environment

```shell
source ./venv/bin/activate
```

Tip: For leaving the virtual environment type 

```shell
deactivate
```

## The Objectives

1. Receive the data produced by a IoT device
2. Store the data in a MQTT Server hosted in the cloud
3. Read the data and take some action

## Reference Architecture 

![Architecture](img/arch.png "IoT Architecture")

```
ALEXAKOS, Christos et al. Building an industrial iot infrastructure with open source software 
for smart energy. In: 2019 First International Conference on Societal Automation (SA). IEEE, 2019. p. 1-8.
```