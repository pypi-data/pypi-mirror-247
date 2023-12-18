import requests
import threading
import time
import os

def download_file_part(url, destination, start_byte, part_size, part_num):
    # Updated file name to include only the start byte
    part_filename = f"{destination}.part{part_num}"
    headers = {'Range': f'bytes={start_byte}-{start_byte + part_size - 1}'}
    response = requests.get(url, headers=headers, stream=True)

    if response.status_code == 206:  # Partial content
        with open(part_filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
            # print(f"Download completed. File saved as {part_filename}")
    else:
        print(f"Error: Failed to download file. HTTP status code: {response.status_code}")

def get_file_size(url):
    response = requests.head(url)
    content_length = response.headers.get('Content-Length')
    if content_length and content_length.isdigit():
        return int(content_length)
    else:
        raise ValueError("Could not determine the file size")

def threaded_download(url, destination, num_parts):
    total_size = get_file_size(url)
    part_size = total_size // num_parts
    threads = []

    total_start_time = time.time()

    for part_num in range(num_parts):
        start_byte = part_num * part_size
        # Adjust the last part size
        if part_num == num_parts - 1:
            part_size = total_size - start_byte

        thread = threading.Thread(target=download_file_part, args=(url, destination, start_byte, part_size, part_num))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

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
    print("Welcome to the Download Manager")
    url = input("Please enter the URL of the file you want to download: ")
    destination = input("Please enter the destination folder path: ")
    filename = input("Please enter the filename to save as (including file extension): ")
    num_splits = input("Please enter the number of splits (threads) for downloading: ")

    try:
        num_splits = int(num_splits)
    except ValueError:
        print("Number of splits must be an integer.")
        return
    
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


# url = 'https://eoimages.gsfc.nasa.gov/images/imagerecords/73000/73751/world.topo.bathy.200407.3x5400x2700.jpg'
# destination = '/Users/home/Documents/projects/Download Manager/coding/img_4.png'
# threaded_download(url, destination, num_parts=3)