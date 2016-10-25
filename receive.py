#!/usr/bin/env python
import pika

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

def recv_msg(exchange, rkey):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost'))
    
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange, type='direct')
    
    result = channel.queue_declare()
    qname = result.method.queue
    
    print("[receive] qname: %s" % (qname))
    
    channel.queue_bind(exchange=exchange, queue=qname, routing_key=rkey)
    
    channel.basic_consume(callback,
                          queue=qname,
                          no_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    recv_msg(
        exchange = 'st2-test',
        rkey = 'opened'
    )
