# DATA_PROVENANCE.md

This document records where the content of this repository comes from, what is
user-authored, and what is deliberately not redistributed.

## Source archives

| Archive            | Role                        | Snapshot (commit)                       |
| ------------------ | --------------------------- | --------------------------------------- |
| `planet_chem`      | Coursework source archive   | `9a2ebd1049e3e5e8d21ed6f9dea71abce7a67ffe` |
| `geoanalytical-lab`| Analytical-lab source archive | `3d33d2614d2c7ba9e6b698704e8f67976b17e1e5` |

Both source repositories are private. The publication layer in this repository
was assembled from these snapshots (via `git archive`); no source history was
imported, and neither source repository is modified by this repository.

## User-authored material

The following categories in this repository are user-authored coursework
artifacts (Xinyu Du, Nanjing University, 2026):

- coursework reports (module `README.md` files);
- Jupyter notebooks (outputs cleared, execution counts reset);
- Python scripts;
- Gaussian input files (`.gjf`);
- generated figures (matplotlib/plotted outputs, microscope display images);
- explicitly derived public data, e.g.
  `isotope_geochemistry/sulfur_fractionation/data/frequencies.csv`
  (derived from the actual course Gaussian calculations) and
  `data/results.csv`.

## Not redistributed

- course lecture PDFs and handouts (`00_讲义/` etc.);
- assignment documents and original question files;
- publisher full-text articles and third-party literature conversions;
- proprietary instrument files (`.l6s`, `.000`, raw instrument exports);
- complete class datasets and teacher-provided raw workbooks;
- other students' files and identifiers;
- raw analytical archives (raw TIFFs, course-provided spreadsheets);
- original submission PDFs.

These materials remain in the private source archives.

## Gaussian

- Gaussian 16 is proprietary software and is not distributed.
- The `.gjf` input files are included (`isotope_geochemistry/sulfur_fractionation/gaussian_inputs/`).
- The public frequency dataset `data/frequencies.csv` is derived from the
  actual course Gaussian 16 calculations (six Opt+Freq runs: H2S, SO2,
  SO4^2- × {32S, 34S}), whose output logs contain `Normal termination` and
  are retained in the private course archive. Provenance anchors (SHA-256 of
  the log files):

  - `H2S_opt_freq.log`:        `71b139a56b84e1d8a844439ed42456c332e308510e2bf7cca5af7e0d9e5774e6`
  - `H2S_34S_opt_freq.log`:    `ae7f2c2036a697bc6f2db30dd160298e41d5f0de656ba7dbfc83bf24286e1704`
  - `SO2_opt_freq.log`:        `eebf4473063ad98d3f63395b23f0d88c6ca34df275d5c03ba44d87dd94e994ed`
  - `SO2_34S_opt_freq.log`:    `c0b5e7ac50365bafc389e57266dbfee6a95b47fb7f882430f2b62e4291705b9a`
  - `SO4_2-_opt_freq.log`:     `28bd903bc5dd149bbe1ce92d27139b6b1b3fd3770c343836041f99fb46be9e88`
  - `SO4_2-_34S_opt_freq.log`: `0f1683b0cfeac70bce74435e899b7fe133abe311afd9e0d89640ada0e1a7f8e2`

- Raw Gaussian program binaries and `.log`/`.chk`/`.fchk` files are not
  included.

## IAC ExoAtmospheres

- The exoplanet-atmosphere statistics coursework
  (`planetary_chemistry/exoplanet_teq_statistics/`) uses the **IAC
  ExoAtmospheres** database (external public database).
- The source snapshot was downloaded in June 2026.
- Source: IAC ExoAtmospheres database, Instituto de Astrofísica de Canarias,
  accessed June 2026.
- The external raw CSV remains in the private source archive and is **not
  redistributed** in this repository.
- The report, script, and figures are user-authored coursework artifacts;
  the script fails loudly if the external dataset is not supplied.

## Analytical labs

- Raw and course-provided analytical archives remain private
  (`geoanalytical-lab`).
- Public modules contain selected reports and display artifacts only.
- Analytical modules are not all fully reproducible from raw data.
- Instrument output formats (`.l6s`, `.000`, `.xlsm`, raw TIFF) are not
  redistributed.

## GC-MS

- Course-provided example chromatograms were used for biomarker
  interpretation; raw GC-MS data are not redistributed.
- The extraction/fractionation workflow itself was performed as part of the
  laboratory course.

## License boundary

- The MIT License (see `LICENSE`) applies only to user-authored source code
  and computational input files unless a file explicitly states otherwise; it
  does not apply to coursework reports, user-generated scientific figures,
  datasets, or third-party/course-provided material.
- Reports and user-generated figures remain copyright Xinyu Du unless
  otherwise noted.
- Course-provided datasets and third-party materials retain their original
  provenance and are not relicensed under MIT.
