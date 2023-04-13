# sinusoidal run rhythm

## Description
If one adds up in-phase cosine functions in integer ratios – which are pure intervals in the audible range – these also entail special characteristics in the form of rhythms: they are temporally shifted in their maxima compared to corresponding notated, discrete rhythms, and are thereby something fundamentally different from polyrhythms in the same ratio a:b. In addition, the rhythms have volume weightings between their maxima.

The number of these completely reduced ratios of two partial frequencies up to a specified maximum frequency corresponds to the number of Farey fractions which can be calculated by evaluating the Euler phi function. Combinations are counted, which are called „prime ratios“ here. Musically speaking, these are pure intervals whose octave transpositions are not taken into account. With three partial frequencies, the number of prime ratios corresponds to the so-called „coprime triples.“ 

It is possible to create svg- and wav-files with this script.

## How to

### Requirements

This script requires Python 3, as well as several additional Python-packages. In detail these are:

- numpy
- matplotlib
- scipy

### Usage

Use the following arguments to run `ssr-plot.py`:

**General**

- `--num-partials <num>`: Sets the number of partials to be calculated from, default (and minimum) is 2.
- `--start-partial <num>`: Sets the minimum partial to calculate from.
- `--partials <list>`: Calculate only for a specific combination of partials. Comma-separated, no spaces (e.g. `--partials 3,5,7,11` )
- `--farey-order <num>`: farey-order to use, Default is 8. Careful, high numbers means way more processing, preferably keep below 20.
- `--resolution <num>`: sets the resolution for plots. Default is 441. *Use only uneven numbers*.

**Output Type**

- `--svgs`: Flag to plot svgs with a linear curve and polar display. Default is 2 partials and and all coprime integers up to 8 (below called farey-order)
  - `--curve-svgs`: plot only linear curve svgs
  - `--polar-svgs`: plot only polar svgs
- `--soundfiles`: Flag to create soundfiles using the set Partials to create a rhythmic pattern as envelope for white noise. Always using a samplerate/resolution of 44.1kHz.
- `--soundfiles-num-loops <num>`: Loop the soundfile/cycle for <num> times. Default is 1.

**Examples**

To plot svgs for the partial-set 3,5,7,11, run
`$ python3 ssr-plot.py --svgs --partials 3,5,7,11 `

To plot only polar svgs for partials up to 8, run
 `$ python3 ssr-plot.py --polar-svgs --num-partials 8`

To render svgs and soundfiles for the the partial-set *2,7,13*, run
`$ python3 ssr-plot.py --svgs --soundfiles --num-partials 2,7,13`

To render svgs with a higher resolution, i.e. 44101, run
`$ python3 ssr-plot.py --svgs --resolution 44101`

**Known limitations**

You can render svg plots and soundfiles simultaneously, as long as the resolution stays at the default value. If you want to plot svgs with a non-default resolution and export soundfiles, use two seperate processes for that.

## More

Make sure to visit https://steffenkrebber.de/research/sinusoidal-run-rhythm/ for further information on this project and visual examples.

Enjoy!
