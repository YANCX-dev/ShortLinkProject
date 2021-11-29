import sqlite3


connect = sqlite3.connect("Links.db")
cursor = connect.cursor()

def regUser(login, password):
    try:
        connect = sqlite3.connect("Links.db")
        cursor = connect.cursor()
        cursor.execute("""INSERT INTO users(login, pass) values(:login, :password)""",
                       {"login": login, "password": password})
        connect.commit()
        return True
    except Exception as e:
        return False

def auth_user(login):
   try:
       connect = sqlite3.connect("Links.db")
       cursor = connect.cursor()
       userData = cursor.execute("""SELECT pass FROM users WHERE login = :login""", {"login": login}).fetchone()
       connect.commit()
       return userData[0]
   except Exception as e:
       return False


def link_entry(user_id, main_link, short_link, link_type):
    try:
        connect = sqlite3.connect("Links.db")
        cursor = connect.cursor()
        cursor.execute("""INSERT INTO links(user_id, link_short, link, type) values(:user_id, :link_short, :link, :type)""",
                       {"user_id": user_id, "link_short": short_link, "link": main_link, "type": link_type})
        connect.commit()
        return True
    except Exception as e:
        return e

def getUserId(login):
    try:
        connect = sqlite3.connect("Links.db")
        cursor = connect.cursor()
        user_id = cursor.execute("""SELECT id FROM users WHERE login = :login""", {"login": login}).fetchone()
        connect.commit()
        return user_id
    except Exception as e:
        return False

def linkExist(user_link):
    try:
        connect = sqlite3.connect("Links.db")
        cursor = connect.cursor()
        returned_link = cursor.execute("""SELECT link_short FROM links WHERE link =:user_link AND type != 'private'""", {"user_link": user_link}).fetchone()
        connect.commit()
        if returned_link:
            return returned_link
        else:
            return False
    except Exception as e:
        return False

def getId(login):
    conn = sqlite3.connect("Links.db")
    cursor = conn.cursor()
    id = cursor.execute('''SELECT id FROM users WHERE login = :login''', {"login": login}).fetchone()
    conn.commit()
    return id


def getFullLink(link_short):
    conn = sqlite3.connect("Links.db")
    cursor = conn.cursor()
    full_link = cursor.execute("""SELECT link From links WHERE link_short = :link_short""", {"link_short": link_short}).fetchone()
    conn.commit()
    return full_link

def getLinkType(link):
    conn = sqlite3.connect("Links.db")
    cursor = conn.cursor()
    type = cursor.execute("""SELECT type From links WHERE link=:link""", {"link": link}).fetchone()
    conn.commit()
    return type

def getUserLinkId(link):
    conn = sqlite3.connect("Links.db")
    cursor = conn.cursor()
    linkUserId = cursor.execute("""SELECT user_id From links WHERE link=:link""", {"link": link}).fetchone()
    conn.commit()
    return linkUserId[0]


connect.commit()
connect.close()