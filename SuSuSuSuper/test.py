import tkinter as tk

class CheckboxApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Checkbox Example")

        # List to store checkbox variables and their associated texts
        self.check_vars = []
        self.check_buttons = []

        # Sample texts for checkboxes
        checkbox_texts = ["Option 1", "Option 2", "Option 3", "Option 4"]

        # Create checkboxes
        for text in checkbox_texts:
            var = tk.IntVar()  # Variable to store checkbox state
            chk = tk.Checkbutton(root, text=text, variable=var, command=self.on_checkbox_interact)
            chk.pack(anchor="w")
            # Store the variable and associated text
            self.check_vars.append((var, text))
            self.check_buttons.append(chk)

    def on_checkbox_interact(self):
        """Callback function for checkbox interaction"""
        checked_texts = self.get_checked_texts()
        print("Checked Options:", checked_texts)

    def get_checked_texts(self):
        """Return a list of texts for checkboxes that are checked."""
        checked_texts = [text for var, text in self.check_vars if var.get() == 1]
        return checked_texts

# Create the main window and run the app
root = tk.Tk()
app = CheckboxApp(root)
root.mainloop()
