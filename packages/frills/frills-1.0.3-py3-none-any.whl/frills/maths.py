
def find_divisors(n):
	divisors = []
	for i in range(1, n):
		if n % i == 0:
			divisors.append(i)
	print(divisors)