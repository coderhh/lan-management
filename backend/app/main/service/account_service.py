import uuid
import datetime

from app.main import db
from app.main.model.account import Account
from typing import Dict, Tuple


def save_new_account(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    account = Account.query.filter_by(email=data['email']).first()
    if not account:
        new_account = Account(
            public_id=str(uuid.uuid4()),
            email=data['email'],
            first_name = data['first_name'],
            last_name = data['last_name'],
            role=data['role'],
            password=data['password'],
            created_on=datetime.datetime.utcnow()
        )
        save_changes(new_account)
        return generate_token(new_account)
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return response_object, 409

def update_an_account(data: Dict[str, str], public_id) -> Tuple[Dict[str, str], int]:
    account = Account.query.filter(public_id=public_id)
    if account:
        new_account = Account(
            email=data['email'],
            first_name = data['first_name'],
            last_name = data['last_name'],
            role=data['role'],
            password=data['password'],
            updated_on=datetime.datetime.utcnow()
        )
        update_account(new_account)
        response_object = {
            'status': 'success',
            'message': 'Successfully updated.'
        }
        return response_object, 200
    else:
        response_object = {
            'status': 'fail',
            'message': 'Account not exists.',
        }
        return response_object, 404

def get_all_accounts():
    return Account.query.all()

def get_a_account_by_id(public_id):
    return Account.query.filter_by(public_id=public_id).first()

def delete_a_account(public_id):
    account = get_a_account_by_id(public_id)
    if account:
        delete_account(account)
        response_object = {
            'status': 'success',
            'message': 'Successfully deleted.',
        }
        return response_object, 200
    else:
        response_object = {
            'status': 'fail',
            'message': 'Account not exists.',
        }
        return response_object, 404

def generate_token(account: Account) -> Tuple[Dict[str, str], int]:
    try:
        # generate the auth token
        auth_token = Account.encode_auth_token(account.id)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
            'Authorization': auth_token.decode()
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401


def save_changes(data: Account) -> None:
    db.session.add(data)
    db.session.commit()
def delete_account(data: Account) -> None:
    db.session.delete(data)
    db.session.commit()
def update_account(data:Account) -> None:
    db.session.update(data)
    db.session.commit()

