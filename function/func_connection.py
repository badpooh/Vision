

class ConnectionManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ConnectionManager, cls).__new__(cls)
            cls._instance.connections = {}  # {ip: connection_object}
        return cls._instance

    def connect(self, ip):
        if ip not in self.connections:
            # Example: create a connection object
            self.connections[ip] = self._create_connection(ip)
        return self.connections[ip]

    def _create_connection(self, ip):
        # Simulate connection logic
        print(f"Connecting to {ip}")
        return f"ConnectionObject({ip})"

    def get_connection(self, ip):
        return self.connections.get(ip, None)

    def disconnect(self, ip):
        if ip in self.connections:
            print(f"Disconnecting from {ip}")
            del self.connections[ip]
