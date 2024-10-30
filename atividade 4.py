n=int(input('digite o codigo de vericação'))
n1=int(input('digite o total de vendas '))
if(n1 < 100):
    print('a comisão aumentou 0%')
elif(n1 > 100) and (n1 < 350):
    print ('a comição 6%')
    soma=(n1/6)+n1
    print(soma)
elif(n1 > 350):
    print('a comisão aumentou10%')
    soma=(n/10)+n1
    print(soma)