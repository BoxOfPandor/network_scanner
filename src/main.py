import argparse
from scanner import scan_network
from database import init_db, is_registered
from tui import NetworkScannerApp

def main():
    # Créer le parser d'arguments
    parser = argparse.ArgumentParser(description='Network Scanner')
    parser.add_argument('--interface', '-i', 
                       default='eth0',
                       help='Network interface to scan (default: eth0)')
    
    # Parser les arguments
    args = parser.parse_args()
    
    init_db()
    app = NetworkScannerApp(interface=args.interface)
    app.run()

if __name__ == "__main__":
    main()
