# Planetary & Geochemical Coursework

Selected computational and analytical coursework from the Planetary Science program at Nanjing University, covering planetary chemistry, isotope geochemistry, quantum-chemical modelling, mass spectrometry, spectroscopy, microscopy, and organic geochemistry.

This repository is a coursework portfolio, not a collection of peer-reviewed research publications.

Detailed coursework reports are primarily written in Chinese.

## 1. Selected highlights

| Highlight                    | Evidence                                                                   |
| ---------------------------- | -------------------------------------------------------------------------- |
| Sulfur isotope fractionation | Gaussian 16 inputs + Bigeleisen–Mayer/Urey post-processing + Python        |
| Lunar KREEP & REE melting    | partitioning, partial-melting models, lunar magma-ocean interpretation     |
| Sr isotope TIMS              | clean-lab separation, TIMS workflow, interference/mass-bias correction, QC |
| Trace elements by ICP-MS     | sample preparation, internal-standard calibration, HR-ICP-MS               |
| SEM-EDS / Raman / AFM        | mineral microanalysis, spectroscopy, surface characterization              |
| Organic geochemistry         | extraction/fractionation, biomarker interpretation, organic petrography    |

## 2. Coursework map

Planetary chemistry (行星化学):

- **Stellar nucleosynthesis** — nucleosynthesis paths, radioactive decay, SN1987A light-curve modelling.
- **Isotope geochronology** — fundamentals of radiometric dating and decay-system analysis.
- **Chemical kinetics** — kinetic modelling exercises.
- **Thermodynamics & phase equilibria** — Gibbs free energy, phase diagrams, equilibrium calculations.
- **Meteorite geochemistry** — iron-meteorite trace elements (Co, Ga, Au), mixing models, planetary differentiation.
- **Core–mantle differentiation** — DMM Nd concentration, BSE siderophile-element core–mantle models.
- **Exoplanet atmosphere statistics** — IAC ExoAtmospheres dataset; equilibrium-temperature distributions, observational selection effects, and planetary-environment interpretation.
- **Lunar KREEP & REE melting** — REE partitioning, partial-melting models, lunar magma-ocean interpretation (Apollo 15 samples 15386/15555, urKREEP).

Isotope geochemistry (同位素地球化学):

- **Stable isotope fractionation** — equilibrium oxygen/hydrogen/carbon fractionation basics.
- **Water–rock exchange** — W/R ratio modelling (Taylor 1977 approximation).
- **Geochronology** — dating-method review (Rb-Sr, Sm-Nd, U-Pb systems).
- **Sulfur fractionation** — ³⁴S/³²S equilibrium fractionation factors from Gaussian 16 vibrational frequencies (B3LYP/6-31G(d), 6-31+G(d)) via Bigeleisen–Mayer/Urey theory.
- **Common Pb evolution** — Stacey–Kramers two-stage Pb evolution model.

Analytical geochemistry (地球化学分析技术 laboratory course):

- **Sr isotopes by TIMS** — clean-lab Sr separation, Triton TIMS, NIST SRM 987 QC, interference/mass-bias correction.
- **Trace elements by HR-ICP-MS** — Mo calibration, Rh internal standard, carbonate selective dissolution, GSR-13, Element XR.
- **Olivine SEM-EDS** — secondary-electron imaging and semiquantitative EDS analysis.
- **Muscovite Raman** — laser Raman identification (HORIBA LabRAM, HQI library matching).
- **AFM calibration** — Bruker MultiMode 8 PeakForce Tapping on a calibration grid.
- **Organic extraction & GC-MS** — microwave extraction, column fractionation, biomarker interpretation (course-provided example chromatograms).
- **Organic petrography** — transmitted/fluorescence light microscopy of microbial mats, reflected-light vitrinite identification (Nikon ECLIPSE LV100N).

## 3. Computational reproducibility

The sulfur-isotope post-processing workflow (`isotope_geochemistry/sulfur_fractionation/`) is fully scripted:

```bash
python isotope_geochemistry/sulfur_fractionation/scripts/isotope_fractionation.py            # recompute results + figure
python isotope_geochemistry/sulfur_fractionation/scripts/isotope_fractionation.py --check    # regression check vs tracked results
python -m pytest -q                                                                          # full test suite
```

- Vibration frequencies come from the actual course Gaussian 16 calculations (`data/frequencies.csv`); the raw Gaussian outputs remain in the private course archive.
- There is **no silent literature fallback**: if `frequencies.csv` is missing, the script fails loudly.
- Gaussian 16 itself is proprietary and is not distributed.

## 4. Analytical coursework and data policy

The analytical modules are a curated public report layer, not raw-data mirrors:

- Raw/course-provided analytical archives (instrument files, class spreadsheets, other students' data, raw TIFFs) remain in the private course archive and are not redistributed.
- Analytical modules contain selected reports and display artifacts; they are not all fully reproducible from raw data.
- GC-MS biomarker interpretation uses course-provided example chromatograms; raw GC-MS data are not redistributed.
- SEM Fo is presented as an approximate semiquantitative EDS-derived estimate.
- AFM observations are not presented as a full metrological calibration.

See [DATA_PROVENANCE.md](DATA_PROVENANCE.md) for the full provenance statement.

## 5. Repository structure

```text
planetary_chemistry/
├── stellar_nucleosynthesis/
├── isotope_geochronology/
├── chemical_kinetics/
├── thermodynamics_phase_equilibria/
├── meteorite_geochemistry/
├── core_mantle_differentiation/
├── exoplanet_teq_statistics/
└── lunar_ree_melting/

isotope_geochemistry/
├── stable_isotope_fractionation/
├── water_rock_exchange/
├── geochronology/
├── sulfur_fractionation/
└── common_pb_evolution/

analytical_geochemistry/
├── sr_isotope_tims/
├── trace_elements_icp_ms/
├── olivine_sem_eds/
├── muscovite_raman/
├── afm_calibration/
├── organic_extraction_gc_ms/
└── organic_petrography/

tests/
.github/workflows/validate.yml
```

## 6. Provenance

- Source archives: `planet_chem` @ `9a2ebd1049e3e5e8d21ed6f9dea71abce7a67ffe`, `geoanalytical-lab` @ `3d33d2614d2c7ba9e6b698704e8f67976b17e1e5`.
- Both source repositories are private and remain unchanged.
- See [DATA_PROVENANCE.md](DATA_PROVENANCE.md).

## 7. License

The repository uses a mixed-provenance licensing model.

The MIT License applies only to user-authored source code and computational input files unless otherwise stated. Coursework reports and user-generated scientific figures remain copyright Xinyu Du. Datasets and third-party/course materials retain their original provenance.

See [LICENSE](LICENSE) and [DATA_PROVENANCE.md](DATA_PROVENANCE.md).
