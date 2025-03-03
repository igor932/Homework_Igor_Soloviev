class ActionNode:
    def __init__(self, action_id, timestamp, username, action_type):
        self.action_id = action_id
        self.timestamp = timestamp
        self.username = username
        self.action_type = action_type
        self.prev = None
        self.next = None
    
    def __str__(self):
        return f"{self.action_id} {self.timestamp} {self.username} {self.action_type}"


class ActionHistory:
    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None
        self.actions_map = {}
        self.next_id = 1

    def add_action(self, timestamp, username, action_type):
        new_action = ActionNode(self.next_id, timestamp, username, action_type)
        self.actions_map[self.next_id] = new_action
        self.next_id += 1
        
        if self.current is None:
            self.head = new_action
            self.tail = new_action
            self.current = new_action
        else:
            new_action.prev = self.current
            new_action.next = self.current.next
            
            if self.current.next:
                self.current.next.prev = new_action 
            
            self.current.next = new_action
            self.current = new_action
            
            if new_action.next is None:
                self.tail = new_action

    def undo(self):
        if self.current and self.current.prev:
            self.current = self.current.prev

    def redo(self):
        if self.current and self.current.next:
            self.current = self.current.next

    def find_action(self, action_id):
        return self.actions_map.get(action_id, None)

    def remove_action(self, action_id):
        action = self.actions_map.pop(action_id, None)
        
        if action:
            print(f"Удалена операция: {action.timestamp} {action.username} {action.action_type}")
            
            if action.prev:
                action.prev.next = action.next
            
            if action.next:
                action.next.prev = action.prev
            
            if action == self.head:
                self.head = action.next
            
            if action == self.tail:
                self.tail = action.prev
            
            if action == self.current:
                if action.prev:
                    self.current = action.prev
                else:
                    self.current = action.next
            self.reorder_action_ids()

    def reorder_action_ids(self):
        current = self.head
        new_id = 1
        new_map = {}
        
        while current:
            current.action_id = new_id
            new_map[new_id] = current
            new_id += 1
            current = current.next

        self.actions_map = new_map
        self.next_id = new_id

    def filter_and_remove(self, action_type):
        to_remove = []
        for action_id, action in self.actions_map.items():
            if action.action_type == action_type:
                to_remove.append(action_id)
        
        for action_id in to_remove:
            self.remove_action(action_id)

    def __iter__(self):
        current = self.head
        while current:
            yield current
            current = current.next
    
    def print_history(self):
        current = self.head
        
        while current:
            if current.action_id <= self.current.action_id:
                color = '\033[92m'
            else:
                color = '\033[90m'
            
            print(f"{color}{current.action_id} {current.timestamp} {current.username} {current.action_type}\033[0m")
            current = current.next


history = ActionHistory()
history.add_action("23.02.2025 11:40:00", "Олег", "Создание слоя")
history.add_action("23.02.2025 11:41:08", "Вася", "Заливка")
history.add_action("23.02.2025 11:42:15", "Маша", "Кисть")
history.add_action("23.02.2025 11:43:20", "Маша", "Кисть")

history.print_history()

history.undo()
print("\nПосле undo:") 
history.print_history()

history.redo()
print("\nПосле redo:")
history.print_history()

history.remove_action(2)
print("\nПосле удаления операции 2:")
history.print_history()

history.filter_and_remove("Кисть")
print("\nПосле удаления всех операций 'Кисть':")
history.print_history()
