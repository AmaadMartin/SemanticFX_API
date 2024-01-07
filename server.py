from flask import Flask, request, jsonify
from EffectGenerator import EffectGeneratorAssistant  # Import your GPT class from your script

app = Flask(__name__)
gpt = EffectGeneratorAssistant()

@app.route('/create-conversation', methods=['POST'])
def create_conversation():
    thread_id = gpt.create_conversation()
    return jsonify(thread_id)

@app.route('/get-params', methods=['POST'])
def get_params():
    data = request.json
    try:
        thread_id = data['thread_id']
        query = data['query']
        current_state = data['current_state']
    except: 
        return jsonify({'error': 'Invalid request'})
    
    new_query = f"Current State: {current_state}\n\n Query:{query}"
    
    print('starting generator')
    messages, run_parameters = gpt.run_generator(new_query, thread_id)
    print('generator finished')
    response = {'messages': messages, 'run_parameters': run_parameters}
    print(response)
    return jsonify(response)

@app.route('/delete-conversation', methods=['POST'])
def delete_conversation():
    data = request.json
    try:
        thread_id = data['thread_id']
    except: 
        return jsonify({'error': 'Invalid request'})
    
    gpt.delete_thread(thread_id)
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run()
