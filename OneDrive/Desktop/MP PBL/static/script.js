function convert() {
    const decimalNumber = document.getElementById('decimalInput').value;
    const precision = document.getElementById('precision').value;

    fetch('/convert', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `decimalInput=${decimalNumber}&precision=${precision}`,
    })
    .then(response => response.json())
    .then(data => displayOutput(data));

    return false; // Prevent form submission
}

function displayOutput(data) {
    const outputDiv = document.getElementById('output');
    outputDiv.innerHTML = "";

    if ('error' in data) {
        displayOutputBox("Error", data.error);
    } else {
        displayOutputBox("Sign Bit", data.sign_bit);
        displayBinaryRepresentation("Whole Binary", data.whole_binary);
        displayBinaryRepresentation("Decimal Binary", data.decimal_binary);
        displayBinaryRepresentation("Combined Binary", data.combined_binary);
        displayOutputBox("Exponent", data.exponent);
        displayBinaryRepresentation("Exponent Binary", data.exponent_binary);
        displayBinaryRepresentation("Mantissa", data.mantissa, 23); // Restrict to 23 bits
        displayBinaryRepresentation("IEEE 754 Representation", data.ieee_754_representation);
    }
}

function displayOutputBox(label, content) {
    const outputDiv = document.getElementById('output');
    const box = document.createElement('div');
    box.innerHTML = `<strong>${label}:</strong><br>${content}<br><br>`;
    outputDiv.appendChild(box);
}

function displayBinaryRepresentation(label, binaryString, limit = binaryString.length) {
    const outputDiv = document.getElementById('output');
    const box = document.createElement('div');
    box.innerHTML = `<strong>${label}:</strong><br>${getBinaryBoxes(binaryString, limit)}<br><br>`;
    outputDiv.appendChild(box);
}

function getBinaryBoxes(binaryString) {
    return binaryString
        .split('')
        .map(bit => bit === ' ' ? '<div class="space"></div>' : `<div class="binary-box binary-box-${bit}">${bit}</div>`)
        .join('');
}


