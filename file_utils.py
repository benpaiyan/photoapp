import os
import shutil
import logging
import string
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.uix.label import Label
from collections import defaultdict
from threading import Thread

from .jpg_metadata_utils import (
    get_exif_data,
    extract_capture_date,
    extract_camera_info,
    write_city_name,
    get_photo_count,
    log_not_moved,
)
from .image_utils import (
    is_image_file,
    is_video_file,
    is_low_quality_image,
    hash_file,
)
from .geocode_utils import reverse_geocode, get_gps_coordinates

Logger = logging.getLogger("FileProcessor")
Logger.setLevel(logging.DEBUG)
Logger.debug("Debug logging enabled")

day_mapping = defaultdict(dict)
day_counter = defaultdict(lambda: defaultdict(int))

def process_file_show_progress(self, source_folder, destination_folder):
    Logger.debug("[TIDY] file_utils process_file_show_progress")
    progress_bar = ProgressBar(max=100)
    progress_label = Label(text="Processing... 0%")

    def start_processing():
        Logger.debug("[TIDY] file_utils start_processing")
        process_files_new(self, source_folder, destination_folder, progress_bar, progress_label)
        Logger.debug("[TIDY] file_utils drop")

    thread = Thread(target=start_processing, daemon=True)
    thread.start()

def process_files_new(self, source_folder, destination_folder, progress_bar, progress_label):
    Logger.debug("[TIDY] file_utils process_files_new")
    file_hashes = {}
    files_to_process = []
    
    for root, _, files in os.walk(source_folder):
        for filename in files:
            file_path = os.path.join(root, filename)
            if is_image_file(filename) or is_video_file(filename):
                files_to_process.append(file_path)
    
    files_to_process.sort(key=lambda x: extract_capture_date(get_exif_data(x), x) or x)
    total_files = len(files_to_process)
    processed_files = 0
    
    for file_path in files_to_process:
        filename = os.path.basename(file_path)
        file_hash = hash_file(file_path)
        if file_hash in file_hashes:
            try:
                os.remove(file_path)
                log_not_moved(filename, "Duplicate - Removed")
            except FileNotFoundError:
                Logger.warning(f"File {file_path} not found while trying to delete duplicate.")
            continue
        else:
            file_hashes[file_hash] = file_path

        if is_image_file(filename) and is_low_quality_image(file_path):
            log_not_moved(filename, "Low Quality")
            continue

        exif_data = get_exif_data(file_path)
        capture_date = extract_capture_date(exif_data, file_path)
        camera_brand, camera_model = extract_camera_info(exif_data)
        lat, lon = get_gps_coordinates(exif_data)
        city_name = reverse_geocode(lat, lon) if lat and lon else None
        if city_name:
            write_city_name(file_path, city_name)

        new_filename = generate_new_filename(
            capture_date, camera_brand, camera_model, city_name, filename
        )
        destination_path = create_destination_path(destination_folder, capture_date, new_filename)

        try:
            shutil.copy2(file_path, destination_path)
            Logger.debug(f"[GANESH] {file_path} -> {destination_folder}")
            processed_files += 1
            progress = (processed_files / total_files) * 100
            Clock.schedule_once(lambda dt: update_progress(self, progress_bar, progress_label, progress), 0)
        except shutil.Error as e:
            log_not_moved(filename, str(e))
    
    Clock.schedule_once(lambda dt: update_progress(self, progress_bar, progress_label, 100), 0)

def update_progress(self, progress_bar, progress_label, progress):
    Logger.debug("[TIDY] file_utils update_progress")
    progress_bar.value = progress
    progress_label.text = f"Processing... {int(progress)}%"
    self.progressbarpopup.custom_progress_bar_text = progress
    if progress == 100:
        self.progressbarpopup.title = "Organizing completed"

def create_destination_path(destination_folder, capture_date, new_filename):
    Logger.debug("[TIDY] file_utils create_destination_path")
    if capture_date is None:
        raise ValueError("capture_date is None, cannot generate destination path.")

    year = str(capture_date.year)
    month = str(capture_date.month).zfill(2)
    actual_day = capture_date.day
    
    # Ensure correct day mapping by sorting and assigning correct order
    sorted_days = sorted(day_mapping[(year, month)].keys())
    if actual_day not in sorted_days:
        existing_day_numbers = {int(v.split("_")[1]) for v in day_mapping[(year, month)].values()}
        next_day_number = max(existing_day_numbers, default=0) + 1
        day_counter[year][month] = next_day_number
        formatted_date = capture_date.strftime("%d-%m-%Y")
        day_mapping[(year, month)][actual_day] = f"Day_{next_day_number}_({formatted_date})"
    
    dayX = day_mapping[(year, month)][actual_day]
    organized_root = os.path.join(destination_folder, "organized_folder")
    destination_day_folder = os.path.join(organized_root, dayX)
    os.makedirs(destination_day_folder, exist_ok=True)
    
    return os.path.join(destination_day_folder, new_filename)

def generate_new_filename(capture_date, camera_brand, camera_model, city_name, original_filename):
    Logger.debug("[TIDY] file_utils generate_new_filename")
    file_extension = os.path.splitext(original_filename)[1]
    year = capture_date.strftime('%Y')
    month = capture_date.strftime('%m')
    day = capture_date.strftime('%d')
    new_filename = f"{year}_{month}_{day}_"

    if camera_brand != 'Unknown':
        new_filename += f"{camera_brand}_"
    new_filename += f"{camera_model}"

    if city_name:
        new_filename += f"_{city_name}"

    photo_count = get_photo_count(camera_model, capture_date)
    new_filename += f"_{photo_count}{file_extension}"
    
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    return ''.join(c for c in new_filename if c in valid_chars)

def resolve_duplicate_filename(destination_folder, filename, max_retries=1000):
    Logger.debug("[TIDY] file_utils resolve_duplicate_filename")
    file_name, file_extension = os.path.splitext(filename)
    counter = 1
    while counter <= max_retries:
        new_filename = f"{file_name}_{counter}{file_extension}"
        if not os.path.exists(os.path.join(destination_folder, new_filename)):
            return new_filename
        counter += 1
    raise RuntimeError(f"Could not resolve filename conflict for {filename} after {max_retries} attempts.")

def delete_empty_folders(directory):
    Logger.debug("[TIDY] file_utils delete_empty_folders")
    for root, dirs, files in os.walk(directory, topdown=False):
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            if not os.listdir(folder_path):
                os.rmdir(folder_path)

