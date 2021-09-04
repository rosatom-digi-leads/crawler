import asyncio
import csv
import sys
from random import randint

import aiohttp
from bs4 import BeautifulSoup


async def get_html(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                return await resp.text()
    return ''


def dump_to_csv(filename, data):
    with open(filename, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for row in data:
            writer.writerow(row)


async def main():
    html = await get_html(sys.argv[1])
    soup = BeautifulSoup(html, 'html.parser')

    result = []

    data_table = soup.find(id='tab1')
    if data_table is None:
        return

    for table in data_table.find_all(class_='property-table')[:-2]:
        for tr in table.find_all('tr'):
            for label, body in [tr.find_all('td')]:
                label_text = label.contents[0]
                body_data = body.find_all('a')
                if body_data:
                    body_data = [a.contents[0] for a in body_data if a.contents]
                    clear_body_data = [a.replace('\n', '').replace(' ', '') for a in body_data]
                    body_text = ', '.join(clear_body_data)
                else:
                    body_text = body.contents[0] if body.contents else ''
                result.append((label_text, body_text))

    result.append(('Тщательность', randint(1, 3)))

    filename = next(filter(lambda x: x[0] == 'Номер закупки', result))[1]
    filename = filename.replace('/', '_') + '.csv'
    dump_to_csv(filename, result)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
