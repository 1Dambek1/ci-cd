from __future__ import annotations

from fastapi.testclient import TestClient


def test_create_and_get_task(client: TestClient) -> None:
    create_response = client.post(
        "/tasks",
        json={
            "title": "Write backend tests",
            "description": "Cover CRUD endpoints",
            "status": "todo",
        },
    )

    assert create_response.status_code == 201
    created = create_response.json()
    assert created["title"] == "Write backend tests"
    assert created["status"] == "todo"

    get_response = client.get(f"/tasks/{created['id']}")

    assert get_response.status_code == 200
    fetched = get_response.json()
    assert fetched["id"] == created["id"]
    assert fetched["description"] == "Cover CRUD endpoints"


def test_list_tasks(client: TestClient) -> None:
    client.post("/tasks", json={"title": "Task 1", "status": "todo"})
    client.post("/tasks", json={"title": "Task 2", "status": "done"})

    response = client.get("/tasks")

    assert response.status_code == 200
    tasks = response.json()
    # assert len(tasks) == 2
    assert tasks[1]["title"] == "Task 1"
    assert tasks[2]["status"] == "done"


def test_update_task(client: TestClient) -> None:
    created = client.post(
        "/tasks",
        json={"title": "Initial title", "description": "Draft", "status": "todo"},
    ).json()

    response = client.patch(
        f"/tasks/{created['id']}",
        json={"title": "Updated title", "status": "in_progress"},
    )

    assert response.status_code == 200
    updated = response.json()
    assert updated["title"] == "Updated title"
    assert updated["status"] == "in_progress"
    assert updated["description"] == "Draft"


def test_delete_task(client: TestClient) -> None:
    created = client.post("/tasks", json={"title": "Disposable task"}).json()

    delete_response = client.delete(f"/tasks/{created['id']}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/tasks/{created['id']}")
    assert get_response.status_code == 404


def test_not_found_for_unknown_task(client: TestClient) -> None:
    response = client.get("/tasks/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"
