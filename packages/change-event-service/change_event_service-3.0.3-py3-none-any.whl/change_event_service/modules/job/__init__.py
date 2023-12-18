import json
import logging
import traceback

import pika as pika
from change_event_service.database import db
from change_event_service.modules.rest.models import ChangeEventModel
from retry import retry


@retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
def consume_change_events(app_context):
    print('Job Started')
    app_context.app_context().push()
    mq_host = app_context.config.get('MQ_HOST')
    mq_vhost = app_context.config.get('MQ_VHOST')
    mq_user = app_context.config.get('MQ_USER')
    mq_pass = app_context.config.get('MQ_PASS')
    mq_queue = app_context.config.get('MQ_QUEUE')
    mq_exchange = app_context.config.get('MQ_EXCHANGE')
    mq_routing_key = app_context.config.get('MQ_ROUTING_KEY')

    def camel_to_snake(s):
        return ''.join(['_'+c.lower() if c.isupper() else c for c in s]).lstrip('_')

    def on_message(channel, method_frame, header_frame, body):
        body = body.decode('utf-8')
        change_event = None
        try:
            body = json.loads(body)
            _body = {}
            for field in body:
                if field == "tag":
                    _body["tag"] = [tag.strip() for tag in body["tag"].split(",")]
                else:
                    _body[camel_to_snake(field)] = body[field]
            change_event = ChangeEventModel(**_body)
            db.session.add(change_event)
            db.session.commit()
        except Exception as e:
            stack_trace = traceback.format_exc()
            logging.error(stack_trace)
            body = json.dumps(body).encode('utf-8')
            channel.basic_publish(exchange=mq_exchange, routing_key=mq_routing_key, body=body)
            db.get_app()
            db.session.rollback()
        finally:
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)

    cred = pika.PlainCredentials(mq_user, mq_pass)
    conn = pika.BlockingConnection(pika.ConnectionParameters(host=mq_host, virtual_host=mq_vhost, credentials=cred))
    channel = conn.channel()
    channel.basic_consume(mq_queue,  on_message, consumer_tag='change-event-service')
    try:
        channel.start_consuming()
    except pika.exceptions.ConnectionClosedByBroker:
        pass
