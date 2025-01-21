import platform
import psutil

def print_header(title):
    print(f"\n{'=' * 40}")
    print(f"{title}".center(40))
    print(f"{'=' * 40}")

def get_system_info():
    # Obtiene la información básica del sistema
    system_info = {
        "Sistema Operativo": platform.system(),
        "Versión del SO": platform.version(),
        "Arquitectura": platform.architecture()[0],
        "Procesador": platform.processor(),
        "Versión de Python": platform.python_version()
    }
    
    # Imprime la información
    print_header("INFORMACIÓN DEL SISTEMA")
    for key, value in system_info.items():
        print(f"{key}: {value}")
    
def check_disk_usage():
    # Obtiene el estado del disco
    disk = psutil.disk_usage('/')
    status = "OK"
    if disk.percent > 85:
        status = "Advertencia"
    if disk.percent > 95:
        status = "Falla"

    print_header("ESTADO DEL DISCO PRINCIPAL")
    print(f"Total: {disk.total / (1024 ** 3):.2f} GB")
    print(f"Usado: {disk.used / (1024 ** 3):.2f} GB")
    print(f"Libre: {disk.free / (1024 ** 3):.2f} GB")
    print(f"Porcentaje de uso: {disk.percent}%")
    print(f"Estado: {status}")

    return status

def check_cpu_usage():
    # Obtiene información de la CPU
    cpu_info = psutil.cpu_freq()
    cpu_usage = psutil.cpu_percent(interval=1)
    status = "OK"
    
    if cpu_usage > 80:
        status = "Advertencia"
    if cpu_usage > 90:
        status = "Falla"
        
    print_header("ESTADO DE LA CPU")
    print(f"Frecuencia máxima: {cpu_info.max:.2f} MHz")
    print(f"Frecuencia actual: {cpu_info.current:.2f} MHz")
    print(f"Porcentaje de uso: {cpu_usage}%")
    print(f"Estado: {status}")

    return status

def check_memory_usage():
    # Obtiene el estado de la memoria
    memory = psutil.virtual_memory()
    status = "OK"
    
    if memory.percent > 85:
        status = "Advertencia"
    if memory.percent > 95:
        status = "Falla"
    
    print_header("ESTADO DE LA MEMORIA")
    print(f"Total: {memory.total / (1024 ** 3):.2f} GB")
    print(f"Usada: {memory.used / (1024 ** 3):.2f} GB")
    print(f"Libre: {memory.available / (1024 ** 3):.2f} GB")
    print(f"Porcentaje de uso: {memory.percent}%")
    print(f"Estado: {status}")
    
    return status

def check_usb_usage():
    # Obtiene información de los dispositivos USB conectados
    print_header("ESTADO DE LOS DISPOSITIVOS USB")
    partitions = psutil.disk_partitions()
    usb_found = False
    
    for partition in partitions:
        if 'removable' in partition.opts:  # Detecta dispositivos extraíbles (USB)
            usb_found = True
            usb_disk = psutil.disk_usage(partition.mountpoint)
            status = "OK"
            
            if usb_disk.percent > 85:
                status = "Advertencia"
            if usb_disk.percent > 95:
                status = "Falla"

            print(f"\nUSB encontrado en: {partition.device}")
            print(f"Total: {usb_disk.total / (1024 ** 3):.2f} GB")
            print(f"Usado: {usb_disk.used / (1024 ** 3):.2f} GB")
            print(f"Libre: {usb_disk.free / (1024 ** 3):.2f} GB")
            print(f"Porcentaje de uso: {usb_disk.percent}%")
            print(f"Estado: {status}")
    
    if not usb_found:
        print("No se detectaron dispositivos USB conectados.")

def generate_report(disk_status, cpu_status, memory_status, usb_status):
    print_header("INFORME FINAL")
    print(f"Estado del Disco Principal: {disk_status}")
    print(f"Estado de la CPU: {cpu_status}")
    print(f"Estado de la Memoria: {memory_status}")
    print(f"Estado de los Dispositivos USB: {usb_status}")

    if "Falla" in [disk_status, cpu_status, memory_status, usb_status]:
        print("\n¡Atención! Se han detectado problemas en el sistema. Se recomienda revisar los puntos con estado 'Falla'.")
    elif "Advertencia" in [disk_status, cpu_status, memory_status, usb_status]:
        print("\nAdvertencia: Algunos componentes del sistema tienen un rendimiento subóptimo. Revisa las recomendaciones.")
    else:
        print("\nEl sistema está funcionando correctamente sin problemas detectados.")

def main():
    print("Iniciando diagnóstico del sistema...\n")
    
    # Recolectar información
    get_system_info()
    disk_status = check_disk_usage()
    cpu_status = check_cpu_usage()
    memory_status = check_memory_usage()
    check_usb_usage()
    
    # Generar el informe final
    generate_report(disk_status, cpu_status, memory_status, "OK")  # USB ya fue revisado por sí mismo
    
    # Esperar para que el diagnóstico no se cierre rápidamente
    input("\nPresiona Enter para salir...")

if __name__ == "__main__":
    main()
