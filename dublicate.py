import os
import numpy as np
import pandas as pd
import cv2
from PIL import Image, UnidentifiedImageError
import imagehash
import matplotlib.pyplot as plt
from collections import defaultdict
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Model


def load_images_from_folder(folder):
    supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')
    images = []
    paths = []
    for filename in os.listdir(folder):
        if filename.lower().endswith(supported_formats):
            img_path = os.path.join(folder, filename)
            try:
                img = Image.open(img_path).convert('RGB')
                images.append(img)
                paths.append(img_path)
            except UnidentifiedImageError:
                print(f"Could not identify image file {img_path}, skipping.")
    return images, paths


def compute_hashes(images):
    hashes = []
    for img in images:
        img_hash = imagehash.phash(img)
        hashes.append(img_hash)
    return hashes


def find_duplicates(hashes, paths):
    hash_dict = defaultdict(list)
    for img_hash, path in zip(hashes, paths):
        hash_dict[img_hash].append(path)

    duplicates = {k: v for k, v in hash_dict.items() if len(v) > 1}
    return duplicates


def visualize_duplicates(duplicates):
    for img_hash, paths in duplicates.items():
        fig, axes = plt.subplots(1, len(paths), figsize=(15, 5))
        for ax, path in zip(axes, paths):
            img = Image.open(path)
            ax.imshow(img)
            ax.set_title(os.path.basename(path))
            ax.axis('off')
        plt.show()


def compare_folders(folder1, folder2):
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


def feature_extraction_model(weights_path=None):
    if weights_path:
        base_model = ResNet50(weights=None, include_top=False, pooling='avg')
        base_model.load_weights(weights_path)
    else:
        base_model = ResNet50(weights='imagenet', include_top=False, pooling='avg')
    model = Model(inputs=base_model.input, outputs=base_model.output)
    return model


def extract_features(img_paths, model):
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
    images1, paths1 = load_images_from_folder(folder1)
    images2, paths2 = load_images_from_folder(folder2)

    features1 = extract_features(paths1, model)
    features2 = extract_features(paths2, model)

    duplicates = []
    for i, f1 in enumerate(features1):
        for j, f2 in enumerate(features2):
            if np.linalg.norm(f1 - f2) < 0.1:
                duplicates.append((paths1[i], paths2[j]))

    return duplicates


def main():
    folder1 = r"D:\Modsen\find_dublicate\Lilly"
    folder2 = r"D:\Modsen\find_dublicate\Lotus"

    print("Searching for duplicates within the same folder...")
    images1, paths1 = load_images_from_folder(folder1)
    hashes1 = compute_hashes(images1)
    duplicates_within_folder = find_duplicates(hashes1, paths1)

    for img_hash, paths in duplicates_within_folder.items():
        print(f"Duplicate images with hash {img_hash}:")
        for path in paths:
            print(f"  {path}")

    visualize_duplicates(duplicates_within_folder)

    print("\nComparing two folders for duplicates...")
    duplicates_between_folders = compare_folders(folder1, folder2)

    for img_hash, (paths1, paths2) in duplicates_between_folders.items():
        print(f"Duplicate images with hash {img_hash}:")
        for path in paths1:
            print(f"  {path} (from folder 1)")
        for path in paths2:
            print(f"  {path} (from folder 2)")

    print("\nFinding duplicates using feature extraction...")
    weights_path = r"D:\Modsen\find_dublicate\resnet50_weights_tf_dim_ordering_tf_kernels_notop.h5"
    model = feature_extraction_model(weights_path=weights_path)
    feature_duplicates = find_duplicates_with_features(folder1, folder2, model)

    for path1, path2 in feature_duplicates:
        print(f"Duplicate images based on features: {path1} and {path2}")
        img1 = Image.open(path1)
        img2 = Image.open(path2)
        fig, axes = plt.subplots(1, 2, figsize=(10, 5))
        axes[0].imshow(img1)
        axes[0].set_title(os.path.basename(path1))
        axes[0].axis('off')
        axes[1].imshow(img2)
        axes[1].set_title(os.path.basename(path2))
        axes[1].axis('off')
        plt.show()


if __name__ == "__main__":
    main()