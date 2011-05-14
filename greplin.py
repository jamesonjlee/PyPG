Q1 = "FourscoreandsevenyearsagoourfaathersbroughtforthonthiscontainentanewnationconceivedinzLibertyanddedicatedtothepropositionthatallmenarecreatedequalNowweareengagedinagreahtcivilwartestingwhetherthatnaptionoranynartionsoconceivedandsodedicatedcanlongendureWeareqmetonagreatbattlefiemldoftzhatwarWehavecometodedicpateaportionofthatfieldasafinalrestingplaceforthosewhoheregavetheirlivesthatthatnationmightliveItisaltogetherfangandproperthatweshoulddothisButinalargersensewecannotdedicatewecannotconsecratewecannothallowthisgroundThebravelmenlivinganddeadwhostruggledherehaveconsecrateditfaraboveourpoorponwertoaddordetractTgheworldadswfilllittlenotlenorlongrememberwhatwesayherebutitcanneverforgetwhattheydidhereItisforusthelivingrathertobededicatedheretotheulnfinishedworkwhichtheywhofoughtherehavethusfarsonoblyadvancedItisratherforustobeherededicatedtothegreattdafskremainingbeforeusthatfromthesehonoreddeadwetakeincreaseddevotiontothatcauseforwhichtheygavethelastpfullmeasureofdevotionthatweherehighlyresolvethatthesedeadshallnothavediedinvainthatthisnationunsderGodshallhaveanewbirthoffreedomandthatgovernmentofthepeoplebythepeopleforthepeopleshallnotperishfromtheearth"
Q2 = 227000
Q3 = [3, 4, 9, 14, 15, 19, 28, 37, 47, 50, 54, 56, 59, 61, 70, 73, 78, 81, 92, 95, 97, 99]


#Fubd tge longest reversible substring
def do1(s):
	s = s.lower()
	best = ""
	good = ""
	_len = len(s)
	for _i in xrange(0,_len,1):
		for _j in xrange(_i+3,_len,1): #remember range is exclusive of the max
			good = s[_i:_j:1]
			if good[::-1] == good and len(good) > len(best):
				best = good
	return best

#find the sum of prime divisors of a Fibonnaci Prime

def fib(end,v1=1,v2=1):
	if end < v2:
		return v1,v2
	else:
		return fib(end,v2,v1+v2)
def isPrime(val):
	if val%2 == 0:
		return 0
	else:
		for i in xrange(3,val,2): #yes this repeats all non-primes
			if val%i == 0:
				return 0
	return 1
def sumPD(val):
	c = 0
	if val%2 == 0:
		c = 2
	for i in xrange(3,val,2):
		if val % i == 0 and isPrime(i):
			c = c + i
	return c
def do2(val):
	v1,v2 = fib(val)
	while not isPrime(v2):
		v1,v2 = v2, v1+v2
	return sumPD(v2+1)

#find subset who's sum exists in the set
#thx stackoverflow
import itertools
def findsubsets(S,m):
  #takes progressively longer and longer
	return set(itertools.combinations(S,m))

def do3(L):
	c = len(L)
	val = 0
	for i in xrange(2,c,1):
		S = findsubset(L,i) #could replace with progressive subset finder
		for _i in S:
			if sum(_i) in L:
				val = val + 1
	return val

print "start"
A1 = do1(Q1)
print "done 1"
A2 = do2(Q2)
print "done 2"
A3 = do3(Q3)
print "done"
[A1, A2, A3]
