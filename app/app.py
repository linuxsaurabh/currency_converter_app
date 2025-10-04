from flask import Flask, request, jsonify, render_template
from decimal import Decimal, ROUND_HALF_UP

app = Flask(__name__, static_folder='static', template_folder='templates')

# rates are relative to USD

RATES = {
    'USD': 1.0,
    'EUR': 0.92,
    'GBP': 0.78,
    'JPY': 155.0
}

SUPPORTED_CURRENCIES = set(RATES.keys())


def convert_amount(amount: float, from_curr: str, to_curr: str) -> float:
    """Convert amount from `from_curr` to `to_curr` using hardcoded RATES.

    We interpret the RATES as: 1 USD = RATES[currency] currency.
    So to convert currency A to B, we do:
      1. Convert from A to USD: X (A -> USD) = X / RATES[A]
      2. Convert from USD to B: X (USD -> B) = X * RATES[B]

    We round the result to 4 decimal places using "round half up" strategy.
    """

    # validate currencies
    if from_curr not in RATES or to_curr not in RATES:
        raise ValueError('unsupported currency')

    # convert to USD then to target
    amount_usd = float(amount) / RATES[from_curr]
    result = amount_usd * RATES[to_curr]

    # round to 4 decimal places, return float
    d = Decimal(result).quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)
    return float(d)


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200


@app.route('/convert', methods=['POST'])
def convert():
    data = request.get_json(force=True)
    if not data:
        return jsonify({'error': 'invalid json body'}), 400

    try:
        amount = data.get('amount', None)
        from_curr = (data.get('from') or '').upper()
        to_curr = (data.get('to') or '').upper()

        if amount is None:
            return jsonify({'error': '`amount` is required'}), 400

        # allow numeric strings
        amount = float(amount)

        if from_curr not in SUPPORTED_CURRENCIES:
            return jsonify({'error': f'unsupported source currency: {from_curr}'}), 400
        if to_curr not in SUPPORTED_CURRENCIES:
            return jsonify({'error': f'unsupported target currency: {to_curr}'}), 400

        converted = convert_amount(amount, from_curr, to_curr)

        # compute implied rate (to_curr per from_curr)
        rate = convert_amount(1.0, from_curr, to_curr)

        return jsonify({
            'amount': amount,
            'from': from_curr,
            'to': to_curr,
            'converted': converted,
            'rate': rate
        }), 200

    except ValueError:
        return jsonify({'error': 'invalid numeric value for amount'}), 400
    except Exception as e:
        return jsonify({'error': 'internal error', 'details': str(e)}), 500


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', supported=sorted(list(SUPPORTED_CURRENCIES)))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)