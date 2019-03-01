#!/usr/bin/env python3

import socket
import serial
import argparse


def ax25call(callsign):
	"""
	Makes a byte array of the callsign in the AX.25 needed format.
	"""
	s = callsign.split('-')
	call = s[0].upper()[:6]
	call = call + ' ' * (6 - len(call))
	ssid = 0 if len(s) == 1 else int(s[1])
	c = bytes([c << 1 for c in bytes(call, 'ascii')])
	ss = bytes([0x60 | (ssid & 0xf) << 1])

	return c + ss


def build_packet(dst, src, message):
	"""
	Builds the AX.25 KISS packet.
	"""
	dst = ax25call(dst)
	src = ax25call(src)
	cmd = message.encode("ascii")

	# 0x03 = UI frame; 0xf0 = no layer 3 protocol
	# Last bit of the address field needs to be 1
	packet = dst + src[:-1] + bytes([src[-1] | 1]) + b'\x03\xf0' + cmd

	# 0xc0 = frame end; 0x00 = KISS send command
	kiss = b'\xc0\x00' + packet.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'

	return kiss


def send_kiss_net(packet, address, port):
	"""
	Sends the KISS packet to the given network address and port.
	"""
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((address, port))
	s.send(packet)
	s.close()


def send_kiss_serial(packet, tnc_port):
	"""
	Sends the KISS packet to a serial port.
	"""

	ser = serial.Serial(
			port=tnc_port,
			baudrate=9600,
		)

	ser.isOpen()
	ser.write(packet)
	ser.close()


def main():
	parser = argparse.ArgumentParser()
	group = parser.add_mutually_exclusive_group()

	group.add_argument("--net", type=str, nargs='?', const="127.0.0.1", help="network address")
	group.add_argument("--serial", type=str, nargs='?', const="/tmp/kisstnc", help="serial port")
	parser.add_argument("-p", "--packet", type=str, nargs=3, help="the packet you want to send; DST SRC MESSAGE")

	args = parser.parse_args()

	dst = args.packet[0]
	src = args.packet[1]
	message = args.packet[2]

	packet = build_packet(dst, src, message)

	if args.net is not None:
		send_kiss_net(packet, args.net, 8001)
	elif args.serial is not None:
		send_kiss_serial(packet, args.serial)


if __name__ == "__main__":
	main()
