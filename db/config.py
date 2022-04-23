import pymysql


mysql_config = {
    'host': '106.12.204.53',
    'user': 'root',
    'password': 'Anker61#$',
    'port': 3306,
}

def create_connect(database):
    return pymysql.connect(host=mysql_config["host"], 
        port=mysql_config["port"],
        user=mysql_config["user"],
        passwd=mysql_config["password"],
        database=database,
        charset='utf8')
