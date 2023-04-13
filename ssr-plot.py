import os
import math
import sys
from itertools import combinations
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import argrelextrema
from farey_sequence import farey
import wave


def make_arrays(res, partials):
    x = np.linspace(0, 2 * np.pi, res)
    xDisp = (x - np.min(x)) / (np.max(x) - np.min(x)) * res
    y = np.cos(partials[0] * x)
    for partial in partials[1:]:
        y += np.cos(partial * x)
    y = y / len(partials) + 1

    # Peak Arrays
    peaksXloc = np.array([])
    peaksX = np.array([])
    peaksY = np.array([])
    yRect = np.full(res, 0.0)
    return x, y, peaksX, peaksY, peaksXloc, yRect, xDisp


# Get Minima and Maxima of Y-Values and the according X-Values
def minAndMax(peaksXloc, peaksX, peaksY, x, y):
    peaksMax = argrelextrema(y, np.greater)
    peaksMin = argrelextrema(y, np.less)
    peaksXloc = np.sort(np.hstack((peaksMin, peaksMax)))
    for peak in peaksXloc[0]:
        if peak in peaksMax[0]:
            peaksY = np.append(peaksY, y[peak])
        elif peak in peaksMin[0]:
            peaksY = np.append(peaksY, 0)

    return peaksX, peaksY, peaksXloc, peaksMin


def parseX(yRect, peaksY, peaksXloc, x, y):
    hold = y[0]
    index = 0

    for counter, _ in enumerate(yRect):
        if counter in peaksXloc:
            hold = peaksY[index]
            np.put(yRect, counter, peaksY[index])
            index += 1
        else:
            np.put(yRect, counter, hold)
    return yRect, peaksY


def cart2pol(x, y):
    rho = np.sqrt(x ** 2 + y ** 2)
    phi = np.arctan2(y, x)
    return phi

# Curve Display
def plot_curve(yRect, xDisp, y, partials, show_or_save="show"):
    fig, ax = plt.subplots()

    # hide axis
    plt.axis("off")
    # rect shape
    plt.plot(yRect)
    # curve shape
    ax.plot(xDisp, y)

    if show_or_save == "show":
        plt.show()
    elif show_or_save == "save":
        plt.savefig(os.path.join("svgs", _filename(partials, "plot_", "svg")))
        plt.close()

# Polar Display
def plot_polar(yRect, peaksY, x, y, partials, show_or_save="show"):
    # Get length of yRect
    yRectLength = len(yRect) - 1
    # End (!) polar plot with y=0
    np.put(yRect, yRectLength, 2)

    ax = plt.subplot(projection="polar")
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(1)

    # hide axis
    plt.axis("off")
    # rect shape
    plt.polar(x, yRect)
    # curve shape
    plt.polar(x, y)

    if show_or_save == "show":
        plt.show()
    elif show_or_save == "save":
        plt.savefig(os.path.join("svgs", _filename(partials, "plotPolar_", "svg")))
        plt.close()


def _filename(partials, identifier, extension, prefix=True):
    partials = "_".join(str(partial) for partial in partials)
    return f"{identifier if prefix else ''}{partials}{identifier if not prefix else ''}.{extension}"


def recipe(args, res, partials):
    x, y, peaksX, peaksY, peaksXloc, yRect, xDisp = make_arrays(res, partials)
    peaksX, peaksY, peaksXloc, peaksMin = minAndMax(peaksXloc, peaksX, peaksY, x, y)
    yRect, peaksY = parseX(yRect, peaksY, peaksXloc, x, y)
    if args.curve_svgs:
        plot_curve(yRect, xDisp, y, partials, show_or_save="save")
    if args.polar_svgs:
        plot_polar(yRect, peaksY, x, y, partials, show_or_save="save")
    if args.soundfiles:
        write_soundfile(
            yRect,
            partials,
            num_samples=44100,
            num_loops=args.soundfiles_num_loops,
            verbose=args.verbose,
        )


