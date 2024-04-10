import threading

class KeyboardListener(threading.Thread):
    def __init__(self, process_input):
        super().__init__()
        self.process_input = process_input
    
    def run(self):
        while True:
            key = input("Enter something (press 'q' to quit): ")
            self.process_input("You entered: " + key)
            if key.lower() == 'q':
                break

# # Method to process the input
# def process_input(message):
#     print(message)

# # Create the KeyboardListener object
# listener_thread = KeyboardListener(process_input)

# # Start the thread
# listener_thread.start()

# # Main thread continues to execute
# # You can add more code here if needed

# # Wait for the listener thread to finish
# listener_thread.join()
# print("Listener thread has finished.")