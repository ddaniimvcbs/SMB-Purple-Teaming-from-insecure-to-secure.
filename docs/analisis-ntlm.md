-*-*-*-*-*-*-*- LEER -*-*-*-*-*-*-*

Kerberos Queda fuera del alcance de este documento (de momento) porque mi laboratorio actual usa Samba independiente, sin dominio

-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*



Voy a empezar explicando porque surgió este método de autentificación, y sus orígenes (me parecen bastante interesantes)


Aclarar que, casi nunca, por obvios métodos de seguridad, se suelen guardar contraseñas en texto plano. En su lugar se guardan los hashes.


Antes de NTLM como sistema y método de autenticación, se usó LM (Lan Manager):

Lan Manager era un sistema de autenticacion antiguo de Windows, el cual lo "único" que hacia era pasar el texto a mayúsculas, haciendo que, por ejemplo "Clave123" y "clave123", generáran el mismo hash (creo que aqui no tendréis mucha perdida, aunque cambie la posicion de mayúsculas y minúusculas en el texto..). Encima no solo eso:

- Si la contraseña era mas corta de 14 caracteres, se añadían bytes nulos hasta llegar a los 14.
- Luego, partía la contraseña en 2 trozos independientes de 7 caracteres

  En realidad, para obtener esa contraseña, no era necesario descifrar los 14 caracteres. Solo tenian que adivinar dos bloques de 7 caracteres INDEPENDIENTES, que solo estaban compuestos por mayusuculas y numeros.. (fatidico). De hecho, gracias a esto surgieron las "Rainbow Tables"


  Tras esto, llegó su sucesor (aunque ya esta reemplazado por Kerberos..), NTLM.


  NTLM propuso un sistema de desafio, entre otras cosas, que lo hizo bastante mas fuerte que LM:

  - Respeta mayusculas y minusculas, es decir, no es lo mismo el hash de "Clave123" que el de       "clave123"
 
  - NO se parte a la mitad, se junta todo en un solo bloque
 
  - Soporta contraseñas larguiiiisimas
 
  - Las Rainbow Tables se volvieron practicamente inutiles, por el increible numero de hashes       en total de cada contraseña posible
 

  NTLMv2 es la version mas actual de este protocolo, entre sus diferencias con la 1 version, ofrece:


  - Un algoritmo criptografico mucho mas seguro (HMAC-MD5) que su antecesor (DES)
 
  - Un numero aleatorio para el cliente (Client Nonce): El cliente añade su propio numero al desafio
 
  - Un "timestamp" que caduca en unos minutos
 

Esto hace que el hash sea mucho mas grande y único en una marca de tiempo inviable (hablamos de milisegundos). Tambien hace que ya no se pueda crackear tan a la ligera, si tiene mas de 10 caracteres o asi.. olvidarse es lo mejor.





*IMPORTANTE*: NTLMv2 ya es anticuado. A dia de hoy, se usa Kerberos, que es el protocolo de autenticación principal en los entornos Windows.








--------------------------------------------------------------------------------------------
Vamos a ver el proceso de una autenticacion NTLMv2 en mi propio servidor SMB, usaremos claro está, Wireshark.


Paso 1 (CLIENTE >>> SERVIDOR)


<img width="1409" height="910" alt="imagen" src="https://github.com/user-attachments/assets/528308f5-62ad-4298-8cec-68e37ef1f6f1" />



En el primer paquete (NTLMSSP_NEGOTIATE), cliente saluda al servidor, acuerdan version SMB, firma y cifrado:



<img width="1296" height="677" alt="imagen" src="https://github.com/user-attachments/assets/03f2695f-a82a-4e41-820e-43058376b56a" />












Segundo paquete (STATUS_MORE_PROCESSING_REQUIRED):

Quiere decir que el servidor necesita mas informacion (que nos autentiquemos) y nos manda el desafio (NTLMSSP_CHALLENGE):



<img width="1467" height="679" alt="imagen" src="https://github.com/user-attachments/assets/792a866f-30fb-462a-94dc-0e6b9354da8c" />







En este punto la contraseña ha sido pasada a un hash, y se mezclará con el NTLM Server Challenge que acaba de mandar el servidor. Aquí ya la contraseña en texto plano es imposible de ver, se ha convertido en hash y se combina con el desafío.

El servidor, por su parte, ya tiene guardado el hash de la contraseña de ese usuario desde que fue dado de alta en Samba. Cuando le llega la respuesta del cliente, el servidor coge ese hash guardado y lo mezcla con el mismo desafío que él mismo mandó. Si el resultado de esa mezcla coincide con lo que le llegó del cliente, se inicia sesión con éxito; si no, queda rechazado.





<img width="1409" height="795" alt="imagen" src="https://github.com/user-attachments/assets/4ff625e6-e5e2-4fcf-9c78-6705ea26f8f9" />



Aqui,en NT Status: vemos STATUS_SUCCESS (logueado con éxito)



















 

 

