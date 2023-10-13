import tkinter as tk
import urllib.request
import urllib.parse
import json
import re

# Define the target languages (Bhojpuri and Dogri)
target_languages = {
    "bh": "Bhojpuri",
    "doi": "Dogri",
}

def translate_to_languages(input_text):
    translations = {}

    # Split the input text into sentences
    sentences = re.split(r'(?<=[.!?])', input_text)

    # Translate each sentence to the target languages
    for lang_code, lang_name in target_languages.items():
        translated_sentences = []
        for sentence in sentences:
            if sentence.strip():  # Skip empty sentences
                translated_sentence = translate_sentence(sentence, lang_code)
                translated_sentences.append(translated_sentence)
        translations[lang_name] = ' '.join(translated_sentences)

    return translations

def translate_sentence(sentence, target_language):
    # Create the URL for the translation request
    base_url = "https://translate.googleapis.com/translate_a/single"
    params = {
        'client': 'gtx',
        'sl': 'hi',  # Source language is Hindi
        'tl': target_language,
        'dt': 't',
        'q': sentence
    }
    url = f"{base_url}?{urllib.parse.urlencode(params)}"

    try:
        # Send the HTTP request and read the response
        response = urllib.request.urlopen(url)
        translation_data = json.loads(response.read().decode('utf-8'))

        # Extract and return the translated text
        translated_text = translation_data[0][0][0]
        return translated_text

    except Exception as e:
        return f"Translation failed: {str(e)}"

def translate_text():
    input_text = input_text_widget.get("1.0", "end-1c")  # Get all text from the widget
    translations = translate_to_languages(input_text)

    # Clear previous content
    for widget in output_widgets.values():
        widget.config(state="normal")
        widget.delete("1.0", "end")
        widget.config(state="disabled")

    # Update the output for each language
    for lang_name, translation in translations.items():
        output_text_widget = output_widgets[lang_name]
        output_text_widget.config(state="normal")
        output_text_widget.insert("1.0", translation)
        output_text_widget.config(state="disabled")

# Create a Tkinter window
window = tk.Tk()
window.title("Hindi to Bhojpuri and Dogri Translator")

# Center the window on the screen
window_width = 600
window_height = 600
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Create and place GUI elements
input_label = tk.Label(window, text="Enter text in Hindi:")
input_label.pack(pady=10)

input_text_widget = tk.Text(window, height=5, width=40)
input_text_widget.pack(pady=5, padx=20)

translate_button = tk.Button(window, text="Translate", command=translate_text)
translate_button.pack(pady=10)

output_widgets = {}

# Create and configure output widgets for each language
for lang_name in target_languages.values():
    output_label = tk.Label(window, text=f"Translation in {lang_name}:")
    output_label.pack(pady=5)
    
    output_text_widget = tk.Text(window, height=5, width=40)
    output_text_widget.pack(pady=5, padx=20)
    output_text_widget.config(state="disabled")  # Disable editing
    output_widgets[lang_name] = output_text_widget

# Start the Tkinter main loop
window.mainloop()
