from fastapi import HTTPException
import pika
import random
import time
from api.utils.connection import get_rabbitmq_connection
from datetime import datetime


def send_message_to_queue(queue_name: str, message: str):
    connection = get_rabbitmq_connection()
    channel = connection.channel()
    
    channel.queue_declare(queue=queue_name, durable=True)
    
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,  
        ))
    
    connection.close()

def send_messages(msg_count):
    count = 0 
    messages_list = []
    try:
        while True:
            status = random.randint(0, 6)
            message = f'{{"status": {status},"timestamp":{time.time()}}}'
            send_message_to_queue("your_queue_name", message)
            messages_list.append(message)
            time.sleep(1)
            count = count + 1 
            if count > msg_count:
                return messages_list
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


