import pika

credentials = pika.PlainCredentials('postman', '11362266')
parameters = pika.ConnectionParameters('192.168.0.3', credentials=credentials) 
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(queue='hello')

print ('[*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

channel.basic_consume('hello', callback, auto_ack=True)

channel.start_consuming()

