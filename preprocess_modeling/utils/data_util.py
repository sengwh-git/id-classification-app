import os
import shutil
import random

def split_dataset(dataset_dir: str, output_dir: str, train_ratio: float, val_ratio: float, test_ratio: float) -> None:
    '''
    Splits the dataset into train, validation, and test directories based on the provided ratios.

    Args:
        dataset_dir: image directory
        output_dir: output directory for the split images
        train_ratio: ratio for training images
        val_ratio: ratio for validation images
        test_ratio: ratio for test images
    '''

    assert train_ratio + val_ratio + test_ratio == 1.0, "Split ratios must sum to 1.0"
    
    # list of countries
    countries = [d for d in os.listdir(dataset_dir) if os.path.isdir(os.path.join(dataset_dir, d))]
    
    for country in countries:
        country_dir = os.path.join(dataset_dir, country)
        images = [f for f in os.listdir(country_dir) if os.path.isfile(os.path.join(country_dir, f))]
        
        # shuffle
        random.shuffle(images)
        
        # split indices
        total_images = len(images)
        train_end = int(train_ratio * total_images)
        val_end = train_end + int(val_ratio * total_images)
        
        # split images
        train_images = images[:train_end]
        val_images = images[train_end:val_end]
        test_images = images[val_end:]
        
        # copy images to respective directories
        splits = {'train': train_images, 'val': val_images, 'test': test_images}
        
        for split, split_images in splits.items():
            split_country_dir = os.path.join(output_dir, split, country)
            os.makedirs(split_country_dir, exist_ok=True)
            for img_name in split_images:
                src = os.path.join(country_dir, img_name)
                dst = os.path.join(split_country_dir, img_name)
                shutil.copy2(src, dst)