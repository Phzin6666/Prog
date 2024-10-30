x=int(input("Informe um Número: "))
y=int(input("Informe outro Número: "))
z=int(input("Informe mais um Número: "))
if(x<y<z):
    print("Ordem crescente: ",x,y,z)
if(x<z<y):
    print("Ordem crescente: ",x,z,y)
if(y<x<z):
    print("Ordem crescente: ",y,x,z)
if(y<z<x):
    print("Ordem crescente: ",y,z,x)
if(z<x<y):
    print("Ordem crescente: ",z,x,y)
if(z<y<x):
    print("Ordem crescente: ",z,y,x)