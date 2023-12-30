from flask import Flask, request, jsonify
from EffectGenerator import GPT  # Import your GPT class from your script

app = Flask(__name__)
gpt = GPT()

@app.route('/get-params', methods=['POST'])
def engineer_prompt():
    data = request.json
    query = data['query']    
    gpt.engineerPrompt(query)
    print(gpt.parameters)
    return jsonify(gpt.parameters)

if __name__ == '__main__':
    app.run()
