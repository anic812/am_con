from flask import Flask, request, jsonify
from main import iTunesCountryChecker  # Replace with the actual file/module name

app = Flask(__name__)

@app.route('/check', methods=['GET'])
def check_app_availability():
    app_id = request.args.get('id')
    
    if not app_id or not app_id.isdigit():
        return jsonify({"error": "Invalid or missing app ID"}), 400

    try:
        with iTunesCountryChecker(int(app_id)) as checker:
            result =  checker.check_countries()
            return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="color-scheme" content="light dark">
        <link rel="mask-icon" href="https://music.apple.com/assets/favicon/favicon.svg" color="#fa233b">
        <title>Apple Music Country Checker</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f7f7f7;
                color: #333;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                text-align: center;
                padding: 30px;
                background-color: #fff;
                border-radius: 10px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                max-width: 500px;
                width: 100%;
            }
            h1 {
                font-size: 2.5rem;
                margin-bottom: 20px;
                color: #f44336;
            }
            p {
                font-size: 1.2rem;
                color: #555;
                line-height: 1.6;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Welcome to the Apple Music Country Availability Checker API!</h1>
            <p>Use the <strong>/check</strong> endpoint with a valid app ID.</p>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True)
