from datetime import datetime
from urllib.parse import urlencode
from aiogram.fsm.context import FSMContext
from typing import Union, Tuple
import aiohttp


async def find_city_info(city_country_str: str) -> Union[Tuple[str, float, float], str]:
    user_agent = "unique_user_agent"+str(datetime.now())
    params = urlencode({'q': city_country_str, 'format': 'json'})
    url = f'https://nominatim.openstreetmap.org/search?{params}'

    async with aiohttp.ClientSession() as session:
        headers = {'User-Agent': user_agent}
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                if data:
                    location = data[0]
                    return location['display_name'], location['lat'], location['lon']
                else:
                    return "Город не найден."
            else:
                return "Ошибка запроса."


async def get_location(state: FSMContext):
    return (await state.get_data()).get("location")
