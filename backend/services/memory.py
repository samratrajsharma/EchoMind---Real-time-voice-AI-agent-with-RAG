class ConversationMemory:
    def __init__(self, max_history = 5):
        self.history = []
        self.max_history = max_history
    
    def add(self, role, content):
        self.history.append({
            "role":role,
            "content": content
        })

        if len(self.history) > self.max_history*2:
            self.history = self.history[-self.max_history * 2:]

    def get_history(self):
        return self.history