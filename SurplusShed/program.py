import csv

import requests
import bs4
import collections

LensEntry = collections.namedtuple('LensEntry',
                                   'prod_id, shape, OD, EFL, coating, price')


def main():
    print_the_header()

    available_shapes = ['ACH', 'ASP', 'DCX', 'PCX', 'DCV', 'PCV', 'TRP', 'NMN', 'PMN', 'BCX', 'BVC']
    all_lenses = []
    for shape in available_shapes:
        print(f'Getting all {shape} lenses...')
        html = get_html_from_web(shape)

        header, lenses = get_lenses_from_html(html)
        all_lenses.append(lenses)

    all_lenses = [le for le_list in all_lenses for le in le_list]
    print(f'Header is {header}')
    print(f'first lens is {all_lenses[0]}')

    write_to_csv(header, all_lenses)


def print_the_header():
    print('------------------------------------')
    print('     SURPLUS SHED WEB SCRAPER')
    print('------------------------------------')
    print()


def get_html_from_web(shape):
    url = f'https://www.surplusshed.com/search_lenses.php?type={shape.upper()}' \
          f'&diameter_to=&diameter_from=&focal_length_to=&focal_length_from=&sort=&sortby=+asc'
    response = requests.get(url)
    # print(response.status_code)
    return response.text


def get_lenses_from_html(html):
    # Structure to variables from CSS:
    # cityCss = 'div#location h1'
    # weatherConditionCss = 'div#curCond span.wx-value'
    # weatherTempCss = 'div#curTemp span.wx-data span.wx-value'
    # weatherScaleCss = 'div#curTemp span.wx-data span.wx-unit'

    soup = bs4.BeautifulSoup(html, 'lxml')
    table = soup.find(class_='table-responsive')

    header = [h.get_text().strip() for h in table.find('thead').findAll('th')][:-2]  # remove link buttons

    lens_entries = table.find('tbody').findAll('tr')
    lenses = []
    for le in lens_entries:
        entry_text = [e.get_text().strip() for e in le.findAll('td')][:-2]  # remove link buttons
        prod_id, shape, OD, EFL, coating, price = entry_text
        try:
            OD = float(OD.split(' ')[0])
            EFL = float(EFL.split(' ')[0])
        except ValueError:
            pass
        lens = LensEntry(prod_id=prod_id, shape=shape, OD=OD, EFL=EFL, coating=coating, price=price)
        lenses.append(lens)

    return header, lenses


def cleanup_text(text: str):  # : type ONLY to help intellisense
    if not text:
        return text

    text = text.strip()
    return text


def write_to_csv(header, lenses):
    try:
        with open('ss_lenses.csv', mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)

            print('Saving lenses to CSV...')
            for l in lenses:
                writer.writerow([l.prod_id, l.shape, l.OD, l.EFL, l.coating, l.price])
            print('Done!')
    except PermissionError as e:
        print(f'Error occurred, is .CSV still open? {e.message}')


if __name__ == '__main__':
    main()
