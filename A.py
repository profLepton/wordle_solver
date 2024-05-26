
l = ["Akshay", "Nandinis", ]

freq = {}


#word list = ['fat', 'cat']
# ('a') letter is the key --> [ 0, 2, 0, 0, 0] is the value

freq['a'] = [1, 1, 0, 0, 1, 0, 0, 0]
freq['k'] = [0, 1, 0, 0, 0, 0, 0, 0]
freq['s'] = [0, 0, 1, 0, 0, 0, 0, 1] = 1
....

i = 7
letter = s

for letter in



a (undefined) = a + 1

# first time you see 's'

freq['s'] = freq.get('s', [0]*5)[i] + 1


# First time we see s
step 1 --> freq.get('s', [0] * 5) returns [0, 0, 0, 0, 0]
step 2 -->  [0, 0, 0, 0, 0][i] return 0
step 3 --> 0 + 1 = 1
step 4 --> freq['s'] = 1

# second time

step 1 --> freq.get('s', [0] * 5) returns 1
step 2 -->  1[i] return 0





for i, letter in enumerate(word):
    # i = 2
    #Holds a list
    variable = freq.get(letter, [0]*5) # [0,0,0,0,0]
    variable[i] += 1 #[0,0,1,0,0]
    freq[letter] = variable 




