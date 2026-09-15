from redis.asyncio import Redis

class TokenRepository:
  def __init__(self, client: Redis):
    self.client = client

  # Main Methods

  async def store_refresh_token(self, jti: str, exp: int, sub: str) -> None:
    await self.client.set(self._get_key(jti), sub, exat=exp)

  async def delete_refresh_token(self, jti: str) -> None:
    await self.client.delete(self._get_key(jti))

  async def get_sub_by_jti(self, jti: str) -> str | None:
    return await self.client.get(self._get_key(jti))


  # Helper Methods

  def _get_key(self, jti: str) -> str:
    return f"refresh_token:{jti}"