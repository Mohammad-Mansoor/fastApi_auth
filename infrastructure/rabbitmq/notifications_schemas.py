from pydantic import BaseModel
from typing import List, Dict, Any
from .notification_events import NotificationChannel, NotificationEventType


class SendNotificationDto(BaseModel):
    type: NotificationEventType
    channels: List[NotificationChannel]
    payload: Dict[str, Any]