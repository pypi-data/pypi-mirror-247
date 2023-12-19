import requests
import threading
import time
import os
from tqdm import tqdm
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn, TransferSpeedColumn
from rich.prompt import Prompt
from rich.theme import Theme

# Create a console with a custom theme
custom_theme = Theme({
    "info": "dim cyan",
    "warning": "magenta",
    "danger": "bold red"
})
console = Console(theme=custom_theme)

pbar = None
pbar_lock = threading.Lock()

def download_file_part(url, destination, start_byte, part_size, part_num, total_size):
    global pbar
    part_filename = f"{destination}.part{part_num}"
    headers = {'Range': f'bytes={start_byte}-{start_byte + part_size - 1}'}
    response = requests.get(url, headers=headers, stream=True)

    if response.status_code == 206:  # Partial content
        with open(part_filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
                    with pbar_lock:  # Ensure thread-safe update of the progress bar
                        pbar.update(len(chunk))
            # print(f"Download completed. File saved as {part_filename}")
    else:
        print(f"Error: Failed to download file. HTTP status code: {response.status_code}")

def get_file_size(url):
    response = requests.head(url)
    content_length = response.headers.get('Content-Length')

    if content_length and content_length.isdigit():
        file_size = int(content_length)
        return file_size
    else:
        raise ValueError("Could not determine the file size or range support")
    
def supports_parallel_download(url):
    test_range = {'Range': 'bytes=0-0'}  # Requesting only the first byte
    response = requests.get(url, headers=test_range)

    if response.status_code == 206 and 'Content-Range' in response.headers:
        return True
    else:
        return False

def threaded_download(url, destination, num_parts):
    global pbar
    total_size = get_file_size(url)
    part_size = total_size // num_parts
    threads = []

    total_start_time = time.time()

    pbar = tqdm(total=total_size, unit='B', unit_scale=True, desc="Downloading")

    if not supports_parallel_download(url):
        print("Server does not support parallel downloads. Downloading in a single thread.")
        num_parts = 1  # Adjust to use only one thread

    with Progress(
        "[progress.description]{task.description}",
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        TextColumn("[bold blue]{task.completed}/{task.total}"),
        TimeRemainingColumn(),
        TransferSpeedColumn(),
        console=console
    ) as progress:
        download_task = progress.add_task("Downloading...", total=total_size)

    for part_num in range(num_parts):
        start_byte = part_num * part_size
        # Adjust the last part size
        if part_num == num_parts - 1:
            part_size = total_size - start_byte

        thread = threading.Thread(target=download_file_part, args=(url, destination, start_byte, part_size, part_num, total_size))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    
    pbar.close()

    # Combine the parts into a single file
    with open(destination, 'wb') as final_file:
        for part_num in range(num_parts):
            part_file_name = f"{destination}.part{part_num}"
            try:
                with open(part_file_name, 'rb') as part_file:
                    final_file.write(part_file.read())
                os.remove(part_file_name)
            except FileNotFoundError:
                print(f"Part file not found: {part_file_name}")
    
    total_end_time = time.time()

    print(f"All parts downloaded and combined in {total_end_time - total_start_time:.2f} seconds.")


def main():
    # console.print("[bold magenta]Welcome to Split Downloader Peta![/bold magenta]", justify="center")
    console.print("""
        [bold cyan]
        Welcome to Split Downloader Peta!
        =================================

            .-~~~-.
        .- ~ ~-(       )_ _
        /                    ~ -.
        |                          ',
        \                         .'
        ~- ._ ,. ,.,.,., ,.. -~

            ↓↓↓↓↓↓↓↓
        
        Fast and Reliable Downloads
        =================================
        [/bold cyan]
        """, justify="center")

    num_cpus = os.cpu_count()
    # print(f"Recommended number of threads (from 1 to max number of threads in your machine): 1 to {num_cpus}")

    url = console.input("[bold green]Please enter the URL of the file you want to download: [/bold green]")
    destination = console.input("[bold green]Please enter the destination folder path: [/bold green]")
    filename = console.input("[bold green]Please enter the filename to save as (including file extension): [/bold green]")

    while True:
        num_splits_input = console.input(f"[bold green]Please enter the number of splits(threads) between 1 and {num_cpus} for downloading: [/bold green]")
        try:
            num_splits = int(num_splits_input)
            if 1 <= num_splits <= num_cpus:
                break
            else:
                console.print(f"[red]Please enter a number between 1 and {num_cpus}.[/red]")
        except ValueError:
            console.print("[red]Invalid input. Please enter a valid integer.[/red]")
    
    # Ensure the destination directory exists
    if not os.path.isdir(destination):
        print(f"The specified destination directory {destination} does not exist.")
        return

    # Construct the full path for the file
    file_name = os.path.join(destination, url.split('/')[-1])
    file_path = os.path.join(destination, filename)

    # Start the download process
    print(f"Starting download from {url} to {file_path} using {num_splits} splits...")
    threaded_download(url, file_path, num_splits)
    print("Download finished!")


if __name__ == '__main__':
    main()