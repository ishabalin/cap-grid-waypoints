# cap-grid-waypoints

CAP grid waypoint generator.

The command `cap-grid-waypoints` will produce for each grid a KML file
that contains waypoints for each quarter grid corner coordinates.
That's 16 waypoints for each grid. The waypoint names are encoded
in the following format: "{GRID}{QUARTER}{CORNER}". For example,
"SFO1CNW" is the north-west corner of SFO1C quarter.

```
usage: cap-grid-waypoints [-h] [-o OUTPUT_DIR] N [N ...]

Generate CAP grid waypoints

positional arguments:
  N                     grid names or ranges, e.g. SFO1 or SFO1,5 or SFO1-16 or SFO1-3,10-12

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        output directory
```
