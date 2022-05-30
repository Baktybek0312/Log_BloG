import requests

URL = "http://127.0.0.1:8000/posts/list"


def get_data():
    data = requests.get(url=URL)

    with open('get_data_blog_posts.xls', 'wb') as file:
        file.write(data.content)
    return data


print(get_data())

