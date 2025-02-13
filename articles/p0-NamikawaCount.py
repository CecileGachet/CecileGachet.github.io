# Online Python compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.
import math

# Number of -1 curves in a smooth del Pezzo surface of degree 1 to 7
# (we indexed the data by the degree of the del Pezzo surface)
pezzo = ("none", 240, 56, 27, 16, 10, 6, 3)


# Count ways to pick a n tuple of disjoint (-1) curves in a general rational elliptic surface, modulo automorphisms of the rational elliptic surface

def label_tuple(n):
    if n == 1:
        return 1
    elif n == 2:
        return label_tuple(1) * pezzo[1] // 2 
        # We pick our first curve (label(1) choices), then we have to pick a (-1) curve on a del Pezzo of Picard rank 9 modulo the automorphisms of the del Pezzo that come from a general rational elliptic surface above it: That group is the Z/2Z acting by fiberwise inversion, which acts freely on the set of (-1) curves on the del Pezzo.
    elif n >= 3 and n <= 8:
        return label_tuple(n - 1) * pezzo[n - 1]
        # We pick our first n - 1 curves, then contract them to get a del Pezzo surface of degree 0 + n - 1 = n - 1. In that del Pezzo surface, we pick our last curve (and since n is larger or equal to 3, no non-trivial automorphism descends from the general rational elliptic surface above)
    elif n == 9:
    	return label_tuple(7) * 2
    	# We pick our first 7 curves, contract them to end up on the del Pezzo surface of degree 7, that is P2 blown up at 2 points. We now have to pick a pair of disjoint (-1) curves in P2 blown up at 2 points. Up to ordering them two, the only way is to pick the two exceptional divisors of that (we cannot pick the strict transform of the line through the two points, since it intersects both exceptional divisors)
    else:
    	raise Exception("Value out of range")

# We also renormalize this function (to keep popping out integers and integers only throughout the program)

def label_renormalized(n):
    return label_tuple(n) // math.factorial(n)
    
    
def label_set(n):
	if n == 2:
		return label_tuple(2) 	# The tuples (l1, l2) and (l2, l1) of (-1) curves are related by the following automorphism: Take l1 as zero section, perform the fiberwise inversion, then perform the translation by l2. Hence, taking 2 tuples of disjoint (-1) curves modulo the automorphism action, we already are counting (l1, l2) and (l2, l1) as one single object. No need to further divide.
	else:
		return label_tuple(n) // math.factorial(n) # For n other than 2, the action of the symmetric group Sn on tuples of disjoint (-1) curves and the action of the automorphism group of the rational elliptic surface commute AND viewing it as Sn acting on the set of tuples modulo automorphsims, there are no stabilizers so all orbits have the same size, which is math.factorial(n). This uses that the rational elliptic surface is general enough that no difference of two disjoint (-1) curves is torsion in the Mordell-Weil group.
    	
# Lists all partitions of an integer n in r positive integers
# TO BE WRITTEN

def partite(n, r):
	if r <= 0 or r > n:
		return []
	elif r == 1:
		return [[n]]
	else:
		list_partite = []
		for i in range(1,n+1):
			aux_list = partite(n - i, r - 1)
			for p in aux_list:
				p.append(i)
				list_partite.append(p)
		return list_partite
 
# Counts, for a fixed Young diagram (given by two lists of the same length drawing the staircase shape), how many ways there are to pick apart subsets of labels for each block column and each block row from some initial set of n row labels and m column labels 

def aux_diagram_contribution(l, n):
	if n == 1 or n == 2:
		return 1 # This is again a consequence of the fact that taking 2 tuples of disjoint (-1) curves modulo the automorphism action, we already are counting (l1, l2) and (l2, l1) as one single object. In other words: Starting from a set of 2 disjoint (-1) curves, either choice of which to label l1 and which to label l2 gives the same data in the end, as we are working up to automorphisms which allow to swap l1 and l2 anyways. See the definition of label_set as well.
	else:	
		r = len(l)
		contrib = math.factorial(n)
		for i in range(r):
			contrib = contrib // math.factorial(l[i])
		return contrib
    	
def diagram_contribution(l1, l2, n, m):
	return aux_diagram_contribution(l1, n) * aux_diagram_contribution(l2, m)
    	
# Count ways to draw Young diagrams with n rows and m columns, and to pick apart subsets of labels for each block column and each block row from initial tuples of n row labels and m column labels (by first turning the tuples in sets, then picking subsets)

def diagrams_and_blocks(n, m):
	total = 0
	for r in range(1, min(n, m)+1):
		possible_block_rows = partite(n, r)
		possible_block_columns = partite(m, r)
		for i in range(len(possible_block_rows)):
			for j in range(len(possible_block_columns)):
				total = total + diagram_contribution(possible_block_rows[i], possible_block_columns[j], n, m)
	return total
    	
def namikawa_P(n, m):
	return label_set(n) * label_set(m) * diagrams_and_blocks(n, m)
	
def namikawa_total():
	total = 0
	for n in range(1, 10):
		for m in range(1, n):
			total = total + 2 * namikawa_P(n, m)
		total = total + namikawa_P(n, n)
	return total

# Output lines, can be changed to display different numbers
	
for n in range(1,10):
	for m in range (1,n+1):
		print((n, m))
		print(int(namikawa_P(n,m)))
		print("\n")
		
print(int(namikawa_total()))