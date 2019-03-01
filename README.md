# Python KISS client

This is a program that can be used to send AX.25 KISS packets via a TNC (physical or software). It is primarily made to work with Direwolf.

Inspired by Daniel Estévez's code from this article: [Open telecommand for BY70-1](https://destevez.net/2017/01/open-telecommand-for-by70-1/).

# Usage

To send a message you first need to have a KISS TNC such as [Direwolf](https://github.com/wb2osz/direwolf) or a physical one connected to a serial port.

To send via the serial port you need to use the `--serial` option. The command would look like this:
```
kiss.py --serial [port] -p [destination] [source] [messsage] 
```

If you don't provide the serial port, the default is `/tmp/kisstnc` (the one Direwolf defaults to).

If you have a TNC listening on a network port you need to use the `--net` option:
```
kiss.py --net [address] -p [destination] [source] [messsage] 
```

The address defaults to '127.0.0.1'.

