
import readline


f = open("e", "r")
e1 = f.readline()
e1 = e1[2:]
found = False

def check_prime(e):
    if e % 2 == 0 or e% 3 == 0 or e%5 == 0:
        return False
    else:
        return ciure(e)

def ciure(e):
    c = [True for x in range(e +1)]
    c[1] = False
    j = 2

    while j<= 100000:
        if (i % j == 0):
            return False
        j +=2
    
    
    return True




while not found:
    e1 += f.readline()
    e1.replace('\n', '')
    while len(e1) >= 10:
        i = 0
        while i < len(e1) - 11:
            e = e1[i:i + 10]
            print(e)
            found = check_prime(int(e))
            print(found)
            if found: 
                print(e)
                break
            i+=1
        if found: break
    
print(e1)