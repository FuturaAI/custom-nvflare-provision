#!/usr/bin/env python3
import os
import sys
import json
from config.generate_image_dataset import split_dataset
import time

def update_and_rename_resources_file(project_name, site_path):
    resources_default = os.path.join("workspace", project_name, "prod_00", site_path, "local", "resources.json.default")
    resources_json = os.path.join("workspace", project_name, "prod_00", site_path, "local", "resources.json")
    
    if os.path.exists(resources_default):
        # Read the JSON file
        with open(resources_default, 'r') as f:
            data = json.load(f)
        
        # Update the GPU values
        for component in data['components']:
            if component['id'] == 'resource_manager':
                component['args']['num_of_gpus'] = 1
                component['args']['mem_per_gpu_in_GiB'] = 1
        
        # Write the modified content to the new file
        with open(resources_json, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Remove the .default file
        os.remove(resources_default)

def wait_for_path(project_name, site_path):  # site_path like "localhost" or "site-1" or "site-2"
    base_path = os.path.join("workspace", project_name, "prod_00", site_path, "local")
    timeout = 10  # 10 seconds
    start_time = time.time()
    
    while not os.path.exists(base_path):
        if time.time() - start_time > timeout:
            raise TimeoutError(f"Timeout waiting for path {base_path} to exist")
        print(f"Waiting for path {base_path} to exist...")
        time.sleep(5)  # Check every 5 seconds
    
    # Once base path exists, create the remaining structure
    full_path = os.path.join(base_path, "images", "split_images")
    os.makedirs(full_path, exist_ok=True)
    return full_path

def main():
    if len(sys.argv) != 2:
        print("Error: Project name not provided!")
        print("Usage: python prebuild_images_split.py <project_name>")
        sys.exit(1)
        
    project_name = sys.argv[1]
    
    # Update and rename resources.json.default to resources.json for site-1 and site-2
    update_and_rename_resources_file(project_name, "site-1")
    update_and_rename_resources_file(project_name, "site-2")
    
    split_images_output_dir_server = wait_for_path(project_name, "localhost")
    split_images_output_dir_site1 = wait_for_path(project_name, "site-1")
    split_images_output_dir_site2 = wait_for_path(project_name, "site-2")

    split_dataset('images', split_images_output_dir_server)
    split_dataset('images', split_images_output_dir_site1)
    split_dataset('images', split_images_output_dir_site2)

if __name__ == "__main__":
    main()