class Kanitham:
    def koottu(a,b):
        print("Koottugiren...")
        print(f'{a}+{b}={a+b}')

    def kazhi(a,b):
        print("Kazhikkiren...")
        print(f'{a}-{b}={a-b}')

    def perukku(a,b):
        print("Perukkuhiren...")
        print(f'{a}*{b}={a*b}')

    def vahu(a,b):
        if b!=0:
            print("Vahukkiren...")
            print(f'{a}/{b}={a/b}')
        else:
            print("Second value shouldn't be ZERO! Try again!")