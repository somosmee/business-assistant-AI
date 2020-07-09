def is_mongo_up(client):
    containers = client.containers.list()
    for container in containers:
        if container.name == 'mongo_meebot':
            return True
    return False

def setup_env(client):
    if is_mongo_up(client) == False:
        subprocess.run(['docker-compose', 'up', '-d'], cwd='./meebot/')
        subprocess.run(['mongorestore', '--port', '27021', '--db', 'mee', 'dump/mee', '--drop'], cwd='./meebot/db/')
