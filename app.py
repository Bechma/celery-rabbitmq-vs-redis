import random
from celery import Celery
from tasks import simple_task
import sys
import time
import string


def random_string(length):
    return random.choices(string.ascii_letters, k=length)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Missing broker name(redis or rabbit)")
        exit(-1)
    if sys.argv[1] == "redis":
        broker = "redis://localhost:6379/0"
    elif sys.argv[1] == "rabbit":
        broker = "pyamqp://guest:guest@localhost"
    else:
        print("The broker name must be redis or rabbit")
        exit(-1)
    app = Celery("benchmarking",
                 backend="redis://localhost:3000/0", broker=broker)

    n = 1_000 if len(sys.argv) >= 3 and not sys.argv[2] else int(sys.argv[2])
    length = 5 if len(sys.argv) >= 4 and not sys.argv[3] else int(sys.argv[3])
    start = time.perf_counter()
    result = [simple_task.delay(random_string(length)) for _ in range(n)]
    result = [i.get() for i in result]
    end = time.perf_counter()
    print(
        f"Time elapsed broker={sys.argv[1]} length=+{length} Bytes messages={n} {end-start}s")
