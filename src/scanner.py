import subprocess
import sys
import netifaces

def get_network_interfaces():
    try:
        return netifaces.interfaces()
    except Exception as e:
        print(f"Error getting interfaces: {e}", file=sys.stderr)
        return []

def scan_network(interface='eth0'):  # Ajout du paramètre interface avec valeur par défaut
    try:
        # Utiliser sudo avec arp-scan avec l'interface spécifiée
        result = subprocess.run(
            ["sudo", "arp-scan", f"--interface={interface}", "--localnet"], 
            capture_output=True, 
            text=True
        )
        if result.returncode != 0:
            print(f"Error running arp-scan: {result.stderr}", file=sys.stderr)
            return []
            
        devices = []
        for line in result.stdout.split("\n"):
            parts = line.split("\t")
            if len(parts) >= 3:
                ip, mac, vendor = parts[:3]
                devices.append((ip, mac, vendor))
        return devices
    except Exception as e:
        print(f"Scanning error: {e}", file=sys.stderr)
        return []