def write_soundfile(waveform, partials, num_samples=44100, num_loops=1, verbose=False):
    from scipy.io.wavfile import write

    mean = 0
    std = 1
    white_noise = np.random.normal(mean, std, size=num_samples)
    stretch = num_samples // len(waveform)
    if verbose:
        print(stretch)
    waveform = waveform.repeat(stretch)
    len_waveform = len(waveform)
    if len_waveform != num_samples:
        diff = len_waveform - num_samples
        sys.stderr.write("Warning: filling the remaining {diff} samples with zeros")
        waveform = np.append(waveform, [0] * diff)
    envelopped_noise = white_noise * waveform
    envelopped_noise_quiet = envelopped_noise * 0.3
    waveform_integers = np.int16(envelopped_noise_quiet * 32767)
    if num_loops > 1:
        waveform_integers = np.resize(waveform_integers, num_samples * num_loops)
    write(
        os.path.join("wavs", _filename(partials, "sound_", "wav")),
        num_samples,
        waveform_integers,
    )


def gather_args():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("--svgs", action="store_true", help="create all svgs")
    parser.add_argument(
        "--polar-svgs", action="store_true", help="create only polar svgs"
    )
    parser.add_argument(
        "--curve-svgs", action="store_true", help="create only curve svgs"
    )
    parser.add_argument(
        "--partials",
        help="use only these partials, hint: comma-separated, no spaces (e.g. --partials 3,5,7,11)",
    )
    parser.add_argument(
        "--start-partial",
        default=1,
        type=int,
        help="use only this and higher partials, hint: must be at least <num-partials> below <farey-order>",
    )
    parser.add_argument(
        "--num-partials",
        default=2,
        type=int,
        help="the number of partials to use, default is 2",
    )
    parser.add_argument("--soundfiles", action="store_true", help="create soundfiles")
    parser.add_argument(
        "--print-number-of-combinations",
        action="store_true",
        help="print the number of combinations and exit",
    )
    parser.add_argument(
        "--soundfiles-num-loops",
        type=int,
        default=1,
        help="loop the soundfiles <num> times, default=1",
    )
    parser.add_argument(
        "--farey-order",
        type=int,
        default=8,
        help="the farey order to use, NB: higher number will create a vast number of files, keep below 20",
    )
    parser.add_argument(
        "--resolution",
        type=int,
        default=441,
        help="the resolution (length) of the charts, also used for soundfile-creation",
    )
    args = parser.parse_args()
    if args.verbose:
        sys.stderr.write(f"{args}\n")
    return args


if __name__ == "__main__":
    args = gather_args()
    if args.svgs:
        args.curve_svgs, args.polar_svgs = True, True
    if args.verbose:
        sys.stderr.write("f{args}\n")
    res = args.resolution
    if args.partials:
        partials_list = [list(int(partial) for partial in args.partials.split(","))]
    else:
        farey_order = args.farey_order
        ordered_ratios = farey(farey_order)
        # 2 partials
        two_partials = [(ratio.x, ratio.y) for ratio in ordered_ratios]
        if args.num_partials <= 2:
            partials_list = two_partials
        else:
            partials_list = []
            for combined_tuple in combinations(range(1, args.farey_order), args.num_partials - 2):
                for partials in two_partials:
                    candidate_partials = sorted(partials + combined_tuple)
                    if len(candidate_partials) == len(set(candidate_partials)) and candidate_partials not in partials_list:
                        if args.start_partial:
                            if not args.start_partial or all([n >= args.start_partial for n in candidate_partials]):
                                partials_list.append(candidate_partials)
                        else:
                            partials_list.append(candidate_partials)

    if args.print_number_of_combinations:
        print(f"{len(partials_list)} of combinations for the current parameters")
        sys.exit(0)
    for partials in partials_list:
        recipe(args, res, partials)
