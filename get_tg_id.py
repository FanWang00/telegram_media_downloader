from telethon import TelegramClient
from telethon import utils

api_id = 28138839
api_hash = "a9a02c1d67d1fffc9f99b033fbbda44a"

with TelegramClient("sess", api_id, api_hash) as client:
    entity = client.get_entity("sgpai520")
    print("entity.id =", entity.id)
    print("peer_id  =", utils.get_peer_id(entity))  # 