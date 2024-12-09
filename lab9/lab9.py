from uuid import uuid4, UUID
from datetime import datetime
from enum import Enum


class Status(Enum):
    ToDo = "ToDo"
    InProgress = "InProgress"
    Done = "Done"


class Task:
    def __init__(self, description: str, schedule_for: datetime):
        self.id = uuid4()
        self.description = description
        self.created_at = datetime.now()
        self.schedule_for = schedule_for
        self.status = Status.ToDo

    def to_dict(self):
        """Повертає об'єкт у вигляді словника для подальшого відображення."""
        return {
            "ID": str(self.id),
            "Description": self.description,
            "Created At": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "Scheduled For": self.schedule_for.strftime("%Y-%m-%d %H:%M:%S"),
            "Status": self.status.value,
        }


class TaskController:
    def __init__(self):
        self.tasks = {}

    def add_task(self, description: str, schedule_for: datetime):
        if not description.strip():
            raise ValueError("Description cannot be empty.")

        if not isinstance(schedule_for, datetime):
            raise ValueError("schedule_for must be a datetime object.")

        # Створення об'єкта Task тільки після перевірок
        task = Task(description, schedule_for)
        self.tasks[task.id] = task
        return task

    def update_task_status(self, task_id: str, new_status: str):
        try:
            task_uuid = UUID(task_id)
            task = self.tasks.get(task_uuid, None)
            if not task:
                raise ValueError("Task ID not found.")
            if new_status not in Status.__members__:
                raise ValueError("Invalid status value.")
            task.status = Status[new_status]
            return True
        except ValueError as e:
            raise e


    def delete_task(self, task_id: str):
        try:
            task_uuid = UUID(task_id)
            return self.tasks.pop(task_uuid, None)
        except ValueError:
            print("Error: Invalid Task ID.")
            return None

    def update_task(self, task_id: str, new_description: str = None, new_schedule: str = None):
        try:
            task_uuid = UUID(task_id)
            task = self.tasks.get(task_uuid, None)
            if not task:
                raise ValueError("Task ID not found.")
            if new_description:
                task.description = new_description
            if new_schedule:
                try:
                    task.schedule_for = datetime.strptime(new_schedule, "%Y-%m-%d %H:%M")
                except ValueError:
                    raise ValueError("Invalid date format. Use YYYY-MM-DD HH:MM.")
            return task
        except ValueError as e:
            print(f"Error: {e}")
            return None

    def get_all_tasks(self):
        return list(self.tasks.values())

    def filter_tasks_by_status(self, status: str):
        try:
            if status not in Status.__members__:
                raise ValueError("Invalid status value.")
            return [task for task in self.tasks.values() if task.status == Status[status]]
        except ValueError as e:
            print(f"Error: {e}")
            return []

    def get_task_by_id(self, task_id: str):
        try:
            task_uuid = UUID(task_id)
            return self.tasks.get(task_uuid, None)
        except ValueError:
            print("Error: Invalid Task ID.")
            return None


class TaskView:
    @staticmethod
    def display_tasks(tasks):
        if not tasks:
            print("No tasks available.")
            return

        print(f"{'ID':<43} {'Description':<20} {'Created At':<20} {'Scheduled For':<20} {'Status':<12}")
        print("-" * 110)
        for task in tasks:
            data = task.to_dict()
            print(f"{data['ID']:<46} {data['Description']:<20} {data['Created At']:<20} {data['Scheduled For']:<20} {data['Status']:<12}")


def main():
    controller = TaskController()
    view = TaskView()

    while True:
        print("\n1. Add Task")
        print("2. Update Task Status")
        print("3. Delete Task")
        print("4. Update Task")
        print("5. Show All Tasks")
        print("6. Filter Tasks By Status")
        print("7. Show Task By ID")
        print("8. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            description = input("Enter task description: ")
            schedule_for = input("Enter schedule time (YYYY-MM-DD HH:MM): ")
            try:
                schedule_time = datetime.strptime(schedule_for, "%Y-%m-%d %H:%M")
                task = controller.add_task(description, schedule_time)
                print("Task added:", task.to_dict())
            except ValueError:
                print("Error: Invalid date format. Use YYYY-MM-DD HH:MM.")

        elif choice == "2":
            task_id = input("Enter task ID: ")
            new_status = input("Enter new status (ToDo/InProgress/Done): ")
            if controller.update_task_status(task_id, new_status):
                print("Status updated.")
            else:
                print("Failed to update status.")

        elif choice == "3":
            task_id = input("Enter task ID: ")
            deleted_task = controller.delete_task(task_id)
            print("Task deleted." if deleted_task else "Task not found.")

        elif choice == "4":
            task_id = input("Enter task ID: ")
            new_description = input("Enter new description (leave blank to keep): ")
            new_schedule = input("Enter new schedule time (YYYY-MM-DD HH:MM) or leave blank: ")
            updated_task = controller.update_task(task_id, new_description, new_schedule)
            print("Task updated:", updated_task.to_dict() if updated_task else "Task not found.")

        elif choice == "5":
            tasks = controller.get_all_tasks()
            view.display_tasks(tasks)

        elif choice == "6":
            status = input("Enter status to filter (ToDo/InProgress/Done): ")
            tasks = controller.filter_tasks_by_status(status)
            view.display_tasks(tasks)

        elif choice == "7":
            task_id = input("Enter task ID: ")
            task = controller.get_task_by_id(task_id)
            if task:
                view.display_tasks([task])
            else:
                print("Task not found.")

        elif choice == "8":
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
