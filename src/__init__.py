from carla import Client

world = None
bla = 12345


def create_client(host: str, port: int) -> Client:
    global world

    client = Client(host, port)

    client.set_timeout(60.0)
    world = client.get_world()
