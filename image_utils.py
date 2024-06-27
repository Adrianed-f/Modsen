import os
import numpy as np
from PIL import Image, UnidentifiedImageError
import imagehash
import matplotlib.pyplot as plt
from collections import defaultdict


def load_images_from_folder(folder):
    """
    Загружает изображения из указанной папки.

    Args:
    - folder (str): Путь к папке с изображениями.

    Returns:
    - images (list): Список загруженных изображений в формате PIL.Image.
    - paths (list): Список путей к загруженным изображениям.
    """
    supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')
    images = []
    paths = []
    try:
        for filename in os.listdir(folder):
            if filename.lower().endswith(supported_formats):
                img_path = os.path.join(folder, filename)
                img = Image.open(img_path).convert('RGB')
                images.append(img)
                paths.append(img_path)
    except FileNotFoundError:
        print(f"Folder '{folder}' not found.")
    except PermissionError:
        print(f"Permission denied to access folder '{folder}'.")
    except Exception as e:
        print(f"Error loading images from folder '{folder}': {e}")
    return images, paths


def compute_hashes(images):
    """
    Вычисляет хэши для изображений.

    Args:
    - images (list): Список изображений в формате PIL.Image.

    Returns:
    - hashes (list): Список хэшей изображений.
    """
    hashes = []
    for img in images:
        img_hash = imagehash.phash(img)
        hashes.append(img_hash)
    return hashes


def find_duplicates(hashes, paths):
    """
    Находит дубликаты изображений на основе их хэшей.

    Args:
    - hashes (list): Список хэшей изображений.
    - paths (list): Список путей к изображениям.

    Returns:
    - duplicates (dict): Словарь с хэшами и списками путей к дубликатам.
    """
    hash_dict = defaultdict(list)
    for img_hash, path in zip(hashes, paths):
        hash_dict[img_hash].append(path)
    duplicates = {k: v for k, v in hash_dict.items() if len(v) > 1}
    return duplicates


def visualize_duplicates(duplicates, output_dir):
    """
    Визуализирует дубликаты изображений.

    Args:
    - duplicates (dict): Словарь с хэшами и списками путей к дубликатам.
    - output_dir (str): Папка для сохранения визуализаций.

    Side Effects:
    - Сохраняет изображения дубликатов в указанную папку.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for img_hash, paths in duplicates.items():
        fig, axes = plt.subplots(1, len(paths), figsize=(15, 5))
        for ax, path in zip(axes, paths):
            img = Image.open(path)
            ax.imshow(img)
            ax.set_title(os.path.basename(path))
            ax.axis('off')
        output_path = os.path.join(output_dir, f'duplicates_{img_hash}.png')
        plt.savefig(output_path)
        plt.close(fig)
        print(f'Duplicates saved to {output_path}')
