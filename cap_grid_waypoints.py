import argparse
import xml.etree.ElementTree as ET

from pathlib import Path


KML_TEMPLATE = """\
<?xml version="1.0" encoding="UTF-8"?>
<kml
  xmlns="http://www.opengis.net/kml/2.2"
  xmlns:gx="http://www.google.com/kml/ext/2.2"
  xmlns:kml="http://www.opengis.net/kml/2.2"
  xmlns:atom="http://www.w3.org/2005/Atom">
%s
</kml>
"""


# grid dimensions
GRIDS = {
    'LMT': {
        'cols': 32,
        'rows': 18,
        'lat': 44.5,
        'lon': 125.0,
    },
    'SEA': {
        'cols': 32,
        'rows': 18,
        'lat': 49.0,
        'lon': 125.0,
    },
    'SFO': {
        'cols': 28,
        'rows': 16,
        'lat': 40.0,
        'lon': 125.0,
    },
    'LAS': {
        'cols': 28,
        'rows': 17,
        'lat': 40.0,
        'lon': 118.0,
        'skip': range(449, 461),
    },
    'LAX': {
        'cols': 26,
        'rows': 16,
        'lat': 36.0,
        'lon': 121.5,
    },
}


# lat/lon offset multipliers for quarter-grids
QUARTERS = (
    ('A', 0, 0),
    ('B', 0, 1),
    ('C', 1, 0),
    ('D', 1, 1),
)

# lat/lon offset multipliers for quarter-grid corners
CORNERS = (
    ('NW', 0, 0),
    ('NE', 0, 1),
    ('SW', 1, 0),
    ('SE', 1, 1),
)

# whole grid size
GSIZE = 0.25

# quarter-grid size
QSIZE = 0.125


def write_grid_kml(name, number, path):
    """
    Given a grid `name` and `number` write a KML file named
    "{name}{number}.kml" under the directory specified by `path`.

    """
    conf = GRIDS[name]
    rows = conf['rows']
    cols = conf['cols']

    if not (0 < number <= rows * cols):
        raise ValueError(f'Invalid grid number: {name}{number}')

    row = (number - 1) // cols
    col = (number - 1) % cols

    base_lat = conf['lat'] - row * GSIZE
    base_lon = conf['lon'] - col * GSIZE

    sub = ET.SubElement
    d = ET.Element('Document')
    f = sub(d, 'Folder')
    sub(f, 'name').text = f'{name}{number}'

    for quarter, lat1k, lon1k in QUARTERS:
        for corner, lat2k, lon2k in CORNERS:
            lat = base_lat - QSIZE * (lat1k + lat2k)
            lon = base_lon - QSIZE * (lon1k + lon2k)

            p = sub(f, 'Placemark')
            sub(p, 'name').text = f'{name}{number}{quarter}{corner}'
            sub(p, 'description')
            pp = sub(p, 'Point')
            sub(pp, 'altitudeMode').text = 'absolute'
            sub(pp, 'coordinates').text = f'-{lon},{lat}'

    # Python 3.9+
    if hasattr(ET, 'indent'):
        ET.indent(d, space='  ')

    with path.joinpath(f'{name}{number}.kml').open('w') as f:
        print(KML_TEMPLATE % ET.tostring(d, encoding='unicode'), file=f)


def parse_grid_spec(grid):
    """
    Parse grid range specification and return an iterator over
    (name, numbers) tuples.

    """
    name = grid[:3]
    if len(name) < 3 or not name.isalpha():
        raise ValueError(f'Invalid grid spec: {grid}')
    if len(grid) == 3:
        # entire grid
        rows = GRIDS[name]['rows']
        cols = GRIDS[name]['cols']
        yield name, range(1, rows * cols + 1)
        return
    for range_spec in grid[3:].split(','):
        try:
            parts = range_spec.split('-', 1)
            if len(parts) > 1:
                range_min, range_max = map(int, parts)
            else:
                range_min = range_max = int(range_spec)
        except ValueError:
            raise ValueError(f'Invalid grid spec: {grid}')
        yield name, range(range_min, range_max + 1)


parser = argparse.ArgumentParser(
    description='Generate CAP grid waypoints')
parser.add_argument(
    'grids', metavar='N', nargs='+',
    help=(
        'grid names or ranges, e.g. SFO1 or SFO1,5 '
        'or SFO1-16 or SFO1-3,10-12'))
parser.add_argument(
    '-o', '--output-dir',
    help='output directory')


def main():
    args = parser.parse_args()
    path = Path(args.output_dir or '.')
    path.mkdir(parents=True, exist_ok=True)

    for grid in args.grids:
        for name, numbers in parse_grid_spec(grid):
            skip = GRIDS[name].get('skip', ())
            for number in numbers:
                if number in skip:
                    continue
                write_grid_kml(name, number, path)


if __name__ == '__main__':
    main()
