#!/usr/bin/env python3
from dataclasses import dataclass, asdict
import time
from ipaddress import ip_network
import itertools
import random


@dataclass
class Request:
    method: str
    path: str
    protocol: str

    def __str__(self):
        return "{method} {path} {protocol}".format(**asdict(self))


@dataclass
class LogLine:
    remote_addr: str
    remote_user: str
    time_local: str  # "common log format"
    request: str
    status: int
    body_bytes_sent: int
    http_referrer: str
    http_user_agent: str

    def __str__(self):
        return '{remote_addr} - {remote_user} [{time_local}] "{request}" {status} {body_bytes_sent} "{http_referrer}" "{http_user_agent}"'.format(
            remote_addr=self.remote_addr,
            remote_user=self.remote_user,
            time_local=self.time_local,
            request=self.request,
            status=self.status,
            body_bytes_sent=self.body_bytes_sent,
            http_referrer=self.http_referrer,
            http_user_agent=self.http_user_agent,
        )


def format_time(epoch_secs: int) -> str:
    local_time_struct = time.localtime(epoch_secs)
    return time.strftime("%d/%b/%Y:%H:%M:%S %z", local_time_struct)


# CIDR (range, weight)
CIDR_BLOCKS = [
    ("10.0.10.0/24", 10),
    ("10.0.20.0/24", 10),
    ("192.168.0.0/20", 15),
    ("192.168.1.18/32", 15),
    ("192.168.1.42/32", 12),
    ("10.0.20.99/32", 10),
    ("74.0.0.0/24", 50),
    ("14.0.0.0/24", 50),
]


def get_remote_ip() -> str:
    subnets = [b[0] for b in CIDR_BLOCKS]
    weights = [b[1] for b in CIDR_BLOCKS]
    subnet = random.choices(subnets, weights, k=1)[0]
    return random.choice(list(ip_network(subnet).hosts()))


def make_request() -> Request:
    method = random.choice(["GET", "POST"])
    path = random.choice(
        [
            "/users",
            "/user?id=%d" % random.randint(1000, 3999),
            "/items?user_id=%d" % random.randint(1000, 3999),
            "/item?id=%d" % random.randint(10, 87000),
        ]
    )
    protocol = random.choices(["HTTP/1.1", "HTTP/2.0"], [150, 1], k=1)[0]

    return Request(method, path, protocol)


def get_referrer() -> str:
    return "/"


def get_status_code(method: str) -> int:
    if method == "POST":
        choices = [201, 404, 400, 503]
        weights = [100, 20, 10, 20]
    else:
        choices = [200, 404, 503]
        weights = [100, 20, 20]
    return random.choices(choices, weights, k=1)[0]


USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15",
]


def get_useragent() -> str:
    return random.choice(USER_AGENTS)


if __name__ == "__main__":
    log_time = time.time()
    for i in range(3000):
        request = make_request()
        log_line = LogLine(
            remote_addr=get_remote_ip(),
            remote_user="-",
            time_local=format_time(log_time),
            request=str(request),
            status=get_status_code(request.method),
            body_bytes_sent=random.randint(0, 6999),
            http_referrer=get_referrer(),
            http_user_agent=get_useragent(),
        )
        print(str(log_line))

        log_time += 5 * random.random()  # 0-5 seconds
