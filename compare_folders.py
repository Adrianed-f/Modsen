from image_utils import load_images_from_folder, compute_hashes, find_duplicates
from collections import defaultdict


def compare_folders(folder1, folder2):
    """
    Сравнивает две папки на наличие дубликатов изображений.

    Args:
    - folder1 (str): Путь к первой папке с изображениями.
    - folder2 (str): Путь к второй папке с изображениями.

    Returns:
    - duplicates (dict): Словарь с хэшами и парами списков путей к дубликатам.
    """
    images1, paths1 = load_images_from_folder(folder1)
    images2, paths2 = load_images_from_folder(folder2)

    hashes1 = compute_hashes(images1)
    hashes2 = compute_hashes(images2)

    hash_dict1 = defaultdict(list)
    for img_hash, path in zip(hashes1, paths1):
        hash_dict1[img_hash].append(path)

    hash_dict2 = defaultdict(list)
    for img_hash, path in zip(hashes2, paths2):
        hash_dict2[img_hash].append(path)

    duplicates = {}
    for h, p1 in hash_dict1.items():
        if h in hash_dict2:
            duplicates[h] = (p1, hash_dict2[h])

    return duplicates
