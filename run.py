import os
from flask.cli import load_dotenv


load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
print('api_key:', api_key)
os.environ["OPENAI_API_KEY"] = api_key

if __name__ == '__main__':
    from app import app
    app.run(host='0.0.0.0', port=8848)
