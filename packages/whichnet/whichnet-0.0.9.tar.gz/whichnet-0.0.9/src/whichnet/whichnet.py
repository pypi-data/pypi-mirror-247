#!/usr/bin/env python3
from scapy.all import *
import os
import argparse
import ipaddress
import threading
import datetime, time

SEEN_ADDRESSES = {
	#'mac addr': {ips:[], related_ips:[], related_operations:[]}
}
INTF = None
DEBUG = False
STOPPING = False
TOTAL_IPS = 0
SCANNED_IPS = 0
LAST_DISPLAY = datetime.datetime.now()
#create a function the capture all packets with arp protocol on a given interface
def sniff_arp(interface, operation):
	global INTF
	global STOPPING
	try:
		INTF = interface
		clear()
		#sniff(iface=interface, store=False, prn=process_sniffed_packet, filter="arp" )
		if operation != "all":
				sniff(iface=interface, store=False, prn=process_sniffed_packet, filter="arp and arp [6:2] = " + operation, stop_filter=lambda x: STOPPING)
		else:
				sniff(iface=interface, store=False, prn=process_sniffed_packet, filter="arp", stop_filter=lambda x: STOPPING)
	except KeyboardInterrupt:
		STOPPING = True
		return


def clear():
	os.system("clear")
	print("Sniffing on interface " + INTF + "...")
	print("Scanned " + str(SCANNED_IPS) + " of " + str(TOTAL_IPS) + " IPs" )
	print("")




def update_display():
	global SEEN_ADDRESSES
	global LAST_DISPLAY
	"""show all entries in seen addresses, with columns for mac, ips, related ips, related operations, and count, sorted by count desc. With the ips and related ips one per line."""
	if LAST_DISPLAY + datetime.timedelta(seconds=1) > datetime.datetime.now():
		return
	LAST_DISPLAY = datetime.datetime.now()
	clear()
	print("MAC\t\t\tIPs\t\tRelated IPs\tRelated Operations\tCount")
	for mac, info in sorted(SEEN_ADDRESSES.items(), key=lambda x: x[1]['count'], reverse=True):
		ips = info['ips'].copy()
		ips=sorted(ips, reverse=True)
		related_ips = info['related_ips'].copy()
		related_ips=sorted(related_ips, reverse=True)
		print(mac + "\t" + str(ips.pop() if ips else "1\t") + "\t" + str(related_ips.pop() if related_ips else "2\t") + "\t" + str(
			info['related_operations']) + "\t\t\t" + str(info['count']))
		while ips or related_ips:
			print("\t\t"+str(ips.pop() if ips else "\t\t") + "\t" + str(related_ips.pop() if related_ips else "2\t\t"))
	if DEBUG:
		print(SEEN_ADDRESSES)


#create a function to process the captured packets
def process_sniffed_packet(packet):
	global SEEN_ADDRESSES
	global STOPPING
	if packet.haslayer(ARP):# and packet[scapy.ARP].op == 2:
		src_mac = packet[ARP].hwsrc
		src_ip = ipaddress.ip_address(packet[ARP].psrc)
		dst_ip = ipaddress.ip_address(packet[ARP].pdst)
		op = 0
		if not src_mac in SEEN_ADDRESSES:
			SEEN_ADDRESSES[src_mac] = {'ips': [], 'related_ips': [], 'related_operations': [], 'count': 0}
		if DEBUG:
			print(packet.show())

		if packet[ARP].op == 1:
			op = 1
		elif packet[ARP].op == 2:
			op = 2
		else:
			print("Unknown operation : " + str(packet[ARP].op))

		if not src_ip in SEEN_ADDRESSES[src_mac]['ips']:
			SEEN_ADDRESSES[src_mac]['ips'].append(src_ip)
		if not dst_ip in SEEN_ADDRESSES[src_mac]['related_ips']:
			SEEN_ADDRESSES[src_mac]['related_ips'].append(dst_ip)
		if not op in SEEN_ADDRESSES[src_mac]['related_operations']:
			SEEN_ADDRESSES[src_mac]['related_operations'].append(op)
		SEEN_ADDRESSES[src_mac]['count'] += 1

		update_display()

def scan(ranges,interface):
	global SEEN_ADDRESSES
	global TOTAL_IPS
	global SCANNED_IPS
	global STOPPING
	try:
		for r in ranges:
			TOTAL_IPS += r.num_addresses
		s = conf.L2socket(iface=interface)
		for r in ranges:
			for ip in r.hosts():
				arp = ARP(pdst=str(ip))
				broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
				arp_broadcast = broadcast/arp
				s.send(arp_broadcast)
				SCANNED_IPS += 1
				if STOPPING:
					return
		update_display()

	except KeyboardInterrupt:
		STOPPING = True
		return


def main():
	global STOPPING
	"""parse command line arguments with interface, passive or active mode and operation 1,2 or all and multiple ip addresses scan range"""
	if not os.getuid() == 0:
		print("This program must be run as root.")
		exit(1)

	argparser = argparse.ArgumentParser()
	argparser.add_argument("-i", "--interface", help="Interface to sniff on", required=True)
	argparser.add_argument("-p", "--passive", help="Passive mode", action="store_true", default=False)
	argparser.add_argument("-o", "--operation", help="Operation to sniff for (1, 2, or all)", default="2", choices=["1", "2", "all"])
	argparser.add_argument("-r", "--range", help="IP range to scan, can have multiple", action="append")
	argparser.add_argument("-w", "--wait", help="Wait when scan finished, else exit", action="store_true", default=True)
	args = argparser.parse_args()

	if args.passive and args.range:
		print("Passive mode and IP range are mutually exclusive.")
		exit(1)

	if not args.passive and not args.range:
		print("Active mode requires an IP range.")
		exit(1)

	if not args.passive:
		ranges = []
		for r in args.range:
			try:
				ranges.append(ipaddress.ip_network(r,strict=True))
			except ValueError:
				print("Invalid IP range: " + r)
				exit(1)

	#Start sniffing thread
	sniff_thread = threading.Thread(target=sniff_arp, args=(args.interface, args.operation))
	sniff_thread.start()

	#Start scanning thread
	scan_thread = None
	if not args.passive:
		scan_thread = threading.Thread(target=scan, args=(ranges,args.interface))
		#grant time for sniff thread to start
		time.sleep(1)
		scan_thread.start()

	while True:
		try:
			if not args.wait:
				break
			time.sleep(0.1)
			update_display()
		except KeyboardInterrupt:
			STOPPING = True
			break

	if scan_thread:
		scan_thread.join()

	#senmd a packet to trigger a sniff dislock
	arp = ARP(pdst=str("192.168.1.1"),op=int(args.operation) if args.operation != "all" else 2)
	broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
	arp_broadcast = broadcast/arp
	sendp(arp_broadcast, iface=args.interface, verbose=False)

	sniff_thread.join()

if __name__ == "__main__":
	main()