import pytest
from datetime import datetime, timedelta
from uuid import uuid4
from lab9 import TaskController, Status


# Тести додавання завдань
@pytest.mark.parametrize(
    "description,schedule_for",
    [
        ("Test Task 1", datetime.now() + timedelta(days=1)),
        ("Another Task", datetime.now() + timedelta(hours=5)),
    ],
)
def test_add_task_valid_input(description, schedule_for):
    controller = TaskController()
    task = controller.add_task(description, schedule_for)
    assert task.description == description
    assert task.schedule_for == schedule_for
    assert task.status == Status.ToDo
    assert len(controller.tasks) == 1


# Тести оновлення статусу
@pytest.mark.parametrize(
    "initial_status,new_status",
    [
        (Status.ToDo.value, Status.InProgress.value),
        (Status.InProgress.value, Status.Done.value),
    ],
)
def test_update_task_status(initial_status, new_status):
    controller = TaskController()
    task = controller.add_task("Task with Status", datetime.now() + timedelta(days=1))
    task.status = Status[initial_status]
    assert controller.update_task_status(str(task.id), new_status)
    assert task.status == Status[new_status]


# Тести видалення завдань
def test_delete_task():
    controller = TaskController()
    task = controller.add_task("Task to Delete", datetime.now() + timedelta(days=1))
    deleted_task = controller.delete_task(str(task.id))
    assert deleted_task is not None
    assert len(controller.tasks) == 0


# Тести отримання завдань
def test_get_task_by_id():
    controller = TaskController()
    task = controller.add_task("Task to Get", datetime.now() + timedelta(days=1))
    fetched_task = controller.get_task_by_id(str(task.id))
    assert fetched_task == task


# Тести некоректного вводу під час додавання завдань
@pytest.mark.parametrize(
    "description,schedule_for,expected_exception",
    [
        ("", datetime.now() + timedelta(days=1), ValueError),  # Порожній опис
        ("Valid Task", "Invalid Date", ValueError),  # Некоректна дата
    ],
)
def test_add_task_invalid_input(description, schedule_for, expected_exception):
    controller = TaskController()
    with pytest.raises(expected_exception):
        controller.add_task(description, schedule_for)


# Тести оновлення статусу з некоректними даними
@pytest.mark.parametrize(
    "task_id,new_status,expected_exception",
    [
        (str(uuid4()), "InvalidStatus", ValueError),
        ("InvalidUUID", Status.ToDo.value, ValueError),
    ],
)
def test_update_task_status_invalid_input(task_id, new_status, expected_exception):
    controller = TaskController()
    with pytest.raises(expected_exception):
        controller.update_task_status(task_id, new_status)


# Тести видалення з некоректним ID
def test_delete_task_invalid_id():
    controller = TaskController()
    result = controller.delete_task("InvalidUUID")
    assert result is None


# Тести отримання завдання з некоректним ID
def test_get_task_by_invalid_id():
    controller = TaskController()
    task = controller.get_task_by_id("InvalidUUID")
    assert task is None

