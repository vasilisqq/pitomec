from aiogram.fsm.storage.redis import RedisStorage
import json

class RedisStorageExpanded(RedisStorage):
    def __init__(self, redis, key_builder = None, state_ttl = None, data_ttl = None, json_loads = json.loads, json_dumps = json.dumps):
        super().__init__(redis, key_builder, state_ttl, data_ttl, json_loads, json_dumps)

    async def clear_all_fsm_data(self):
        prefix = self.key_builder.prefix
        separator = self.key_builder.separator
        pattern = f"{prefix}{separator}*"
        keys = []
        async for key in self.redis.scan_iter(match=pattern):
            keys.append(key)
        if keys:
            await self.redis.delete(*keys)

