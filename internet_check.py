from ping3 import ping


def pinger(host):
    ping_time = ping(host)
    return str(ping_time * 1000)[0:5]  # in ms


def multi_ping(hosts):
    ping_results = {}
    for host in hosts:
        ping_results[host] = pinger(host)
    return str(ping_results)


results = multi_ping(['1.1.1.1', '8.8.8.8'])
