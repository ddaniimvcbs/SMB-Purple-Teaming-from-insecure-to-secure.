import sys      #Libreria para interactuar directamente con el interpreter de Python y el OS
import subprocess   # Libreria de Python para ejecutar comandos como si estuvieramos en la terminal
import re           # Herramienta para buscar, extraer, reemplazar patrones de texto dentro de cadenas de texto
                      #(usado principalmente para quitar caracteres ANSI del texto de enum4linux)




#Funcion para mostrar el menú:
def menu_principal():
    print("-" * 30)
    print("AUDITORIA SERVIDORES SMB V0.2")
    print("-" * 30)
#----------------------------------------





#Funcion mostrar menu con resultados

def menu_resultados(resultados):

    categorias = {
        "1": "smb",
        "2": "NetBIOS",
        "3": "sistema operativo",
        "4": "otros"
    }

    while True:

        print("""
        ╔════════════════════════════════════════════════════════════╗
                                RESULTADOS                          
        ║  1.) SMB                3.) Informacion OS                 ║
        ║  2.) NetBIOS            4.) Otros              0.) VOLVER  ║

        ╚════════════════════════════════════════════════════════════╝
        """)

        opcion = input("Introduce tu opción: ")

        if opcion in categorias:
            
            for linea in resultados[categorias[opcion]]:
                
                print(linea)

        
        elif opcion == "0":
            
            
            break

        
        else:
            
            print("Opción no válida")




#Funcion para sacar los resultados, en un diccionario
def sacar_resultados_texto(texto_comando_con_split):

    resultados = {
    "smb":                  [],
    "NetBIOS":                  [],
    "sistema operativo":                    [],
    "otros":                                []
                                            }
     



    patron_ansi = re.compile(r'\x1b\[[0-9;]*m')              #Expresion regular para detectar codigos ANSI


     
     
    for linea in texto_comando_con_split:                   

        lineas_stripeadas = patron_ansi.sub("", linea)        #Creamos un str nuevo para quitar los patrones ansi de las lineas
        

        if "SMB" in lineas_stripeadas:

            resultados["smb"].append(lineas_stripeadas)

        
        elif "NetBIOS" in lineas_stripeadas:

            resultados["NetBIOS"].append(lineas_stripeadas)

        
        
        elif  "OS" in lineas_stripeadas:

            resultados["sistema operativo"].append(lineas_stripeadas)
        
        
        else:

            resultados["otros"].append(lineas_stripeadas)


    
    return resultados



#Funcion para comprobar los puertos cogiendo como parametros una ip y los puertos que el usuario elija
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




#Funcion que ejecuta e4linux sobre la ip introducida
def ejecutar_e4linuxng(ip_introducida):

    print("Ejecutando enumeracion completa simple con enum4linux...")
    
    #Ejecutamos el comando con subprocess.run y capturamos literalmente lo que la terminal de linux mostraria

    comando_e4linuxng = subprocess.run(["enum4linux-ng", "-A" , ip_introducida], capture_output = True, text = True)

    #Nos llevamos el texto

    texto_comando_con_split = comando_e4linuxng.stdout.strip().splitlines()

    
    
    return texto_comando_con_split
#-----------------------------------------------------------------------------------------------------------------------








#Code:





#Muestra el menu

menu_principal()






#Guardar IP introducida y puertos introducidos, y hacemos tupla
puertos_smb = ("139","445")
ip_introducida = input("Introduce una dirección IP o dominio: ")
puertos_introducidos = input("Introduce que puertos deseas escanear (139,445 o ambos), escribelos separados por coma (PUERTO,PUERTO) solo se admiten los anteriores mencionados: ")



# Guardamos los puertos que ha introducido el usuario, aplicandoles un metodo de separacion por coma.
puertos_introducidos_formateados = puertos_introducidos.split(",")  



#Bucle para recorrer cada puerto de los puertos introducidos ya formateados/spliteados
for puerto in puertos_introducidos_formateados:

    puerto = puerto.strip()                      #Por si acaso alguien introduce un espacio antes del puerto, esto quita los espacios a izquierdas y derechas de las str 

    if puerto not in puertos_smb:

        print(f"No puedes usar puertos que no sean 139 o 445...")
        sys.exit()





#Guarda resultado de los puertos y comprueba los introducidos

resultado_puertos = comprobar_puertos(ip_introducida,puertos_introducidos)


#Mostramos resultado puertos y la ip introducida
print(f"IP: >{ip_introducida}<   >Estado de los puertos: {resultado_puertos}")




# Guardamos el texto spliteado de la funcion ejecutar_e4linuxng
texto_comando_con_split = ejecutar_e4linuxng(ip_introducida)





#Guardamos los resultados 
resultados = sacar_resultados_texto(texto_comando_con_split)





#Ejecutamos el menu de los resultados
menu_resultados(resultados)








