from flask import Flask, render_template, request
import qrcode
import base64
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    link = request.form['link']
    token = generate_unique_token()  # Function to generate your unique token

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,  # Controls the size of the QR Code (1 is the smallest)
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level
        box_size=5,  # Size of each box in the QR code grid
        border=2,  # Thickness of the border (minimum is 4)
    )
    qr.add_data(link)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')

    # Convert image to base64 for rendering in HTML
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    qr_code_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

    return render_template('qr_page.html', qr_code=qr_code_base64, token=token)

def generate_unique_token():
    # Your logic to generate a unique token
    import uuid
    return str(uuid.uuid4())

if __name__ == '__main__':
    app.run(debug=True)
