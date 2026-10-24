import subprocess   # Libreria de Python para ejecutar comandos como si estuvieramos en la terminal
import re           # Herramienta para buscar, extraer, reemplazar patrones de texto dentro de cadenas de texto (usado principalmente para quitar caracteres ANSI del texto de enum4linux)
import ipaddress    # Libreria para crear, manipular y operar sobre direcciones IP
import sys          # Libreria para interactuar directamente con el interprete de Python



#Funcion para mostrar el menú:
def menu_principal():
    print("-" * 30)
    print("AUDITORIA SERVIDORES SMB V0.3")
    print("-" * 30)
#----------------------------------------

#Funcion mostrar menu con resultados
def menu_resultados(resultados):

    #*FALLO* Al depender de enum4linux, si enum4linux no puede hacer la condicion de abajo, fallara y no podra ejecutarse.. la explicacion la detallo abajo.
    
    for linea in resultados["smb"]:

        if "Could not connect to SMB" in linea:

            print("Enum4Linux no ha podido completar el handshake a traves de los dialectos del servidor disponibles, tuberias rpc..(en algun punto, enum4linux ha fallado en esto,saliendo...)")

            sys.exit()

        
        else:

            pass


    
    
    categorias = {
        "1": "smb",
        "2": "NetBIOS",
        "3": "sistema_operativo",
        "4": "otros",
        "5": "Guardar en txt"
                                  }

    while True:

        print("""
        ╔═══════════════════════════════════════════════════════════════════╗
                                RESULTADOS                          
        ║  1.) SMB                3.) Informacion OS     5.) Guardar en txt ║          
        ║  2.) NetBIOS            4.) Otros              0.) Salir          ║

        ╚═══════════════════════════════════════════════════════════════════╝
        """)

        opcion = input("Introduce tu opción: ")

        
        if opcion == "5":
                
                with open("resultados_smb.txt" , "w" , encoding="utf-8") as archivo:

                 archivo.write(f"--RESULTADOS--\n")
                    
                 for clave,datos in resultados.items():
                   
                    archivo.write(f"\n══════════════")
                    archivo.write(f"\n{clave.upper()}\n")
                    archivo.write(f"════════════════\n")

                    for linea in datos:

                         
                         
                         if linea == "SMB1 only: true":

                            archivo.write(f"\n ****MUY CRITICO*****: SMB1 SOLO ACEPTADO")

                        
                        
                        
                         elif not linea.startswith(","):

                            archivo.write(f"\n{linea}")
                                      




                print("Archivo guardado con exito")
                input('Pulsa "Enter" para continuar... ')



        elif opcion in categorias:
            
            
            for linea in resultados[categorias[opcion]]:
                
                print(linea)
        
            input('Pulsa "Enter" para continuar..')

                 

        
        elif opcion == "0":

            
            
            break

        
        
        
        else:
            
            print("Opción no válida")
            input('Pulsa "Enter" para continuar..')
            
#-------------------------------------------------------
#Funcion para sacar los resultados, en un diccionario
def sacar_resultados_texto(texto_comando_con_split):

    resultados = {
    "smb":                  [],
    "NetBIOS":                  [],
    "sistema_operativo":                    [],
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

            resultados["sistema_operativo"].append(lineas_stripeadas)
        
        
        else:

            resultados["otros"].append(lineas_stripeadas)


    
    return resultados
#----------------------------------------------------------------------------------------------------

#Funcion para comprobar si la IP es valida dentro de la funcion ejecutar_e4linuxng
def comprobar_ip(nueva_ip_introducida):
    
    while True:

          try:

            ipaddress.ip_address(nueva_ip_introducida)

            return (nueva_ip_introducida)

           
          except ValueError:
            
            nueva_ip_introducida = input("¡IP Invalida! Escribela de nuevo: ")

#Funcion que ejecuta e4linux sobre la ip introducida
def ejecutar_e4linuxng(ip_introducida):

    
    
    print("Ejecutando enumeracion completa simple con enum4linux...")
    
    
    
    #Ejecutamos el comando con subprocess.run y capturamos algun error si los hay:
    while True: 
     
     
     try:
            #Ahora los errores tambien salen por la salida normal del comando y asi depuro mejor los errores en la funcion que muestra el menu con los resultados

            comando_e4linuxng = subprocess.run(["enum4linux-ng", "-A" , ip_introducida], timeout=60, capture_output=True, text = True)
            
            
            
            texto_comando_con_split = comando_e4linuxng.stdout.strip().splitlines()  
            return texto_comando_con_split
    
       
    
    
     except FileNotFoundError:            #Por si no esta enum4linux instalado

        
        print("Error: enum4linux-ng no esta instalado en tu sistema... instalalo con 'sudo [tu gestor de paquetes] [argumento] enum4linux-ng'")

        return None

        break

     
       
     
     except subprocess.TimeoutExpired:                            #Errores por timeout

           while True:

            print("EL TIEMPO DE ESPERA SE CUMPLIO, PUEDE DEBERSE A DIVERSOS MOTIVOS: IP valida sin ruta asignada (la ip existe pero no se puede llegar a ella)")
            print(f"¿Quieres volver a intentarlo?    1. Si      2. No")

            opcion = input()

            
            if opcion == "1":

                ip_introducida = comprobar_ip(input("Introduce de nuevo la IP: "))

                break
                            

            
            
            elif opcion == "2":

                sys.exit()

            
            
            else:


                print("Opcion invalida, selecciona '1' o '2'")
#-----------------------------------------------------------------------------------------------------------------------



#Code:





#Muestra el menu

menu_principal()


#Guardamos la ip introducida, y comprobamos que sea una IP valida

ip_introducida = comprobar_ip(input("Introduce una dirección IP: "))



# Guardamos el texto spliteado de la funcion ejecutar_e4linuxng
texto_comando_con_split = ejecutar_e4linuxng(ip_introducida)



#Comparamos entidad, valor no
if texto_comando_con_split is None:                     

    sys.exit()





#Guardamos los resultados 
resultados = sacar_resultados_texto(texto_comando_con_split)




#Ejecutamos el menu de los resultados
menu_resultados(resultados)







