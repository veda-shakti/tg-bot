import aiofiles
from os.path import dirname


async def read_text_from_file(name: str, **kwargs) -> str:
    async with aiofiles.open(dirname(__file__) + '/' + name + '.html', mode='r', encoding='utf-8') as file:
        content = await file.read()
    return content.format(**kwargs) if kwargs else content
