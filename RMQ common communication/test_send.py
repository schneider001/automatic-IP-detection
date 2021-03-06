import pika

credentials = pika.PlainCredentials('username', 'password')
parameters = pika.ConnectionParameters('192.168.0.3', credentials=credentials) 
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
print ("[x] Sent 'Hello World!")
connection.close()
