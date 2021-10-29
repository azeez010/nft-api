import os
from base64 import b64encode
from flask import request, jsonify
from models.init import app, db
from models.store import Address, Referral
from config.config import REWARD, WITHDRAW_MIN
from utils import is_address, remove_symbols

from flask_cors import CORS

cors = CORS(app, resources={"*": {"origins": "*"}})

@app.route("/is-address-valid", methods=["GET"])
def check_address():
    address = request.args.get("address")
    check_address = is_address(address)
    return jsonify({"addressValid": check_address})

@app.route("/ref/<code>", methods=["GET", "POST"])
def refer(code: str):
    if request.method == "POST":
        address = request.json.get("address")
        
        address_info = Address.query.filter_by(address=address).first()
        if address_info:
            return jsonify(address_info)
        else:
            if code == "None":
                referral_code = remove_symbols(b64encode(os.urandom(32)).decode())[:7]
                store_address = Address(address=address, balance=REWARD, referral_count=0, rewards=REWARD, referral_code=referral_code)
                db.session.add(store_address)
                db.session.commit()

                return jsonify(store_address)
            else:
                get_address = Address.query.filter_by(referral_code=code).first()
                if get_address:
                    get_address.balance += REWARD
                    get_address.rewards += REWARD
                    get_address.referral_count += 1
                
                    referral_code = remove_symbols(b64encode(os.urandom(32)).decode())[:7]
                    store_address = Address(address=address, balance=REWARD, referral_count=0, rewards=REWARD, referral_code=referral_code)
                    referral = Referral(referral_id=get_address.id, address=address )
                
                    db.session.add(store_address)
                    db.session.add(referral)
                    
                    db.session.commit()
                else:
                    referral_code = remove_symbols(b64encode(os.urandom(32)).decode())[:7]
                    store_address = Address(address=address, balance=REWARD, referral_count=0, rewards=REWARD, referral_code=referral_code)
                
                    db.session.add(store_address)
                
                    db.session.commit()
                    
                
                return jsonify(store_address)
    
    
@app.route("/address", methods=["GET", "POST"])
def get_address():
    if request.method == "POST":
        address = request.json.get("address")
        address_info = Address.query.filter_by(address=address).first()
        if address_info:
            return jsonify(address_info)
        else:
            referral_code = b64encode(os.urandom(32))[:7]
            store_address = Address(address=address, balance=0, referral_count=0, rewards=0, referral_code=referral_code)
            db.session.add(store_address)
            db.session.commit()
            return jsonify(store_address)
    else:
        address = request.args.get("address")
        address_info = Address.query.filter_by(address=address).first()
        return jsonify(address_info)

@app.route("/withdraw", methods=["GET", "POST"])
def withdraw():
    if request.method == "POST":
        address = request.json.get("address")
        print(address)
        
        address_info = Address.query.filter_by(address=address).first()
        if address_info:
            if address_info.balance >= WITHDRAW_MIN:
                address_bal = address_info.balance
                address_info.balance = 0 
                db.session.commit()
                return jsonify({"msg": f"Your {address_bal}NS withdrawal is pending, Keep referring"})
            else:
                return jsonify({"msg": f"Mini withdraw {WITHDRAW_MIN} NS. Keep referring"})


if __name__  == '__main__':
    app.run(debug=True, host="0.0.0.0", port="6700")
    db.create_all()