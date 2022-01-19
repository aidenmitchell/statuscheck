from ping3 import ping


def pinger(host):
    ping_time = ping(host)
    return str(ping_time * 1000)[0:3]  # in ms


def multi_ping(hosts):
    ping_results = []
    for host in hosts:
        result = pinger(host)
        ping_results.append([host, result])
    return ping_results
