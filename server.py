from flask import Flask, request, jsonify
from EffectGenerator import GPT  # Import your GPT class from your script

app = Flask(__name__)

@app.route('/get-params', methods=['POST'])
def engineer_prompt():
    data = request.json
    query = data['query']
    gpt = GPT()
    gpt.engineerPrompt(query)
    return jsonify(gpt.parameters)

if __name__ == '__main__':
    app.run()
