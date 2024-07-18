from flask import Flask, request, jsonify
import uuid
import re
from datetime import datetime

app = Flask(__name__)

receipts = {}

def calculate_points(receipt):
    points = 0
    
    # Rule 1: One point for every alphanumeric character in the retailer name
    points += sum(1 for char in receipt['retailer'] if char.isalnum())
    
    # Rule 2: 50 points if the total is a round dollar amount with no cents
    total_float = float(receipt['total'])
    if total_float.is_integer():
        points += 50
    
    # Rule 3: 25 points if the total is a multiple of 0.25
    if total_float % 0.25 == 0:
        points += 25
    
    # Rule 4: 5 points for every two items on the receipt
    points += (len(receipt['items']) // 2) * 5
    
    # Rule 5: If trimmed length of item description is multiple of 3, calculate points based on price
    for item in receipt['items']:
        trimmed_length = len(item['shortDescription'].strip())
        if trimmed_length % 3 == 0:
            price = float(item['price'])
            extra_points = int(price * 0.2 + 0.5)  # Round up to nearest integer
            points += extra_points
    
    # Rule 6: 6 points if the day in the purchase date is odd
    purchase_date = datetime.strptime(receipt['purchaseDate'], '%Y-%m-%d')
    if purchase_date.day % 2 != 0:
        points += 6
    
    # Rule 7: 10 points if the time of purchase is after 2:00pm and before 4:00pm
    purchase_time = datetime.strptime(receipt['purchaseTime'], '%H:%M').time()
    if datetime.strptime('14:00', '%H:%M').time() < purchase_time < datetime.strptime('16:00', '%H:%M').time():
        points += 10
    
    return points

@app.route('/receipts/process', methods=['POST'])
def process_receipt():
    receipt_data = request.get_json()
    receipt_id = str(uuid.uuid4())
    receipts[receipt_id] = receipt_data
    response = {'id': receipt_id}
    return jsonify(response), 200

@app.route('/receipts/<receipt_id>/points', methods=['GET'])
def get_points(receipt_id):
    if receipt_id in receipts:
        receipt = receipts[receipt_id]
        points = calculate_points(receipt)
        response = {'points': points}
        return jsonify(response), 200
    else:
        return jsonify({'error': 'Receipt ID not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)