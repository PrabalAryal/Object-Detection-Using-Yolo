import requests
import os


# define a function to search for photos on flickr
def search_filter(query, api_key, num_images=100):
    # pass url for flickr api
    url = "https://api.flickr.com/services/rest/"
    # parameters for the api request
    params = {
        "method": "flickr.photos.search",  # api method to search photos
        "api_key": api_key,  # api key for authentication
        "text": query,  # search query
        "tags": "football",  # search result by relevance
        "per_page": num_images,  # number of results for pages
        "format": "json",  # format of the response per page
        "nojsoncallback": 1,  # response in json format
    }
    # send the get request to the api
    response = requests.get(url, params=params)
    # check if the request is successful
    if response.status_code == 200:
        # return the response in json format
        return response.json()["photos"]["photo"]
    else:
        # return an empty list if the request is not successful
        print("failed to fetch image !!!")
        return []


# define a function to construct the url of image
def get_photo_url(photo, size="large"):
    # base url of the photo
    url = f"https://live.staticflickr.com/{photo['server']}/{photo['id']}_{photo['secret']}"
    # append the size suffix to the url based on the specified size
    if size == "big":
        url += "_b.jpg"
    elif size == "small":
        url += "_z.jpg"
    else:
        url += ".jpg"
    return url


# define a function to download the image
def download_image(photos_list, directory):
    # create a directory if it does not exist
    if not os.path.exists(directory):
        os.makedirs(directory)
    # loop through the list of photos
    for i, photo in enumerate(photos_list):
        # get the url of the photo
        img_url = get_photo_url(photo)
        # construct a path to save the images
        img_path = os.path.join(directory, f"image_{i+1}.jpg")

        # download and save the image
        with open(img_path, "wb") as img_file:
            img_file.write((requests.get(img_url)).content)


# define the main function
def main():
    # search query for flickr
    query = "football"
    # api key for flickr
    api_key = "2c091cbda37bd0c4f9e1ddc42bedf1c1"
    # number of images to download
    num_images = 100
    # search for photos on flickr
    photo_list = search_filter(query, api_key, num_images)
    download_image(photo_list, "Football_images")


# run the main function if the script is executed directly
if __name__ == "__main__":
    main()
