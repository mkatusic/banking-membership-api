import hashlib
import json


def generate_request_hash(request_data: dict) -> str:
    serialized_data = json.dumps(
        request_data,
        sort_keys=True,
        separators=(",", ":"),
    )

    return hashlib.sha256(
        serialized_data.encode("utf-8")
    ).hexdigest()