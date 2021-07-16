# Specifications
- Hardware:
  - Processor: i7-9750H
  - RAM: 32GB
- SO: Windows 10 Professional x64
- Python 3.8.10
- Celery 5.1.2 (12 workers)
- Redis v6.2.4 backend
- Redis v6.2.4 broker
- RabbitMQ v3.8.14 broker
- Docker with WSL2 as a backend

Both Redis and Rabbit have the default configuration(with the exception of the second redis
acting as a backend that have a different default port).


# Instructions to run on your systems

I made everything to keep things nice and easy:

```powershell
git clone https://github.com/Bechma/celery-rabbitmq-vs-redis ./crvs
cd ./crvs
python -m venv venv
& ./venv/Scripts/Activate.ps1
docker-compose up -d
pip install -r requirements.txt
./run1.ps1
./run2.ps1
```

# Results
All times are measured in seconds. Take the results as a reference, as the benchmark
is self made. If I made something wrong I'm more than happy to fix it.

## Redis

| total messages | iter1    | iter2    | iter3    | iter4    | iter5    | avg      | std    |
| -------------- | -------- | -------- | -------- | -------- | -------- | -------- | ------ |
| 100            | 0.5070   | 0.5402   | 0.5352   | 0.5246   | 0.6352   | 0.5484   | 0.0501 |
| 500            | 1.7293   | 1.7511   | 1.5756   | 1.6054   | 1.7344   | 1.6792   | 0.082  |
| 1000           | 3.2468   | 3.2050   | 2.9194   | 3.0427   | 3.4820   | 3.1792   | 0.2139 |
| 5000           | 16.3459  | 15.9685  | 14.2287  | 14.1687  | 15.8892  | 15.3202  | 1.0384 |
| 10000          | 38.3914  | 37.5223  | 33.4419  | 35.3912  | 36.2909  | 36.2075  | 1.9248 |
| 50000          | 175.6866 | 173.6639 | 171.4163 | 182.7176 | 179.9086 | 176.6786 | 4.6007 |

## RabbitMQ

| total messages | iter1    | iter2    | iter3    | iter4    | iter5    | avg      | std    |
| -------------- | -------- | -------- | -------- | -------- | -------- | -------- | ------ |
| 100            | 0.4693   | 0.5115   | 0.5297   | 0.4956   | 0.4441   | 0.49     | 0.0339 |
| 500            | 1.5276   | 1.4719   | 1.3981   | 1.4574   | 1.4950   | 1.47     | 0.0482 |
| 1000           | 2.8623   | 2.7301   | 2.8031   | 2.7363   | 2.6339   | 2.7531   | 0.0858 |
| 5000           | 13.2805  | 13.7742  | 13.2819  | 13.5831  | 13.1306  | 13.4101  | 0.2617 |
| 10000          | 26.6272  | 26.2769  | 26.9550  | 26.4570  | 25.5128  | 26.3658  | 0.5384 |
| 50000          | 125.9251 | 124.7698 | 124.5677 | 124.9540 | 124.0607 | 124.8555 | 0.6848 |

## Side to side comparison

##### Average Times, lower is better
| total messages | RabbitMQ | Redis    |
| -------------- | -------- | -------- |
| 100            | 0.49     | 0.5484   |
| 500            | 1.47     | 1.6792   |
| 1000           | 2.7531   | 3.1792   |
| 5000           | 13.4101  | 15.3202  |
| 10000          | 26.3658  | 36.2075  |
| 50000          | 124.8555 | 176.6786 |

##### Standard Deviation, lower is better

| total messages | RabbitMQ | Redis  |
| -------------- | -------- | ------ |
| 100            | 0.0339   | 0.0501 |
| 500            | 0.0482   | 0.082  |
| 1000           | 0.0858   | 0.2139 |
| 5000           | 0.2617   | 1.0384 |
| 10000          | 0.5384   | 1.9248 |
| 50000          | 0.6848   | 4.6007 |


### Long messages

Following the [official documentation](https://docs.celeryproject.org/en/stable/getting-started/backends-and-brokers/index.html#redis), redis looks to perform bad with long messages.

We are going to try it with the same task example but increasing the message size +1MB


## Redis

| total messages | iter1    | iter2    | iter3    | avg      | std    |
| -------------- | -------- | -------- | -------- | -------- | ------ |
| 100            | 70.6913  | 72.3711  | 75.6312  | 72.8979  | 2.0508 |
| 200            | 141.6594 | 145.2148 | 149.5441 | 145.4728 | 3.2241 |

## RabbitMQ

| total messages | iter1    | iter2    | iter3    | avg      | std    |
| -------------- | -------- | -------- | -------- | -------- | ------ |
| 100            | 58.1334  | 59.5851  | 60.5988  | 59.4391  | 1.0118 |
| 200            | 114.6794 | 117.0006 | 122.3457 | 118.0086 | 3.2099 |


##### Average Times, lower is better
| total messages | RabbitMQ | Redis    |
| -------------- | -------- | -------- |
| 100            | 59.4391  | 72.8979  |
| 200            | 118.0086 | 145.4728 |

##### Standard Deviation, lower is better

| total messages | RabbitMQ | Redis  |
| -------------- | -------- | ------ |
| 100            | 1.0118   | 2.0508 |
| 200            | 3.2099   | 3.2241 |


# Conclussion

It looks like Redis although it's a great backend, as a broker, it's better RabbitMQ.
I could have made another comparison with priority queues, but as redis does not have that feature, and celery do a python-side implementation with redis, there is no doubt that Rabbit would win that race too.
Besides, Rabbit offers more configuration parameters for queue jobs and persistency.
