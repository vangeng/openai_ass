from flask import jsonify, request
from flask import Blueprint
import openai

from .models import Assistant, Thread, Run
assistant_bp = Blueprint('assistant', __name__)

client = openai.Client()
@assistant_bp.route('/assistant', methods=['POST'])
def new_assistant():
    """
    创建一个新的助手，使用给定的指令和名称。
    
    Args:
        instruction (str): 助手的指令。
        Assistant_name (str): 助手的名称。
        
    Returns:
        包含创建的助手的消息、助手ID和名称的JSON响应。
    """
    instruction = request.form.get('instruction')
    Assistant_name = request.form.get('name')
    
    if not instruction:
        return jsonify({'error': 'instruction is required'}), 400
    
    if not Assistant_name:
        return jsonify({'error': 'Assistant_name is required'}), 400
    
    try:
        assistant = Assistant(client=client, name=Assistant_name, 
                  instruction=instruction)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
    return jsonify({'message': 'assistant created', 
                    'assistant_id': assistant.id,
                    'name':assistant.name}), 200


@assistant_bp.route('/assistant/list', methods=['GET'])
def list_assistants():
    """
    获取所有助手的列表。

    Returns:
        包含所有助手的列表的 JSON 响应。
    """
    assistants = Assistant.list(client=client)
    return jsonify({'assistants': assistants}), 200

@assistant_bp.route('/assistant/delete', methods=['DELETE'])
def delete_assistant():
    """
    删除给定 ID 的助手。

    Args:
        assistant_id (str): 助手的 ID。

    Returns:
        包含删除助手的消息的 JSON 响应。
    """
    assistant_id = request.form.get('assistant_id')
    if not assistant_id:
        return jsonify({'error': 'assistant_id is required'}), 400
    try:
        Assistant.delete_assistant(client=client, assistant_id=assistant_id)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    return jsonify({'message': 'assistant deleted'}), 200


@assistant_bp.route('/thread/create', methods=['GET'])
def new_thread():
    """
    为助手创建一个新的线程。

    Args:
        assistant_id (str): 助手的ID。

    Returns:
        包含消息和创建的线程ID的JSON响应。
    """
    assistant_id = request.args.get('assistant_id')
    if not assistant_id:
        return jsonify({'error': 'assistant_id is required'}), 400
    try:
        thread = Thread(client=client)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    return jsonify({'message': 'thread created', 
                    'thread_id': thread.id}), 200
    
@assistant_bp.route('/run', methods=['POST'])
def run():
    """
    接收一个带有 assistant_id、thread_id 和 message 参数的 POST 请求。
    使用给定的参数创建一个 Run 对象，并返回 Run 对象的响应。
    如果缺少任何必需参数，则返回一个带有 400 状态码的错误消息。
    如果在创建 Run 对象期间发生异常，则返回带有 400 状态码的异常消息。
    """
    assistant_id = request.form.get('assistant_id')
    thread_id = request.form.get('thread_id')
    message = request.form.get('message')
    
    if not assistant_id:
        return jsonify({'error': 'assistant_id is required'}), 400
    
    if not thread_id:
        return jsonify({'error': 'thread_id is required'}), 400
    
    if not message:
        return jsonify({'error': 'message is required'}), 400
    
    try:
        client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message
        )
        run = Run(client=client, assistant_id=assistant_id, thread_id=thread_id)
        # run.send_message(message=message)
        response = run.get_response()
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    if response != '':
        return jsonify({'message': 'successful', 'response':response}), 200