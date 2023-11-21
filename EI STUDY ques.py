#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from datetime import datetime
from typing import List
class Memento:
    def __init__(self, state):
        self._state = state
    def get_state(self):
        return self._state
class Task:
    def __init__(self, description, completed=False, due_date=None, tags=None):
        self.description = description
        self.completed = completed
        self.due_date = due_date
        self.tags = tags if tags else []
    def mark_completed(self):
        self.completed = True
    def mark_pending(self):
        self.completed = False
    def add_tag(self, tag):
        self.tags.append(tag)
    def remove_tag(self, tag):
        self.tags.remove(tag)
    def show_details(self):
        status = "Completed" if self.completed else "Pending"
        due_date_info = f", Due: {self.due_date}" if self.due_date else ""
        tags_info = f", Tags: {', '.join(self.tags)}" if self.tags else ""
        return f"{self.description} - {status}{due_date_info}{tags_info}"
class TaskBuilder:
    def __init__(self, description):
        self.task = Task(description)
    def set_due_date(self, due_date):
        self.task.due_date = due_date
        return self
    def add_tag(self, tag):
        self.task.tags.append(tag)
        return self
    def build(self):
        return self.task
class TaskList:
    def __init__(self):
        self.tasks = []
        self.mementos = []
    def add_task(self, task):
        self.tasks.append(task)
        self.save_state()
    def delete_task(self, task):
        self.tasks.remove(task)
        self.save_state()
    def mark_completed(self, task):
        task.mark_completed()
        self.save_state()
    def mark_pending(self, task):
        task.mark_pending()
        self.save_state()
    def save_state(self):
        state = [task.__dict__ for task in self.tasks]
        self.mementos.append(Memento(state))
    def undo(self):
        if len(self.mementos) > 1:
            self.mementos.pop()
            previous_state = self.mementos[-1].get_state()
            self.tasks = [Task(**task) for task in previous_state]
    def view_tasks(self, filter_option=None):
        if filter_option == "completed":
            filtered_tasks = [task for task in self.tasks if task.completed]
        elif filter_option == "pending":
            filtered_tasks = [task for task in self.tasks if not task.completed]
        else:
            filtered_tasks = self.tasks

        for task in filtered_tasks:
            print(task.show_details())
if __name__ == "__main__":
    todo_list = TaskList()
    while True:
        print("\n=== To-Do List Manager ===")
        print("1. Add Task")
        print("2. Mark Task as Completed")
        print("3. Delete Task")
        print("4. View Tasks")
        print("5. Undo")
        print("6. Exit")
        choice = input("Enter your choice (1-6): ")
        if choice == "1":
            description = input("Enter task description: ")
            due_date = input("Enter due date (optional, press Enter to skip): ")
            tags = input("Enter tags (optional, separate by commas, press Enter to skip): ").split(",")
            tags = [tag.strip() for tag in tags if tag.strip()]
            task_builder = TaskBuilder(description)
            if due_date:
                task_builder.set_due_date(due_date)
            for tag in tags:
                task_builder.add_tag(tag)
            new_task = task_builder.build()
            todo_list.add_task(new_task)
        elif choice == "2":
            todo_list.view_tasks()
            task_description = input("Enter task description to mark as completed: ")
            task_to_mark = next((task for task in todo_list.tasks if task.description == task_description), None)
            if task_to_mark:
                todo_list.mark_completed(task_to_mark)
                print(f'Task "{task_description}" marked as completed.')
            else:
                print(f'Task "{task_description}" not found.')
        elif choice == "3":
            todo_list.view_tasks()
            task_description = input("Enter task description to delete: ")
            task_to_delete = next((task for task in todo_list.tasks if task.description == task_description), None)
            if task_to_delete:
                todo_list.delete_task(task_to_delete)
                print(f'Task "{task_description}" deleted.')
            else:
                print(f'Task "{task_description}" not found.')
        elif choice == "4":
            filter_option = input("Enter filter option (all/completed/pending): ")
            todo_list.view_tasks(filter_option.lower())
        elif choice == "5":
            todo_list.undo()
            print("Undo completed.")

        elif choice == "6":
            print("Exiting To-Do List Manager.")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

