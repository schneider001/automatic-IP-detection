import pika


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


def receive_messege():
    credentials = pika.PlainCredentials("username", "password")
    parameters = pika.ConnectionParameters("localhost", credentials=credentials) 
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue="hello")

    print ("[*] Waiting for messages. To exit press CTRL+C")

    channel.basic_consume("hello", callback, auto_ack=True)

    channel.start_consuming()


def main():
    receive_messege()


if __name__ == "__main__":
    main()
