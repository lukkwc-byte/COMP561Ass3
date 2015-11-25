with open('b.fa', 'r') as b:
	with open('n.fa', 'r') as n:
		with open('b0.fa', 'w') as b0:
			with open('n0.fa', 'w') as n0:
				for line in b:
					b0.write(line.strip())
				for line in n:
					n0.write(line.strip())