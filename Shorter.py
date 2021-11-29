import sqlite3

import flask
from flask import Flask,redirect
from flask import request
from flask import jsonify
import jwt
import dbHandler
import bcrypt

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended import get_jwt




app = Flask(__name__)
# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "linksecret"
jwt_create = JWTManager(app)


# Регистрация
@app.route('/registration', methods=["POST"])
def register():
    login = request.json.get("login", None)
    password = request.json.get("password", None)
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password.encode("utf-8"), salt)
    try:
        dbHandler.regUser(login, password_hash)
    except Exception as e:
        print(e)
    print(login, password)
    return {"ok": 200}



# Авторизация
@app.route('/authorization', methods=["POST"])
def auth():
    login = request.json.get('login', None)
    password = request.json.get('password', None)
    try:
        hashed_pass = dbHandler.auth_user(login)
        if not bcrypt.checkpw(password.encode("utf-8"), hashed_pass):
            auth_res = "Your password isn't valid"
        else:
            id = dbHandler.getUserId(login)
            user_data = {"user_id": id[0]}
            print(user_data)
            access_token = create_access_token(identity=login, additional_claims=user_data)
            return jsonify(access_token=access_token)
        return auth_res
    except Exception as e:
        print(e)
    return {"ok": 200}


# Создание ссылки
@app.route('/links', methods=["POST"])
@jwt_required(optional=True)
def link():
    if bool(get_jwt()):
        user_id = get_jwt()["user_id"]
    else:
        user_id = None
    # DATA ######################################################
    user_link = request.json.get('user_link', None)
    link_type = request.json.get('link_type', None)
    user_link_name = request.json.get('user_link_name', None)
    salt = bcrypt.gensalt()
    hash_link = bcrypt.hashpw(user_link.encode("utf-8"), salt)
    short_link_hash = hash_link[8:20]
    short_Link = short_link_hash.decode("utf-8")
    #############################################################
    if not user_link_name:
        if dbHandler.linkExist(user_link):
            returned_link = dbHandler.linkExist(user_link)
            print(returned_link)
        else:
            dbHandler.link_entry(user_id, user_link, short_Link, link_type)
            print("Ссылка добавлена")
    else:
        if dbHandler.linkExist(user_link):
            returned_link = dbHandler.linkExist(user_link)
            print(returned_link)
        else:
            try:
                print(dbHandler.link_entry(user_id, user_link, user_link_name[0:8], link_type))
            except Exception as e:
                print(e)
            print("Ссылка добавлена")
    return {"ok" : 200}



@app.route('/<shortUrl>', methods=["GET"])
@jwt_required(optional=True)
def getUrl(shortUrl):
    if bool(get_jwt()):
        user_id = get_jwt()["user_id"]
    else:
        user_id = None
    full_link = dbHandler.getFullLink(shortUrl)[0]
    link_type = dbHandler.getLinkType(full_link)[0]
    print("LinkType:" + link_type)
    print(full_link)
    if link_type == "public":
        return redirect(str(full_link), code=302)
    elif link_type == "private":
        linkUserId = dbHandler.getUserLinkId(full_link)
        if linkUserId == get_jwt()["user_id"]:
            print(get_jwt()["user_id"])
            return redirect(str(full_link), code=302)
        else:
            print("Вы не владелец ссылки!")
    elif link_type == "authorized":
        print(get_jwt())
        if get_jwt()["user_id"]:
            return redirect(str(full_link), code=302)
        else:
            print("Вы не авторизованы!")
    return {"ok":200}


















if __name__ == '__main__':
    app.run()






