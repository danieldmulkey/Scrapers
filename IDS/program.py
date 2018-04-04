import csv

import requests
import bs4


def main(debug=False):
    print_the_header()

    urls = get_camera_urls()

    all_cameras = []
    print('Getting camera specs...')
    for ind, url in enumerate(urls):
        print(f'Getting specs for camera {ind+1} of {len(urls)}')
        camera = get_camera_from_url(url)
        all_cameras.append(camera)
        if debug and ind >= 5:
            break

    header = camera.keys()
    print(f'Header is {header}')
    print(f'First camera is {all_cameras[0]}')

    write_to_csv(header, all_cameras)


def print_the_header():
    print('------------------------------------')
    print('     IDS IMAGING WEB SCRAPER')
    print('------------------------------------')
    print()


def get_camera_urls():
    print('Getting camera URLs...')
    base_url = 'https://en.ids-imaging.com/store/products/cameras/show/all.html'
    response = requests.get(base_url)
    soup = bs4.BeautifulSoup(response.text, 'lxml')
    camera_urls = [c.find('a')['href'] for c in soup.findAll(class_='product-name')]
    return camera_urls


def get_camera_from_url(url):
    html = requests.get(url)
    soup = bs4.BeautifulSoup(html.text, 'lxml')
    table = soup.find(class_='data-table', id='product-attribute-specs-table')
    labels = [l.get_text() for l in table.findAll(class_='label')]
    data = [d.get_text().strip() for d in table.findAll(class_='data')]
    camera = {l: d for l, d in zip(labels, data)}
    return camera


def write_to_csv(header, cameras):
    try:
        with open('IDS_cameras.csv', mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)

            print('Saving cameras to CSV...')
            for c in cameras:
                writer.writerow([c[k] for k in header])
            print('Done!')
    except PermissionError as e:
        print(f'Error occurred, is .CSV still open? {e.message}')


if __name__ == '__main__':
    main(debug=False)
