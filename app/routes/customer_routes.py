from flask import Blueprint, jsonify, make_response, request, abort
from werkzeug.exceptions import RequestEntityTooLarge
from app import db
from app.models.customer import Customer

customer_bp = Blueprint("customer", __name__, url_prefix="/customers")

# HELPER FUNCTIONS
def valid_int(number, parameter_type):
    try:
        number = int(number)
    except:
        abort(400, {"error":f"{parameter_type} must be an int"})

def get_customer_from_id(customer_id):
    valid_int(customer_id, "customer_id")
    customer = Customer.query.get(customer_id)
    if not customer:
        abort(make_response({"message":f"Customer {customer_id} was not found"}, 404))
    
    return customer

# CUSTOMER ROUTES

# Get all customers
@customer_bp.route("", methods =["GET"])
def read_all_customers():
    customers = Customer.query.all()

    customers_response = []
    for customer in customers:
        customers_response.append(
            customer.to_dict()
        )

    return jsonify(customers_response), 200

#Create customer
@customer_bp.route("", methods =["POST"])
def create_customer():
    request_body = request.get_json()
    if "name" not in request_body: 
        return {"details":"Request body must include name."}, 400
    elif "postal_code" not in request_body:
        return {"details":"Request body must include postal_code."}, 400
    elif "phone" not in request_body:
        return {"details": "Request body must include phone."}, 400
    else:
        new_customer = Customer(
            name=request_body["name"],
            postal_code=request_body["postal_code"],
            phone=request_body["phone"],
        )

        db.session.add(new_customer)
        db.session.commit()

        return {"id":new_customer.id}, 201

# Get customer by id
@customer_bp.route("/<customer_id>", methods =["GET"])
def get_one_customer(customer_id):
    customer = get_customer_from_id(customer_id)
    response_body = customer.to_dict()
    return jsonify(response_body), 200

# Update customer by id
@customer_bp.route("/<customer_id>", methods =["PUT"])
def update_customer(customer_id):
    customer = get_customer_from_id(customer_id)
    request_body = request.get_json()
    if "name" not in request_body or "postal_code" not in request_body or "phone" not in request_body:
        return {"Message":"Bad request"}, 400
    else:
        customer.name = request_body["name"]
        customer.postal_code = request_body["postal_code"]
        customer.phone = request_body["phone"]

        db.session.commit()

        response_body = customer.to_dict()
        return jsonify(response_body), 200

# Delete customer by id
@customer_bp.route("/<customer_id>", methods =["DELETE"])
def delete_customer(customer_id):
    customer = get_customer_from_id(customer_id)
    db.session.delete(customer)
    db.session.commit()

    customer
    return {"id":customer.id}, 200



