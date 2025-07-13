enc = "70 58 43 73 58 52 55 91 112 37 94 106 28 108 234 1 204 195 28 91 76 43 34 106 99 118"
enc = bytes([int(x) for x in enc.split()])
for e in enc:
	for i in range(256):
		if (i * 3) % 257 == e:
			print(chr(i), end='')
print()

# midnight{buy_$NVDA_today!}
