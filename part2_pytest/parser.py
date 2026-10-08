import re

# Регулярний вираз для рядків виводу iperf3 з полями Interval/Transfer/Bitrate/Retr/Cwnd
# Приклад рядка: [  5]   0.00-1.00   sec  5.00 GBytes  42.9 Gbits/sec    0    407 KBytes
REGEXP = re.compile(
    r'\[\s*\d+\]\s+([\d.]+-[\d.]+)\s+sec\s+'
    r'([\d.]+)\s+[KMG]?Bytes\s+'
    r'([\d.]+)\s+[KMG]?bits/sec\s+'
    r'(\d+)\s+'
    r'([\d.]+)\s+[KMG]?Bytes'
)
KEYS = ('Interval', 'Transfer', 'Bitrate', 'Retr', 'Cwnd')


def parser(output):
    """
    Розбирає вивід iperf3-клієнта та повертає список словників з усіма інтервалами передачі.

    :param output: текстовий вивід iperf3 (stdout)
    :return: список словників виду
             {'Interval': '0.00-1.00', 'Transfer': 5.0, 'Bitrate': 42.9, 'Retr': 0.0, 'Cwnd': 407.0}
    """
    result = []
    for line in output.splitlines():
        match = REGEXP.search(line)
        if match:
            interval, transfer, bitrate, retr, cwnd = match.groups()
            result.append({
                'Interval': interval,
                'Transfer': float(transfer),
                'Bitrate': float(bitrate),
                'Retr': float(retr),
                'Cwnd': float(cwnd),
            })
    return result
