import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Model


def feature_extraction_model_keras(weights_path=None):
    """
    Инициализирует модель для извлечения признаков изображений с использованием ResNet50.

    Args:
    - weights_path (str): Путь к предварительно обученным весам модели.

    Returns:
    - model (tensorflow.keras.Model): Загруженная модель ResNet50 для извлечения признаков.
    """
    if weights_path:
        base_model = ResNet50(weights=None, include_top=False, pooling='avg')
        base_model.load_weights(weights_path)
    else:
        base_model = ResNet50(weights='imagenet', include_top=False, pooling='avg')
    model = Model(inputs=base_model.input, outputs=base_model.output)
    return model


def extract_features_keras(img_paths, model):
    """
    Извлекает признаки изображений с помощью предварительно обученной модели ResNet50.

    Args:
    - img_paths (list): Список путей к изображениям.
    - model (tensorflow.keras.Model): Загруженная модель ResNet50 для извлечения признаков.

    Returns:
    - features (numpy.ndarray): Матрица признаков изображений.
    """
    features = []
    for path in img_paths:
        img = image.load_img(path, target_size=(224, 224))
        img_data = image.img_to_array(img)
        img_data = np.expand_dims(img_data, axis=0)
        img_data = preprocess_input(img_data)
        feature = model.predict(img_data)
        features.append(feature.flatten())
    return np.array(features)


def find_duplicates_with_features(folder1, folder2, model):
    """
    Находит дубликаты изображений на основе признаков, извлеченных с помощью модели ResNet50.

    Args:
    - folder1 (str): Путь к первой папке с изображениями.
    - folder2 (str): Путь ко второй папке с изображениями.
    - model (tensorflow.keras.Model): Загруженная модель ResNet50 для извлечения признаков.

    Returns:
    - duplicates (list): Список кортежей с парами путей к дубликатам изображений.
    """
    from image_utils import load_images_from_folder

    images1, paths1 = load_images_from_folder(folder1)
    images2, paths2 = load_images_from_folder(folder2)

    features1 = extract_features_keras(paths1, model)
    features2 = extract_features_keras(paths2, model)

    duplicates = []
    for i, f1 in enumerate(features1):
        for j, f2 in enumerate(features2):
            if np.linalg.norm(f1 - f2) < 0.1:
                duplicates.append((paths1[i], paths2[j]))

    return duplicates
