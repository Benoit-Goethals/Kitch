from shiny import App, ui, reactive, render

# 1. Define your class
class Person:
    def __init__(self, name="", age=0):
        self.name = name
        self.age = age

    def greet(self):
        return f"Hello, my name is {self.name} and I am {self.age} years old."

# 2. UI part
app_ui = ui.page_fluid(
    ui.h2("Person Binding Example"),
    ui.input_text("name", "Enter name:", value="John Doe"),
    ui.input_numeric("age", "Enter age:", value=30),
    ui.output_text_verbatim("greeting")
)

# 3. Server logic
def server(input, output, session):
    person = reactive.value(Person())  # Create reactive person object

    @reactive.effect
    def _():
        # Update the person object when input changes
        person().name = input.name()
        person().age = input.age()

    @output
    @render.text
    def greeting():
        # Display greeting from person object
        return person().greet()

# 4. Create the app
app = App(app_ui, server)
