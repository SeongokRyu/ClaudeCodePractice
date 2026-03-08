import threading
from typing import Any, Callable, Dict, List, Optional

# Callback type for this module
Callback = Callable[[Optional[Exception], Any], None]

# In-memory database simulation using callbacks
_store: Dict[str, Dict[str, Any]] = {}


def init_collection(collection_name: str, callback: Callback) -> None:
    def _run():
        _store[collection_name] = {}
        callback(None, None)

    timer = threading.Timer(0.01, _run)
    timer.start()


def insert(
    collection_name: str, id: str, data: Any, callback: Callback
) -> None:
    def _run():
        collection = _store.get(collection_name)
        if collection is None:
            callback(
                Exception(f"Collection '{collection_name}' does not exist"),
                None,
            )
            return
        if id in collection:
            callback(
                Exception(f"Document with id '{id}' already exists"),
                None,
            )
            return
        collection[id] = {**data} if isinstance(data, dict) else data
        callback(None, {**data} if isinstance(data, dict) else data)

    timer = threading.Timer(0.01, _run)
    timer.start()


def find_by_id(
    collection_name: str, id: str, callback: Callback
) -> None:
    def _run():
        collection = _store.get(collection_name)
        if collection is None:
            callback(
                Exception(f"Collection '{collection_name}' does not exist"),
                None,
            )
            return
        doc = collection.get(id)
        if doc is None:
            callback(
                Exception(f"Document with id '{id}' not found"),
                None,
            )
            return
        callback(None, {**doc} if isinstance(doc, dict) else doc)

    timer = threading.Timer(0.01, _run)
    timer.start()


def find_all(collection_name: str, callback: Callback) -> None:
    def _run():
        collection = _store.get(collection_name)
        if collection is None:
            callback(
                Exception(f"Collection '{collection_name}' does not exist"),
                None,
            )
            return
        docs = [{**doc} if isinstance(doc, dict) else doc for doc in collection.values()]
        callback(None, docs)

    timer = threading.Timer(0.01, _run)
    timer.start()


def update(
    collection_name: str,
    id: str,
    data: Dict[str, Any],
    callback: Callback,
) -> None:
    def _run():
        collection = _store.get(collection_name)
        if collection is None:
            callback(
                Exception(f"Collection '{collection_name}' does not exist"),
                None,
            )
            return
        existing = collection.get(id)
        if existing is None:
            callback(
                Exception(f"Document with id '{id}' not found"),
                None,
            )
            return
        if isinstance(existing, dict):
            updated = {**existing, **data}
        else:
            updated = data
        collection[id] = updated
        callback(None, {**updated} if isinstance(updated, dict) else updated)

    timer = threading.Timer(0.01, _run)
    timer.start()


def remove(collection_name: str, id: str, callback: Callback) -> None:
    def _run():
        collection = _store.get(collection_name)
        if collection is None:
            callback(
                Exception(f"Collection '{collection_name}' does not exist"),
                None,
            )
            return
        if id not in collection:
            callback(
                Exception(f"Document with id '{id}' not found"),
                None,
            )
            return
        del collection[id]
        callback(None, None)

    timer = threading.Timer(0.01, _run)
    timer.start()


def clear_all(callback: Callback) -> None:
    def _run():
        _store.clear()
        callback(None, None)

    timer = threading.Timer(0.01, _run)
    timer.start()
