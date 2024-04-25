from celery import Task
from ..commands.kafka import KafkaPostfix
from ...events.kafka.client import KafkaConsumer


class DlqShovel(Task):
    def run(self, *args, **kwargs):
        try:
            consumer = KafkaConsumer()
            topic = f"^.*-{KafkaPostfix.DEAD_LETTER_QUEUE.value}"

            for topic_names, headers, data_values in consumer.consume(topic=topic):
                consumer.rotate_dql_messages(topic_names, headers, data_values)
        except Exception as e:
            raise self.retry(exc=e, countdown=10, raise_exception=True)
