import swisseph as swe
from datetime import datetime
from timezonefinder import TimezoneFinder
import pytz

def convert_to_utc(local_datetime: datetime, lat: float, lon: float) -> datetime:
    """ Converts local time to UTC """
    local = pytz.timezone(TimezoneFinder().timezone_at(lat=lat, lng=lon))
    local_dt = local.localize(local_datetime, is_dst=None)
    return local_dt.astimezone(pytz.utc)

def calculate_positions(jdn: float, location: dict, flags: int) -> dict:
    """ Calculates astrological positions """
    ayanamsa = swe.get_ayanamsa(jdn)
    sun_long = swe.calc_ut(jdn, swe.SUN, flags=flags)[0][0] - ayanamsa
    moon_long = swe.calc_ut(jdn, swe.MOON, flags=flags)[0][0] - ayanamsa
    ascendant_long = swe.houses(jdn, location['lat'], location['lon'], b'A')[0][0] - ayanamsa

    return {
        "sun_sign": get_zodiac_sign(sun_long),
        "moon_sign": get_zodiac_sign(moon_long),
        "ascendant": get_zodiac_sign(ascendant_long)
    }

async def astro_calc(location: dict, full_datetime: datetime) -> dict:
    full_datetime_utc = convert_to_utc(full_datetime, location['lat'], location['lon'])

    jdn = swe.julday(full_datetime_utc.year, full_datetime_utc.month, full_datetime_utc.day,
                     full_datetime_utc.hour + full_datetime_utc.minute / 60 + full_datetime_utc.second / 3600)
    swe.set_topo(location['lon'], location['lat'], 0)

    return calculate_positions(
        jdn, 
        location, 
        swe.FLG_SWIEPH | swe.FLG_TOPOCTR | swe.FLG_SPEED
    )

def get_zodiac_sign(longitude: float) -> str:
    zodiac = ['Овен', 'Телец', 'Близнецы', 'Рак', 'Лев', 'Дева', 'Весы', 'Скорпион', 'Стрелец', 'Козерог', 'Водолей', 'Рыбы']
    index = int(longitude / 30) % 12
    return zodiac[index]

# Пример использования
# location = {'lat': 47.9102734, 'lon': 33.3917703}
# full_datetime = datetime(1987, 1, 25, 23, 35)
# astro_data = asyncio.run(astro_calc(location, full_datetime))
# print(astro_data)
