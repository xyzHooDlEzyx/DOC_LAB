import json
from abc import ABC, abstractmethod
from typing import Dict, Iterable, Mapping, Optional


class OutputStrategy(ABC):
    @abstractmethod
    def write_records(self, records: Iterable[Mapping[str, object]]) -> int:
        raise NotImplementedError


class ConsoleOutputStrategy(OutputStrategy):
    def __init__(self, limit: Optional[int] = None) -> None:
        self._limit = limit

    def write_records(self, records: Iterable[Mapping[str, object]]) -> int:
        count = 0
        for record in records:
            if self._limit is not None and count >= self._limit:
                break
            print(json.dumps(record, ensure_ascii=True))
            count += 1
        return count


class KafkaOutputStrategy(OutputStrategy):
    def __init__(self, bootstrap_servers: str, topic: str) -> None:
        self._bootstrap_servers = bootstrap_servers
        self._topic = topic

    def write_records(self, records: Iterable[Mapping[str, object]]) -> int:
        try:
            from kafka import KafkaProducer
        except ImportError as exc:
            raise RuntimeError(
                "kafka-python is required for Kafka output."
            ) from exc

        producer = KafkaProducer(bootstrap_servers=self._bootstrap_servers)
        count = 0
        try:
            for record in records:
                payload = json.dumps(record, ensure_ascii=True).encode("utf-8")
                producer.send(self._topic, payload)
                count += 1
            producer.flush()
        finally:
            producer.close()
        return count


class RedisOutputStrategy(OutputStrategy):
    def __init__(self, host: str, port: int, list_key: str) -> None:
        self._host = host
        self._port = port
        self._list_key = list_key

    def write_records(self, records: Iterable[Mapping[str, object]]) -> int:
        try:
            import redis
        except ImportError as exc:
            raise RuntimeError("redis is required for Redis output.") from exc

        client = redis.Redis(host=self._host, port=self._port)
        count = 0
        for record in records:
            payload = json.dumps(record, ensure_ascii=True)
            client.rpush(self._list_key, payload)
            count += 1
        return count


class FirebaseOutputStrategy(OutputStrategy):
    def __init__(
        self,
        service_account_file: str,
        collection: str,
        database_id: Optional[str] = None,
    ) -> None:
        self._service_account_file = service_account_file
        self._collection = collection
        self._database_id = database_id

    def write_records(self, records: Iterable[Mapping[str, object]]) -> int:
        try:
            import firebase_admin
            from firebase_admin import credentials, firestore
            from google.oauth2 import service_account
        except ImportError as exc:
            raise RuntimeError(
                "firebase-admin is required for Firebase output."
            ) from exc

        if not self._service_account_file:
            raise RuntimeError("Firebase service_account_file is required.")

        credentials_obj = service_account.Credentials.from_service_account_file(
            self._service_account_file
        )
        firebase_cred = credentials.Certificate(self._service_account_file)

        if not firebase_admin._apps:
            firebase_admin.initialize_app(firebase_cred)

        if self._database_id:
            db = firestore.Client(
                project=credentials_obj.project_id,
                credentials=credentials_obj,
                database=self._database_id,
            )
        else:
            db = firestore.client()
        batch = db.batch()
        count = 0
        for record in records:
            doc_ref = db.collection(self._collection).document()
            batch.set(doc_ref, record)
            count += 1
            if count % 500 == 0:
                batch.commit()
                batch = db.batch()

        if count % 500 != 0:
            batch.commit()
        return count


def build_output_strategy(output_config: Dict[str, object]) -> OutputStrategy:
    output_type = str(output_config.get("type", "console")).lower()
    if output_type == "console":
        console_config = output_config.get("console", {})
        limit = console_config.get("limit")
        return ConsoleOutputStrategy(limit=limit)
    if output_type == "kafka":
        kafka_config = output_config.get("kafka", {})
        return KafkaOutputStrategy(
            bootstrap_servers=str(kafka_config.get("bootstrap_servers", "")),
            topic=str(kafka_config.get("topic", "")),
        )
    if output_type == "redis":
        redis_config = output_config.get("redis", {})
        return RedisOutputStrategy(
            host=str(redis_config.get("host", "localhost")),
            port=int(redis_config.get("port", 6379)),
            list_key=str(redis_config.get("list_key", "police_incidents")),
        )
    if output_type == "firebase":
        firebase_config = output_config.get("firebase", {})
        return FirebaseOutputStrategy(
            service_account_file=str(
                firebase_config.get("service_account_file", "")
            ),
            collection=str(
                firebase_config.get("collection", "police_incidents")
            ),
            database_id=str(firebase_config.get("database_id", "")) or None,
        )
    raise ValueError(f"Unsupported output type: {output_type}")
