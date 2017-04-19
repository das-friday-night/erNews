from rabbitMQ import RabbitMQ

rabbitMQUrl = "amqp://uneggxcr:eElS-gADqt1sv8niqv6uzKaiCKT2mnhP@donkey.rmq.cloudamqp.com/uneggxcr"
queueName = "test"

client = RabbitMQ(rabbitMQUrl, queueName)
client.sendMessage("Hello")
client.sleep(5)
client.getMessage()
