from celery import Celery

celery_app = Celery(
    'telegram_bot',
    broker='amqp://guest:guest@localhost:5672//',
    backend='redis://localhost:6379/0'
)

celery_app.conf.update(
    # Настройки RabbitMQ для надежности
    broker_transport_options={
        'visibility_timeout': 3600,  # 1 час
        'max_retries': 3,
        'interval_start': 0,
        'interval_step': 0.2,
        'interval_max': 0.5,
    },
    
    # Персистентные сообщения
    task_default_delivery_mode='persistent',  # Сообщения пишутся на диск
    
    # Подтверждение после выполнения
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    
    # Настройки результатов в Redis
    result_backend_transport_options={
        'master_name': "mymaster",
        'retry_policy': {
            'timeout': 5.0
        }
    }
)