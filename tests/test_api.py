import pytest
import pytest_asyncio


class TestQuestionsAPI:
    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.parametrize("question", ("Что делать, чтобы быть счастливым?", ))
    async def test_crud(self, async_client, question):
        request_data = {
            "text": "Что делать, чтобы быть счастливым?",
        }

        response = await async_client.post("/questions", json=request_data)
        created_at = response.json()["created_at"]

        assert response.status_code == 200
        assert response.json()["id"] == 1
        assert response.json()["text"] == question

        response = await async_client.delete("/questions/1")

        assert response.status_code == 200
        assert response.json()["id"] == 1
        assert response.json()["text"] == question
        assert response.json()["created_at"] == created_at

        response = await async_client.get("/questions")

        assert response.status_code == 200
        assert type(response.json()["questions"]) is list
        assert len(response.json()["questions"]) == 0

