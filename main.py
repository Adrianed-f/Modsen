import os
import shutil
from image_utils import load_images_from_folder, compute_hashes, find_duplicates, visualize_duplicates
from compare_folders import compare_folders
from feature_extraction import feature_extraction_model_keras, extract_features_keras, find_duplicates_with_features


def main():
    """
    Основная функция программы для поиска дубликатов изображений.
    """
    # Пути к папкам с изображениями и папке для сохранения результатов
    folder1 = "Lilly"
    folder2 = "Lotus"
    output_dir = "output"

    # Проверка существования папки output и создание её, если она не существует
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    try:
        # Поиск дубликатов внутри одной папки
        print("Searching for duplicates within the same folder...")
        images1, paths1 = load_images_from_folder(folder1)
        hashes1 = compute_hashes(images1)
        duplicates_within_folder = find_duplicates(hashes1, paths1)

        for img_hash, paths in duplicates_within_folder.items():
            print(f"Duplicate images with hash {img_hash}:")
            for path in paths:
                print(f"  {path}")

        visualize_duplicates(duplicates_within_folder, output_dir)

        # Сравнение двух папок на наличие дубликатов
        print("\nComparing two folders for duplicates...")
        duplicates_between_folders = compare_folders(folder1, folder2)

        for img_hash, (paths1, paths2) in duplicates_between_folders.items():
            print(f"Duplicate images with hash {img_hash}:")
            for path in paths1:
                print(f"  {path} (from folder 1)")
            for path in paths2:
                print(f"  {path} (from folder 2)")

        # Поиск дубликатов с использованием извлечения признаков Keras
        print("\nFinding duplicates using Keras feature extraction...")
        keras_model = feature_extraction_model_keras()
        feature_duplicates_keras = find_duplicates_with_features(folder1, folder2, keras_model)

        for path1, path2 in feature_duplicates_keras:
            print(f"Duplicate images based on Keras features: {path1} and {path2}")

    except Exception as e:
        print(f"Error occurred: {str(e)}")


if __name__ == "__main__":
    main()
