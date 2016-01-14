# PRISM_pyPol
Polarimetric reduction of astronomical \*.fits images.

# Dependencies and Setup

pyPol requires installation of the "AstroImage" class. This can be downloaded
from the jmontgom10 GitHub repository and has its own set of dependencies, which
the user should take care to install properly (see the AstroImage README File a
guide on install those packages).

I recommend using the Anaconda environment, as that comes with numpy, scipy,
astropy, and matplotlib preinstalled. If you elect not to use Anaconda, then
make sure to get those packages properly installed before proceeding to install
the AstroImage dependencies.

This package is written for Python 3 and is not compatible with Python 2.

# Procedure

The pyPol package consists of a set of scripts, each of which perform one of the
basic steps in the reduction of polarimetry CCD data. The script names are all
prepended by a number, and the scripts should be executed in the order of their
numbers, as in

```
$ python 01_buildIndex.py
```

*Nota Bene* The user must always take care to update the directory structure
information at the top of each script. Technically, the user can elect to use
whatever directory structure they like, but I recommend using a similar
directory structure to the one shown in the default values. These help keep the
intermittent data cleanly separated into logical directories.

## 01_buildIndex.py

The first step in this reduction procedure is to simply look at all the files in
the "reducedDir" directory and categorize them according to their content.
Waveband and polaroid filter rotation angle can be pulled straight out of the
image header, but some information must be provided by the user. The two
essential user-provided pieces of information are the group "target" and the
group "dither pattern."

*Use a single name to refer to each individual target*. The purpose of the
"target" information is to provided the scripts with an easy way to tell what
images should be treated as repeated measurements of the same object. For
example, the scripts cannot parse that the group names "NGC 7023_R1",
"ngc7023R2", and "NGC_7023V_1" all refer to the same target. Thus, the user
should enter an identical string (e.g. "NGC7023") for each of these groups.
Fortunately, the scripts **are** able to parse the waveband of each image, so
you should not use different target names for different wavelengths. For
example, do **not** use "NGC7023_R" to refer to R-band observations of NGC7023
and "NGC7023_V" to refer to V-band observations of NGC7023, use "NGC7023" to
refer to both, and the scripts will figure out which observations are R-band vs.
V-band. Of course, if you make a mistake, the file index will be saved as a .csv
file, so you can easily edit the file using your favorite .csv editor (excel,
open office, etc...).

The indexing script also adds a "Use" flag column to the index. Files with a 1
in this column will be used in the final polarimetry analysis while files with a
0 in this column will be omitted from later processing steps.

## 02_doAstrometry.py

This step can be optional depending on how you want to align your images in step
05_avgPolAngImages and beyond. If you are planning on using astrometry, then
you'll need to install Astrometry.net on your system. If you are using Linux,
then the Astrometry.net website is probably enough to get going. If you need a
bit more help, or if you're installing Astrometry.net on Windows, then I
recommend you check out the [setup
guide](https://sites.google.com/site/jmastronomy/Software/astrometry-net-setup)
I wrote expressly for that purpose.

Once you've successfully installed Astrometry.net, this step is quite
straightforward. Simply update the paths at the beginning of the script, and
execute it with Python. This should loop through all the files in your
reducedDir location and solve their astrometry (updating file headers along the
way).

## 03_repairAstrometry.py

Of course, it would be wonderful if all the files had perfect astrometry right
out of the gate, but that's not always the case. To check the self-consistency
of the solved astrometry, this script produces a histogram of the plate-scale
values for each science target and each waveband (e.g. NGC7023, R-band). Any
outliers in the histogram are identified and their astrometry information is
replaced with a substitute set of values from the other images in that group.

To execute this script, simply update the paths at the top of the file, and run it through the Python interpreter.

## 04_buildMasks.py

## 05_avgPolAngImages.py

## 06_finalPolarimetry.py

## 07_photometricCalibration
