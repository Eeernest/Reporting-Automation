import pytest

@pytest.mark.anyio
@pytest.mark.integration
async def test_add_item(integ_item_repo, integ_item_obj):
  result = await integ_item_repo.add_item(integ_item_obj)

  assert result.id
  assert result == integ_item_obj