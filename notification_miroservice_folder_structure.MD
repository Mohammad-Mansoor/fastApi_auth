notification-service/
│
├── app/
│   │
│   ├── main.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── rabbitmq.py
│   │   ├── redis.py
│   │   ├── logging.py
│   │
│   ├── websocket/                     # 🔥 REAL-TIME GATEWAY
│   │   ├── manager.py                 # connection manager
│   │   ├── gateway.py                 # socket server
│   │   ├── events.py                  # emit events to clients
│   │
│   ├── consumers/                     # RabbitMQ listeners
│   │   ├── auth_events.py            # login/logout events
│   │   ├── system_events.py
│   │   ├── notification_events.py
│   │
│   ├── services/
│   │   ├── notification_service.py
│   │   ├── email_service.py
│   │   ├── push_service.py
│   │
│   ├── brokers/
│   │   ├── rabbitmq_consumer.py
│   │   ├── redis_pubsub.py
│   │
│   ├── models/
│   │   ├── notification.py
│   │
│   ├── common/
│   │   ├── utils/
│   │   ├── base/
│   │
│   └── tests/
│
└── requirements.txt