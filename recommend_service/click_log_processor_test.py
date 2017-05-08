import sys
import os
from datetime import datetime
import yaml
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'py_utils'))
from rabbitMQ import RabbitMQ

f = open(os.path.join(os.path.dirname(__file__), '..', 'config.yaml'))
config = yaml.load(f)
f.close()
QUE_LOGGER = config['QUE_LOGGER']

logClient = RabbitMQ(QUE_LOGGER['URI'], QUE_LOGGER['NAME'])

message = {
    'userID': 'xiaoming',
    'newsID': 'hvLPGJwNiM34lv+wki/9hQ==\n',
    'timestamp': str(datetime.utcnow())}

logClient.sendMessage(message)

# TODO: test the click_log_processor after machine learning complete
