try:
    as_num = int(input("Ingrese el número de AS BGP: "))
    if 1 <= as_num <= 64511:
        print("El número AS es PÚBLICO.")
    elif 64512 <= as_num <= 65534:
        print("El número AS es PRIVADO.")
    elif as_num == 65535:
        print("El número AS está RESERVADO.")
    else:
        print("Número fuera del rango estándar.")
except ValueError:
    print("Ingrese un número válido.")
