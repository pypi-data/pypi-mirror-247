import re

from telegraph.aio import Telegraph

telegraph = Telegraph('ccd85ea0b1314d9dd43284b9fabd47954bd467ff4a6c5800889b807fbe9c')


## Telegraph thingy
async def convert_to_telegraph():
    """Convert some medias found into telegraph"""



async def search_in_telegraph():
    """Search content, created by my token"""
    my_pages = await telegraph.get_page_list()
    
    posts = []
    for post in my_pages['pages']:
        if re.findall("Coba", post["description"] + post["title"]):
            posts.append(post)


async def create_new_pages(title):
    """Create new telegraph post"""
    
    response = await telegraph.create_page(
        title,
        html_content='<p>Test 123456, Coba coba</p>',
    )
    print(response['url'])
