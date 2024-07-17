n = int(input())

def is_abundant(n):
    Uoc_cua_n = []
    for i in range(1,n):
        if n % i == 0 :
            Uoc_cua_n.append(i)
            
    if sum(Uoc_cua_n) > n :
        return True
    else : 
        return False
    
print(is_abundant(n))




