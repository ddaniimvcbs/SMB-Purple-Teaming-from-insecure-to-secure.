import sys      #Libreria para interactuar directamente con el interpreter de Python y el OS
import subprocess   # Libreria de Python para ejecutar comandos como si estuvieramos en la terminal



#----------------------------------------
#Funcion para mostrar el menú:

def menu_principal():
    print("-" * 30)
    print("AUDITORIA SERVIDORES SMB V0.1")
    print("-" * 30)

#---------------------------------------




def formatear_resultados(texto_comando_spliteado):
    
     print("=" * 20)
     print("|     RESULTADOS    |")
     print("=" * 20)

     
     
     #Lista de variables que contienen las respuestas guardadas.
     
     protocolos_aceptados = []
     protocolo_preferido = []
     solo_smb1 = []
     inicio_sesion_requerido = []
     miniresultados_netbios = []
     informacion_os = []
     

    

    
    #Bucle iterando sobre el numero de linea(guia) y el texto correspondiente de la linea (linea)
    

     for guia, linea in enumerate(texto_comando_spliteado, start=1):




        # Va buscando las linea que contiene las versiones de protocolos aceptados y los mete en la lista de protocolos_aceptados
    
        
        if "[+] Supported dialects and settings:" in linea:

            

            continue

        if "SMB 1.0:" in linea:

            protocolos_aceptados.append(linea)

            continue


        
        if "SMB 2.0.2:" in linea:

            protocolos_aceptados.append(linea)

            continue


        if "SMB 2.1:" in linea:

            protocolos_aceptados.append(linea)

            continue


        if "SMB 3.0:" in linea:

            protocolos_aceptados.append(linea)

            continue

        
        if "SMB 3.1.1:" in linea:

            protocolos_aceptados.append(linea)
            
            continue

        if "Preferred dialect:" in linea:

            protocolo_preferido.append(linea)

            continue

        
        if "SMB1 only:" in linea:

            solo_smb1.append(linea)

            continue

        
        if "SMB signing required:" in linea:

            inicio_sesion_requerido.append(linea)

            continue


        if "NetBIOS" in linea:

            miniresultados_netbios.append(linea)

            continue

     resultados = [protocolos_aceptados , protocolo_preferido , solo_smb1 , inicio_sesion_requerido , miniresultados_netbios , ]
     
     return resultados

     



#----------------------------------------------------------------------------------------------------------------
# Definimos funcion para comprobar los puertos cogiendo como parametros una ip y los puertos que el usuario elija

def comprobar_puertos(ip_introducida,puertos_introducidos):     

    
    
    
    
    puertos_introducidos = str(puertos_introducidos)  # Convertimos los puertos del input a tipo str
    
    


    lista_puertos = puertos_introducidos.split(",")  # Convertimos los puertos a una lista y los spliteamos con una coma

    
    
    
    resultado_puertos = subprocess.run(["sudo" , "nmap" , "-Pn" , "-n" , "-sS" , "-p" , puertos_introducidos , ip_introducida], capture_output = True , text = True) #Ejecuta el comando de nmap y devuelve el lo que escupe la terminal en string
    

    
    texto_formateado = resultado_puertos.stdout.splitlines()      # Spliteamos el texto en lineas y los metemos en una lista
     

    estado_puertos = []        # Creamos una lista que contendra el valor de cada puerto





    for puerto in lista_puertos:         #Bucle para recorrer cada puerto de la lista de puertos

       puerto = puerto.strip()    # Quitamos los espacios en blanco, por si los hay

       for linea in texto_formateado:    # Bucle para recorrer cada linea de la lista del texto del comando de nmap

        # Condiciones con la lista de puertos formateada y las lineas del texto del comando de nmap
            
            if f"{puerto}/tcp" in linea and "open|filtered" in linea: 

                estado_puertos.append (f"{puerto} - abierto/filtrado")

                break

            
            elif f"{puerto}/tcp" in linea and "open" in linea:

                estado_puertos.append (f"{puerto} - abierto")

                break

            
            elif f"{puerto}/tcp" in linea and "filtered" in linea:

                estado_puertos.append (f"{puerto} - filtrado")

                break

            
            
            elif f"{puerto}/tcp" in linea and "closed" in linea:

                estado_puertos.append(f"{puerto} - cerrado")

                break


                

            
    #Devolvemos el estado de los puertos (la lista)       
     
    return estado_puertos

#------------------------------------------------------------------------------------------------------------------




#--------------------------------


#Funcion que ejecuta e4linux sobre la ip introducida

def ejecutar_e4linuxng(ip_introducida):

    print("Ejecutando enumeracion completa simple con enum4linux...")
    
    #Ejecutamos el comando con subprocess.run y capturamos literalmente lo que la terminal de linux mostraria

    comando_e4linuxng = subprocess.run(["enum4linux-ng", "-A", "-C" , ip_introducida], capture_output = True, text = True)

    #Nos llevamos el texto spliteado en lineas:

    texto_comando_spliteado = comando_e4linuxng.stdout.splitlines()

    return texto_comando_spliteado

    


  



#-------------------------------------------------------------------------------------------



#Muestra el menu


menu_principal()





#Guardar IP introducida y puertos introducidos, y hacemos una tupla para que permitir solo escanear puertos SMB

puertos_smb = ("139","445")
ip_introducida = input("Introduce una dirección IP o dominio: ")
puertos_introducidos = input("Introduce que puertos deseas escanear (139,445 o ambos), escribelos separados por coma (PUERTO,PUERTO) solo se admiten los anteriores mencionados: ")




puertos_introducidos_formateados = puertos_introducidos.split(",")  # Formateamos el texto de los puertos introducidos por el usuario para separarlo en comas


#VALIDACIONES:


#Bucle para recorrer cada puerto de los puertos introducidos ya formateados/spliteados

for puerto in puertos_introducidos_formateados:

    puerto = puerto.strip()

    if puerto not in puertos_smb:

        print(f"No puedes usar puertos que no sean 139 o 445...")
        sys.exit()

#--------------------------------------------------------







#Funcion para comprobar si los puertos estan abiertos, filtrados o cerrados:

resultado_puertos = comprobar_puertos(ip_introducida,puertos_introducidos)

print(f"IP:{ip_introducida}  Estado de los puertos: {resultado_puertos}")


# Guardamos el texto spliteado de la funcion ejecutar_e4linuxng
texto_comando_spliteado = ejecutar_e4linuxng(ip_introducida)



#Formatear texto del comando enum4linux-ng:

resultados = formatear_resultados(texto_comando_spliteado)


#Bucles para mostrar los resultados:


# 1. Protocolos aceptados


print("Protocolos aceptados:")


for resultado in resultados[0]:
    print(resultado.strip())

# 2. Protocolo prefereido

print("\nProtocolo preferido:")


for resultado in resultados[1]:
    print(resultado.strip())

# 3. ¿Acepta solo SMBV1?

print("\n¿Acepta solo SMBV1?:")


for resultado in resultados[2]:
    print(resultado.strip())

# 4. ¿Requiere login?

print("\n¿Requiere loguin?:")

for resultado in resultados[3]:
    # Aqui eliminamos el código de color \x1b[0m del final si existe
    print(resultado.replace("\x1b[0m", "").strip())

# Info NetBios

print("\nInformacion obtenida de NetBios:")


for resultado in resultados[4]:
    print(resultado.strip())
















