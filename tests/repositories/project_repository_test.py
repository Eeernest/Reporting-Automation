import pytest

# add_project

@pytest.mark.anyio
@pytest.mark.integration
async def test_add_project(integ_project_repo, integ_project_obj):
  result = await integ_project_repo.add_project(integ_project_obj)

  assert result.id
  assert result == integ_project_obj