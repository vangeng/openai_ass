import time

import openai


class Assistant:
    def __init__(self, client, name, instruction, model='gpt-4-1106-preview'):
        self.client = client
        self.id = self.create_assistant(client, name, instruction, model)
        self.name = name
        self.instruction = instruction
        self.model = model
    
    def create_assistant(self, client, name, instruction, model):
        assistant = client.beta.assistants.create(
            instructions=instruction,
            name=name,
            tools=[],
            model=model,
        )
        return assistant.id

    def delete(assistant_id):
        response = client.beta.assistants.delete(assistant_id=assistant_id)
        return response

    def list(client, order="desc", limit="20"):
        my_assistants = client.beta.assistants.list(
            order=order,
            limit=limit,
        )
        return my_assistants.data

class Thread:
    def __init__(self, client):
        self.client = client
        self.id = self.create_thread(client)
    
    def create_thread(self, client):
        thread = client.beta.threads.create()
        return thread.id

class Run:
    def __init__(self, client, thread_id, assistant_id):
        self.client = client
        self.thread_id = thread_id
        self.assistant_id = assistant_id
        self.run = self.create_run(client, thread_id, assistant_id)
    
    def create_run(self, client, thread_id, assistant_id):
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id,
        )
        return run
    
    # def send_message(thread_id, message):
    #     client.beta.threads.messages.create(
    #     thread_id=thread_id,
    #     role="user",
    #     content=message
    #     )

    def get_response(self):
        secends = 1
        while self.run.status != 'completed':
            print(f'{secends} s')
            time.sleep(1)
            self.run = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread_id,
                run_id=self.run.id
            )
            secends += 1
        print('status:', self.run.status)
        messages = self.client.beta.threads.messages.list(
            thread_id=self.thread_id
        )
        respone = messages.data[0].content[0]
        if respone.type == 'text':
            return respone.text.value
        
    
# if __name__ == "__main__":
#     import os
#     from flask.cli import load_dotenv

#     load_dotenv()
#     api_key = os.getenv('OPENAI_API_KEY')
#     print('api_key:', api_key)
#     os.environ["OPENAI_API_KEY"] = api_key
#     client = openai.Client()
    
#     data = Assistant.list(client=client) 
#     print(data)