import subprocess
import re

data = subprocess.run(["netdiscover", "-r", "192.168.0.0/24", "-P"], capture_output=True).stdout.decode()
order_ips = sorted([int(each.split()[0].split(".")[-1])for each in data.split("\n") if re.findall(r"\d+.\d+.\d+.\d+", each)])
get_all_hostnames = {each.split()[0]:" ".join(each.split()[4:]) for each in data.split("\n") if re.findall(r"\d+.\d+.\d+.\d+", each)}
sorted_ips = [(ip, host) for each_number in order_ips for ip, host in get_all_hostnames.items() if str(each_number) == ip.split(".")[-1]]

print(sorted_ips)