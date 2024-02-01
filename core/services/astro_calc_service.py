import swisseph as swe
from datetime import datetime

async def astro_calc(location: dict, full_datetime: datetime) -> dict:
    swe.set_ephe_path('assets/ephe')

    # Convert datetime to Julian Day Number (JDN)
    jdn = swe.julday(full_datetime.year, full_datetime.month, full_datetime.day,
                     full_datetime.hour + full_datetime.minute / 60 + full_datetime.second / 3600)

    # Setting flags for calculation
    flags = swe.FLG_SWIEPH | swe.FLG_TOPOCTR | swe.FLG_SPEED

    # Set geoposition for topocentric calculations
    swe.set_topo(location['lon'], location['lat'], 0)

    # Get the ayanamsa value for given Julian Day
    ayanamsa = swe.get_ayanamsa(jdn)

    # Calculating the position of the Sun and correcting for ayanamsa
    sun_long = swe.calc_ut(jdn, swe.SUN, flags=flags)[0][0] - ayanamsa
    sun_sign = get_zodiac_sign(sun_long)

    # Calculating the position of the Moon and correcting for ayanamsa
    moon_long = swe.calc_ut(jdn, swe.MOON, flags=flags)[0][0] - ayanamsa
    moon_sign = get_zodiac_sign(moon_long)

    # Ascendant calculation and correcting for ayanamsa
    ascendant_long = swe.houses(jdn, location['lat'], location['lon'], b'A')[0][0] - ayanamsa
    ascendant_sign = get_zodiac_sign(ascendant_long)

    return {
        "sun_sign": sun_sign,
        "moon_sign": moon_sign,
        "ascendant": ascendant_sign
    }

def get_zodiac_sign(longitude: float) -> str:
    # zodiac = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
    zodiac = ['Овен', 'Телец', 'Близнецы', 'Рак', 'Лев', 'Дева', 'Весы', 'Скорпион', 'Стрелец', 'Козерог', 'Водолей', 'Рыбы']
    index = int(longitude / 30) % 12
    return zodiac[index]

# location = {'lat': 40.7128, 'lon': -74.0060}
# full_datetime = datetime(2021, 1, 1, 12, 0)
# astro_data = astro_calc(location, full_datetime)
# print(astro_data)
