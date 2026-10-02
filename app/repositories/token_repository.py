from redis.asyncio import Redis
from redis.exceptions import RedisError

import app.core.exceptions as e

class TokenRepository:
  def __init__(self, client: Redis):
    self.client = client

  # Main Methods

  async def store_refresh_token(self, jti: str, sub: str, exp: int) -> None:
    try:
      await self.client.set(name=self._get_key(jti), value=sub, exat=exp)

    except RedisError:
      raise e.RedisFailureError()

  async def delete_refresh_token(self, jti: str) -> None:
    try:
      await self.client.delete(self._get_key(jti))

    except RedisError:
      raise e.RedisFailureError()
    
  # As for right now it is used only in tests
  async def get_sub_by_jti(self, jti: str) -> str | None:
    try:
      return await self.client.get(self._get_key(jti))

    except RedisError:
      raise e.RedisFailureError()


  # Helper Methods

  def _get_key(self, jti: str) -> str:
    return f"refresh_token:{jti}"