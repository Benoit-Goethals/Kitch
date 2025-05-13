from shiny.express import input, render, ui

ui.input_text("text", "Text input", "Enter text 2...")


@render.text
def value():
    return input.text()
