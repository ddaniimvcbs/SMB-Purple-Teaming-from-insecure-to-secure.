# Configuración del servidor (protegido)

# Entorno
## Sistema operativo: Ubuntu Server 26.04.1 
## Máquina virtual: VirtualBox
## Versión de Samba: ver4.23.6

# Configuración del servidor (smb.conf)

La configuración establece SMB3 como protocolo mínimo, exige el cifrado y la firma de los mensajes SMB, deshabilita NetBIOS y define una carpeta compartida con acceso restringido a un grupo de usuarios.

```ini
[global]
    # Seguridad del protocolo SMB
    server min protocol = SMB3
    client min protocol = SMB3
    smb encrypt = required
    server signing = mandatory

    # Identificación del servidor
    workgroup = WORKGROUP
    server string = %h serversmb ()

    # Deshabilitar NetBIOS
    disable netbios = yes

    # Configuración de red
    interfaces = 192.168.0.0/24,127.0.0.0/8 enp0s3
    bind interfaces only = yes

    # Registros y depuración
    log level = 3
    log file = /var/log/samba/log.%m
    max log size = 1000
    logging = file
    panic action = /usr/share/samba/panic-action %d

    # Autenticación
    server role = standalone server
    obey pam restrictions = yes
    unix password sync = yes
    passwd program = /usr/bin/passwd %u
    passwd chat = *Enter\snew\s*\spassword:* %n\n *Retype\snew\s*\
    spassword:* %n\n *password\supdated\ssuccessfully* .
    pam password change = no
    map to guest = Never
    restrict anonymous = 2
    usershare allow guests = no

# Carpeta compartida
[principal]
    path = /srv/samba/principal
    browseable = yes
    read only = no
    valid users = @dnmvsamba
    create mask = 0660
    force create mode = 0660
    directory mask = 0770
    force directory mode = 0770
```

