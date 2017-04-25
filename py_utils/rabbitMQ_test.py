from rabbitMQ import RabbitMQ

rabbitMQUrl = "amqp://uneggxcr:eElS-gADqt1sv8niqv6uzKaiCKT2mnhP@donkey.rmq.cloudamqp.com/uneggxcr"
queueName = "test"

client = RabbitMQ(rabbitMQUrl, queueName)
# client.sendMessage("Hello")
# client.sendMessage("Hello1")
# client.sendMessage("Hello2")
# client.sendMessage("Hello3")
# client.sendMessage("Hello4")
# client.sleep(5)
# client.getMessage()
client.getMessage()
# client.ackMessage()
# client.getMessage()

