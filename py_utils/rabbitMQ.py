import pika
import json

class RabbitMQ:
    def __init__(self, rabbitMQUrl, queueName):
        self.rabbitMQUrl = rabbitMQUrl
        self.queueName = queueName
        self.params = pika.URLParameters(rabbitMQUrl)
        self.params.socket_timeout = 3
        self.connection = pika.BlockingConnection(self.params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queueName)
        self.delivery_tag = 0

    def sendMessage(self, message):
        self.channel.basic_publish(exchange='', routing_key=self.queueName, body=json.dumps(message))
        # print "[X] sent message to %s: %s" % (self.queueName, message)
        print "[X] sent message to %s" % self.queueName
        return

    # get message from queue, to consume the message, need to call ackMessage.
    def getMessage(self):
        method_frame, header_frame, body = self.channel.basic_get(self.queueName)
        if method_frame:
            # print "[O] Received message from %s: %s" % (self.queueName, body)
            print "[O] Received message from %s" % self.queueName
            self.delivery_tag = method_frame.delivery_tag
            return json.loads(body)
        else:
            print "No message returned"
            return None

    def ackMessage(self):
        if(self.delivery_tag != 0):
            self.channel.basic_ack(self.delivery_tag)
        else:
            print "message not being acked"

    def sleep(self, seconds):
        self.connection.sleep(seconds)