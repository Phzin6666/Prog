caro=0
barato=999
pedidos=0
valorPizza=0
pequena=str("pequena")
média=str("média")
grande=str("grande")
calabresa=str("calabresa")
mussarela=str("mussarela")
tomate=str("tomate")
cebola=str("cebola")
bacon=str("bacon")
S=str("S")
N=str("N")
while True:
    print("Você vai querer uma pizza pequena 20$, média 30$ ou grande 40$?")
    pizza=str(input("Insira: "))
    if pizza == pequena:
        valorPizza=valorPizza+20
    if pizza == média:
        valorPizza=valorPizza+30
    if pizza == grande:
        valorPizza+valorPizza+40
    passagem=str(input("okay! Gostaria de adicionar algum ingrediente extra? S/N: "))
    if passagem == S:
        print("Cada ingrediente extra vale 5$, temos calabresa, mussarela, tomate, cebola e bacon")
        while True:
            extra=str(input("Insira o extra que você quer: "))
            if extra == calabresa or mussarela or tomate or cebola or bacon:
                valorPizza=valorPizza+5
            desejacontinuar=str(input("Deseja continuar? S/N: "))
            if desejacontinuar == N:
                break
    beber=str(input("Deseja beber algo? S/N: "))
    if beber == S:
        valorPizza=valorPizza+8
    print("Seu pedido deu: ",valorPizza)
    pedidonovo=str(input("Deseja fazer um novo pedido? S/N: "))
    if valorPizza > caro:
            caro=valorPizza
    if valorPizza < barato:
            barato=valorPizza
    if pedidonovo == S:
        valorPizza=0
        pedidos+=1
    else:
        print("Pedido mais caro: ", caro)
        print("Pedido mais barato: ",barato)
        break