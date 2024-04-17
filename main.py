import os
import httpx

def API_request(keyword, per_page, num_pages):
    all_results = []
    for page in range(1, num_pages + 1):
        link = f"https://unsplash.com/napi/search/photos?page={page}&per_page={per_page}&query={keyword}"
        resp = httpx.get(link)
        if resp.status_code == 200:
            page_results = resp.json().get('results', [])
            all_results.extend(page_results)
        else:
            print(f"Error fetching page {page}: Status code {resp.status_code}")
            break  # Exit the loop if there's an error
    return all_results

def extract_raw_urls(response_json, skip_premium=True):
    urls = []
    for image_data in response_json:
        if skip_premium and image_data.get('premium', False):
            continue
        raw_url = image_data['urls']['raw']
        trimmed_url = raw_url.split('?')[0]
        urls.append((image_data['id'], trimmed_url))
    return urls

def download_images(keyword, urls):
    directory = f"C:/Users/Scott/Pictures/bmw/{keyword}"
    if not os.path.exists(directory):
        os.makedirs(directory)

    print(f"Starting download of {len(urls)} images for {keyword}...")
    for idx, (image_id, url) in enumerate(urls, start=1):
        image_response = httpx.get(url)
        if image_response.status_code == 200:
            image_path = os.path.join(directory, f"{image_id}.jpg")
            with open(image_path, 'wb') as image_file:
                image_file.write(image_response.content)
            print(f"{idx}. Downloaded {image_id} to {image_path}")
        else:
            print(f"{idx}. Failed to download image {image_id}")

# Example usage
if __name__ == "__main__":
    for i in [ "bmw m3", "bmw m5"]:
        keyword = i
        num_pages = 1  # Number of pages you want to fetch
        per_page = 10  # Number of images per page
        all_results = API_request(keyword, per_page, num_pages)
        if all_results:  # Ensure we have results
            urls = extract_raw_urls(all_results)  # Extract URLs, skipping premium images
            if urls:
                print(f"Total images to be downloaded (excluding premium ones): {len(urls)}")
                download_images(keyword, urls)
            else:
                print("No non-premium images found for download.")
        else:
            print("No results found or there was an error.")
