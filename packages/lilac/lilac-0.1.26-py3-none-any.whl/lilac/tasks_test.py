"""Tests for tasks.py."""


from .tasks import TaskManager


def test_task_manager_outside_event_loop() -> None:
  # Make sure we can make a default TaskManager from outside a running loop.
  task_manager = TaskManager()
  assert task_manager is not None
  task_manager.stop()


async def test_async_task_manager_outside_event_loop() -> None:
  # Make sure we can make a default TaskManager from outside a running loop.
  task_manager = TaskManager()
  assert task_manager is not None
  task_manager.stop()
