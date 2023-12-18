#IEEE floating point converter new 

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def decimal_to_ieee_754_single(decimal_number, precision):
    result = {}

    # Handling special cases: positive and negative zero
    if decimal_number == 0.0:
        result['special_case'] = 'Positive Zero'
        result['binary_representation'] = '00000000000000000000000000000000'
        return result

    # Determine the sign bit
    result['sign_bit'] = '0' if decimal_number >= 0 else '1'

    # Separate the whole and decimal part of the number
    whole_part = abs(int(decimal_number))
    decimal_part = abs(decimal_number) - whole_part

    # Convert the whole number into binary
    whole_binary = bin(whole_part)[2:]
    result['whole_binary'] = whole_binary

    # Convert the decimal part into binary
    decimal_binary = ''
    while decimal_part > 0:
        decimal_part *= 2
        decimal_binary += str(int(decimal_part))
        decimal_part -= int(decimal_part)
    result['decimal_binary'] = decimal_binary[:23]

    # Combine the whole and decimal parts directly
    binary_number = whole_binary +"."+ decimal_binary
    result['combined_binary'] = binary_number[:23]

    # Determine the exponent
    exponent = len(whole_binary) - 1 + 127  # Add bias (127 for single precision)
    result['exponent'] = exponent

    # Convert the exponent to binary representation
    exponent_binary = format(exponent, '08b')
    result['exponent_binary'] = exponent_binary

    # Determine the mantissa (excluding the implied leading '1')
    mantissa = whole_binary[1:] + decimal_binary
    
    # Pad with zeros to reach 23 bits after the leading '1'
    mantissa = mantissa.ljust(23, '0')
    
    result['mantissa'] = mantissa[:23]

    # Combine the sign bit, exponent, and mantissa to get the final IEEE 754 representation
    ieee_754_representation = result['sign_bit'] + "  " + result['exponent_binary']+ "  " + result['mantissa']
    result['ieee_754_representation'] = ieee_754_representation[:36]  # Restrict to 32 bits for single precision

    return result


def decimal_to_ieee_754_double(decimal_number, precision):
    result = {}

    # Handling special cases: positive and negative zero
    if decimal_number == 0.0:
        result['special_case'] = 'Positive Zero'
        result['binary_representation'] = '00000000000000000000000000000000'
        return result

    # Determine the sign bit
    result['sign_bit'] = '0' if decimal_number >= 0 else '1'

    # Separate the whole and decimal part of the number
    whole_part = abs(int(decimal_number))
    decimal_part = abs(decimal_number) - whole_part

    # Convert the whole number into binary
    whole_binary = bin(whole_part)[2:]
    result['whole_binary'] = whole_binary

    # Convert the decimal part into binary
    decimal_binary = ''
    while decimal_part > 0:
        decimal_part *= 2
        decimal_binary += str(int(decimal_part))
        decimal_part -= int(decimal_part)
    result['decimal_binary'] = decimal_binary

    # Combine the whole and decimal parts directly
    binary_number = whole_binary +"."+ decimal_binary
    result['combined_binary'] = binary_number

    # Determine the exponent
    exponent = len(whole_binary) - 1 + 1023  # Add bias (1023 for double precision)
    result['exponent'] = exponent

    # Convert the exponent to binary representation
    exponent_binary = format(exponent, '011b')
    result['exponent_binary'] = exponent_binary

    # Determine the mantissa (excluding the implied leading '1')
    mantissa = whole_binary[1:]+ decimal_binary [:] # 52 bits for double precision
    
    # Pad with zeros to reach 52 bits after the leading '1'
    mantissa = mantissa.ljust(52, '0')
    
    result['mantissa'] = mantissa

    # Combine the sign bit, exponent, and mantissa to get the final IEEE 754 representation
    ieee_754_representation = result['sign_bit'] + "  "+result['exponent_binary'] + "  " + result['mantissa']
    result['ieee_754_representation'] = ieee_754_representation[:68]

    return result

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    decimal_number = float(request.form['decimalInput'])
    precision = request.form['precision']
    
    if precision == 'single':
        ieee_754_result = decimal_to_ieee_754_single(decimal_number, precision)
    elif precision == 'double':
        ieee_754_result = decimal_to_ieee_754_double(decimal_number, precision)
    else:
        return jsonify({'error': 'Invalid precision'})

    return jsonify(ieee_754_result)

if __name__ == '__main__':
    app.run(debug=True)


