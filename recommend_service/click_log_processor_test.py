import sys
import os
from datetime import datetime
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'py_utils'))
from config import QUE_LOGGER
from rabbitMQ import RabbitMQ

logClient = RabbitMQ(QUE_LOGGER['URI'], QUE_LOGGER['NAME'])

message = {
    'userID': 'xiaoming',
    'newsID': 'yAUfY0rLXNlEd4ZnCsfiOA==\n',
    'timestamp': str(datetime.utcnow())}

logClient.sendMessage(message)

# TODO: test the click_log_processor after machine learning complete
