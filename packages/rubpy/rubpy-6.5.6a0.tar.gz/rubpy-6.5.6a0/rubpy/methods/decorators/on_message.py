class OnMessage:
    def on_message(self, *args, **kwargs):
        def MetaHandler(func):
            self.add_handler(func, 'message_updates')
            return func
        return MetaHandler