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
    return "Welcome to the iTunes App Availability Checker API! Use the /check endpoint with a valid app ID."   

if __name__ == '__main__':
    app.run(debug=True)