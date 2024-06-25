from api.utils.connection import get_mongodb_collection,get_rabbitmq_connection

def insert_message(message):
    collection = get_mongodb_collection()
    collection.insert_one({"message": message})
    print("Message stored in MongoDB")

    
def process_messages(queue_name = "your_queue_name"):
    while True:
        status = get_message(queue_name)
        print(status)
        if not status:
            return 

def get_message(queue_name):
    connection = get_rabbitmq_connection()
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)
    
    while True:
        # Fetch a single message from the queue
        method_frame, properties, body = channel.basic_get(queue=queue_name, auto_ack=True)
        if not method_frame:
            print("No messages in queue")
            connection.close()
                        
        print(f"Received message: {body.decode()}")
        insert_message(body.decode())
    
        


        