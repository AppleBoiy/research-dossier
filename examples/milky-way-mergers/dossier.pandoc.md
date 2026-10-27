---
title: "Reconstructing the Milky Way's last major merger from its stars"
author: "Research Suite showcase"
date: 2026-10-27
bibliography: references.bib
link-citations: true
---

> **Question:** How are galaxy merger histories reconstructed from stellar data?

## The short answer

The Milky Way's merger history is read from the **orbits, chemistry and ages of its stars**. Gaia astrometry combined with spectroscopic surveys revealed a radially anisotropic population in the inner halo that most studies attribute to one massive accretion event, Gaia-Sausage-Enceladus (GSE), roughly 8–11 Gyr ago [@belokurov2018formation; @helmi2018merger]. Tailored simulations fitted to survey data suggest GSE delivered about half of the stellar halo [@naidu2021reconstructing], and several independent tracers indicate it was gas-rich and helped build the thick disc [@grand2020dual; @ciuca2023chasing]. The open questions are how massive it really was, how long its own star formation lasted, and whether earlier mergers of similar size are hidden in the inner Galaxy [@fragkoudi2020chemodynamics; @massari2026evidence].

**Key takeaways**

1. Kinematics find the debris, chemistry confirms it: clean GSE samples need both orbital actions and metallicity, not kinematics alone [@feuillet2020skymapper].
2. Three different tracers — simulations, stellar ages and globular-cluster ages — agree that GSE was a gas-rich merger [@grand2020dual; @ciuca2023chasing; @valenzuela2023galaxy].
3. Most observational studies call GSE a major merger, but bulge chemodynamics in simulations allow only a mass ratio of a few per cent [@fragkoudi2020chemodynamics].
4. Globular-cluster ages are emerging as a precise clock for mergers, revealing a second event about 1.8 Gyr before GSE [@massari2026evidence; @massari2023cluster].

## What the literature says

### Finding the debris: kinematics plus chemistry

The starting point is a population of halo stars on highly radial orbits whose anisotropy cannot be produced by continuous accretion of small satellites [@belokurov2018formation]. Gaia DR2 showed that local halo stars split into a blue colour–magnitude sequence of accreted stars and a red sequence that is the dynamically heated old disc [@haywood2018disguise]. Selecting members cleanly remains the main methodological issue: selections in a single kinematic space are contaminated, while combining radial action, angular momentum and metallicity gives a narrow metallicity distribution centred at [Fe/H] ≈ −1.17 [@feuillet2020skymapper]. Newer work adds unsupervised clustering (t-SNE and HDBSCAN) on combined APOGEE and Gaia data [@plevne2025estimating].

### A gas-rich merger that shaped the disc

Cosmological simulations find the GSE-like merger gas-rich, fuelling a central starburst that rapidly forms a compact thick disc [@grand2020dual]. Machine-learned ages for 68,360 APOGEE giants show the matching chemical signature — a metallicity dip and [Mg/Fe] rise followed by enrichment [@ciuca2023chasing]. Simulations further link the merger to the formation of the bar within about 1 Gyr [@merrow2024did] and to the long-lived disc warp [@deng2024potential], and show that such mergers steepen gas metallicity gradients and can seed a second low-α sequence [@buck2023early].

### The progenitor's own history, from abundances

Detailed abundances turn GSE debris into a record of the dwarf galaxy that was destroyed. GSE stars show higher [Eu/Mg] than in-situ stars, pointing to r-process enrichment by neutron-star mergers [@matsuno2021process]. Neutron-capture and α-element trends imply star formation that began gradually, lasted over 2 Gyr and was quenched near [Fe/H] ≈ −0.5 as GSE fell in [@ernandes2024gaia], whereas a chemical-evolution fit prefers a short timescale with strong outflows and a gas mass near 4.9 × 10⁹ M⊙ [@plevne2025estimating].

### Clocks for other mergers: globular clusters and streams

Globular-cluster ages provide timing that field stars cannot. The Milky Way's GC age distribution is bimodal, with younger clusters tied to GSE and plausibly formed in the merger itself [@valenzuela2023galaxy]. Homogeneous relative ages from the CARMA project separate in-situ from accreted clusters [@massari2023cluster] and now reveal a third age–metallicity sequence: a merger of similar stellar mass about 1.8 Gyr before GSE [@massari2026evidence]. Thin stellar streams, over a hundred of them now found with Gaia, add tracers of smaller accreted systems and of the Galactic potential [@bonaca2024stellar; @ibata2019streams].

## Where the evidence disagrees

### gaia-sausage-enceladus was a major merger

Observational studies agree GSE was a major event — about half of the stellar halo and 20% of the dark matter [@naidu2021reconstructing], a satellite above 10¹⁰ M⊙ in virial mass [@belokurov2018formation], a stellar mass of 10^8.85–9.85 M⊙ [@feuillet2020skymapper]. Simulations matched to the bulge instead allow only a few per cent mass ratio [@fragkoudi2020chemodynamics]. The two sides use different evidence (halo debris vs bulge chemodynamics) and different definitions of mass, so the disagreement is about scale and method rather than about whether the merger happened.

### gaia-sausage-enceladus had extended star formation

Abundance trends in SAGA stars favour gradual star formation lasting over 2 Gyr [@ernandes2024gaia]; a chemical-evolution model fitted to APOGEE stars favours a short timescale [@plevne2025estimating]. Sample selection and model assumptions differ, and the second study is a preprint — a direct comparison on the same stars would settle it.

### in-situ stellar halo is detected in milky way survey data

With Gaia DR2 alone, the in-situ halo could not be robustly identified and may be heated disc plus merger debris [@haywood2018disguise]; adding APOGEE aluminium abundances later isolated a metal-poor in-situ component, Aurora [@belokurov2022dawn]. Better chemistry, not new theory, resolved this one.

## Open questions

1. What is GSE's mass once halo-debris and bulge-chemodynamics constraints are fitted together [@fragkoudi2020chemodynamics; @naidu2021reconstructing]?
2. Did GSE form stars for more than 2 Gyr or in a short burst, when measured on one common sample [@ernandes2024gaia; @plevne2025estimating]?
3. How many inner-Galaxy mergers like Low-energy-Kraken-Heracles remain to be dated with globular clusters [@massari2026evidence]?
4. Do the predicted retrograde GSE streams beyond 30 kpc exist [@naidu2021reconstructing]?

## How this review was made

Papers were found with paper-scout across OpenAlex and arXiv (Semantic Scholar was rate-limited during the run), snowballed from the four top-ranked papers, and screened to 21 studies on stellar evidence for the Milky Way's merger history. Claims were extracted from abstracts only, so every claim is capped at medium confidence; preprints are marked.

## References

::: {#refs}
:::
