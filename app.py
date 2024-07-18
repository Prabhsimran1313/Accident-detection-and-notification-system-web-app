from flask import Flask, render_template, request, jsonify
import camera

app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    
    result = camera.process_input(file)
    
    return jsonify({'result': result}), 200

if __name__ == '__main__':
    app.run(debug=True)
