s = open('test.txt', 'r').read()
if all(ord(char) < 128 for char in s):
	print('all chars in file are ascii')
else:
	print('not all chars in file are ascii')
	for char in s:
		if not ord(char) < 128:
			print('non-ascii char {}'.format(char))

