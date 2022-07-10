from stock_service.app import create_app, create_rabbitmq_channel

app = create_app()

rabbitmq_channel = create_rabbitmq_channel()
rabbitmq_channel.start_consuming()
