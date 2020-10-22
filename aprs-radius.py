import aprslib
from datetime import datetime, timezone
from pymongo import MongoClient
import os


def unpack_dict(d):
    try:
        message = dict()
        message["timestamp_"] = datetime.now(timezone.utc)
        message["ttl"] = datetime.now(timezone.utc)
        message["script"] = "radius"
        for k, v in d.items():
            try:
                for k1, v1 in v.items():
                    message[k + "_" + k1] = v1
            except Exception:
                try:
                    message[k] = v
                except Exception:
                    message[k] = str(v)
        raw.insert_one(message)
        print(message)
    except Exception:
        print("unpack failed")


if __name__ == "__main__":
    while True:
        try:
            # MongoDB client
            client = MongoClient(os.environ["MONGODB_CLIENT"])
            db = client.aprs
            raw = db.raw

            # Mosquitto client
            ais = aprslib.IS("N0CALL", "13023", port=14580)
            ais.set_filter("r/30/-95/250 t/n")
            ais.connect()
            ais.consumer(unpack_dict, raw=False)
        except Exception:
            pass
