# Reconstructing the Milky Way's last major merger from its stars

> **Question:** How are galaxy merger histories reconstructed from stellar data?

## The short answer

The Milky Way's merger history is read from the **orbits, chemistry and ages of its stars**. Gaia astrometry combined with spectroscopic surveys revealed a radially anisotropic population in the inner halo that most studies attribute to one massive accretion event, Gaia-Sausage-Enceladus (GSE), roughly 8–11 Gyr ago [1, 2]. Tailored simulations fitted to survey data suggest GSE delivered about half of the stellar halo [3], and several independent tracers indicate it was gas-rich and helped build the thick disc [4, 5]. The open questions are how massive it really was, how long its own star formation lasted, and whether earlier mergers of similar size are hidden in the inner Galaxy [6, 7].

**Key takeaways**

1. Kinematics find the debris, chemistry confirms it: clean GSE samples need both orbital actions and metallicity, not kinematics alone [8].
2. Three different tracers — simulations, stellar ages and globular-cluster ages — agree that GSE was a gas-rich merger [4, 5, 9].
3. Most observational studies call GSE a major merger, but bulge chemodynamics in simulations allow only a mass ratio of a few per cent [6].
4. Globular-cluster ages are emerging as a precise clock for mergers, revealing a second event about 1.8 Gyr before GSE [7, 10].

## What the literature says

### Finding the debris: kinematics plus chemistry

The starting point is a population of halo stars on highly radial orbits whose anisotropy cannot be produced by continuous accretion of small satellites [1]. Gaia DR2 showed that local halo stars split into a blue colour–magnitude sequence of accreted stars and a red sequence that is the dynamically heated old disc [11]. Selecting members cleanly remains the main methodological issue: selections in a single kinematic space are contaminated, while combining radial action, angular momentum and metallicity gives a narrow metallicity distribution centred at [Fe/H] ≈ −1.17 [8]. Newer work adds unsupervised clustering (t-SNE and HDBSCAN) on combined APOGEE and Gaia data [12].

### A gas-rich merger that shaped the disc

Cosmological simulations find the GSE-like merger gas-rich, fuelling a central starburst that rapidly forms a compact thick disc [4]. Machine-learned ages for 68,360 APOGEE giants show the matching chemical signature — a metallicity dip and [Mg/Fe] rise followed by enrichment [5]. Simulations further link the merger to the formation of the bar within about 1 Gyr [14] and to the long-lived disc warp [15], and show that such mergers steepen gas metallicity gradients and can seed a second low-α sequence [13].

### The progenitor's own history, from abundances

Detailed abundances turn GSE debris into a record of the dwarf galaxy that was destroyed. GSE stars show higher [Eu/Mg] than in-situ stars, pointing to r-process enrichment by neutron-star mergers [16]. Neutron-capture and α-element trends imply star formation that began gradually, lasted over 2 Gyr and was quenched near [Fe/H] ≈ −0.5 as GSE fell in [17], whereas a chemical-evolution fit prefers a short timescale with strong outflows and a gas mass near 4.9 × 10⁹ M⊙ [12].

### Clocks for other mergers: globular clusters and streams

Globular-cluster ages provide timing that field stars cannot. The Milky Way's GC age distribution is bimodal, with younger clusters tied to GSE and plausibly formed in the merger itself [9]. Homogeneous relative ages from the CARMA project separate in-situ from accreted clusters [10] and now reveal a third age–metallicity sequence: a merger of similar stellar mass about 1.8 Gyr before GSE [7]. Thin stellar streams, over a hundred of them now found with Gaia, add tracers of smaller accreted systems and of the Galactic potential [19, 18].

## Where the evidence disagrees

### gaia-sausage-enceladus was a major merger

Observational studies agree GSE was a major event — about half of the stellar halo and 20% of the dark matter [3], a satellite above 10¹⁰ M⊙ in virial mass [1], a stellar mass of 10^8.85–9.85 M⊙ [8]. Simulations matched to the bulge instead allow only a few per cent mass ratio [6]. The two sides use different evidence (halo debris vs bulge chemodynamics) and different definitions of mass, so the disagreement is about scale and method rather than about whether the merger happened.

### gaia-sausage-enceladus had extended star formation

Abundance trends in SAGA stars favour gradual star formation lasting over 2 Gyr [17]; a chemical-evolution model fitted to APOGEE stars favours a short timescale [12]. Sample selection and model assumptions differ, and the second study is a preprint — a direct comparison on the same stars would settle it.

### in-situ stellar halo is detected in milky way survey data

With Gaia DR2 alone, the in-situ halo could not be robustly identified and may be heated disc plus merger debris [11]; adding APOGEE aluminium abundances later isolated a metal-poor in-situ component, Aurora [20]. Better chemistry, not new theory, resolved this one.

## Open questions

1. What is GSE's mass once halo-debris and bulge-chemodynamics constraints are fitted together [6, 3]?
2. Did GSE form stars for more than 2 Gyr or in a short burst, when measured on one common sample [17, 12]?
3. How many inner-Galaxy mergers like Low-energy-Kraken-Heracles remain to be dated with globular clusters [7]?
4. Do the predicted retrograde GSE streams beyond 30 kpc exist [3]?

## How this review was made

Papers were found with paper-scout across OpenAlex and arXiv (Semantic Scholar was rate-limited during the run), snowballed from the four top-ranked papers, and screened to 21 studies on stellar evidence for the Milky Way's merger history. Claims were extracted from abstracts only, so every claim is capped at medium confidence; preprints are marked.

## References

1. Belokurov, V. A., Erkal, D., Evans, N. W., Koposov, S. E., & Deason, A. J. (2018). Co-formation of the disc and the stellar halo★. *Monthly Notices of the Royal Astronomical Society*. https://doi.org/10.1093/mnras/sty982
   - Shows the local halo's extreme radial anisotropy at [Fe/H] > −1.7 and argues for one massive accretion 8–11 Gyr ago.
2. Helmi, A., Babusiaux, C., Koppelman, H. H., Massari, D., Veljanoski, J., & Brown, A. G. A. (2018). The merger that led to the formation of the Milky Way’s inner stellar halo and thick disk. *Nature*. https://doi.org/10.1038/s41586-018-0625-x
   - The Nature paper that named Gaia-Enceladus as the merger building the inner halo and thick disc.
3. Naidu, R. P., Conroy, C., Bonaca, A., Zaritsky, D., Weinberger, R., Ting, Y. S., …, & Cargile, P. A. (2021). Reconstructing the Last Major Merger of the Milky Way with the H3 Survey. *The Astrophysical Journal*. https://doi.org/10.3847/1538-4357/ac2d2d
   - First tailored N-body simulations of GSE, fitted to H3 survey data; predicts a double-break halo density profile and distant retrograde streams.
4. Grand, R. J. J., Kawata, D., Belokurov, V. A., Deason, A. J., Fattahi, A., Fragkoudi, F., …, & Pakmor, R. (2020). The dual origin of the Galactic thick disc and halo from the gas-rich Gaia–Enceladus Sausage merger. *Monthly Notices of the Royal Astronomical Society*. https://doi.org/10.1093/mnras/staa2057
   - Auriga simulations linking a gas-rich GSE to both the thick disc and the inner halo.
5. Ciucă, I., Kawata, D., Ting, Y. S., Grand, R. J. J., Miglio, A., Hayden, M., …, & Freeman, K. C. (2023). Chasing the impact of the Gaia-Sausage-Enceladus merger on the formation of the Milky Way thick disc. *Monthly Notices of the Royal Astronomical Society Letters*. https://doi.org/10.1093/mnrasl/slad033
   - Bayesian ML ages for 68k APOGEE giants reveal the chemical footprint of a gas-rich merger.
6. Fragkoudi, F., Grand, R. J. J., Pakmor, R., Blázquez-Calero, G., Gargiulo, I. D., Gómez, F. A., …, & White, S. D. M. (2020). Chemodynamics of barred galaxies in cosmological simulations: On the Milky Way’s quiescent merger history and in-situ bulge. *Monthly Notices of the Royal Astronomical Society*. https://doi.org/10.1093/mnras/staa1104
   - Counterpoint: bulge chemodynamics in simulations favour a quiet merger history and a small GSE.
7. Massari, D., Zerbinati, C., Fanelli, C., Helmi, A., Ceccarelli, E., Agelet, F. A., …, & Mucciarelli, A. (2026). Evidence of a massive accretion event 1.8 billion years before the Gaia-Sausage-Enceladus merger. *Nature Astronomy*. https://doi.org/10.1038/s41550-026-02931-5
   - Precise HST globular-cluster ages reveal a merger about 1.8 Gyr before GSE.
8. Feuillet, D. K., Feltzing, S., Sahlholdt, C., & Casagrande, L. (2020). The SkyMapper-Gaia RVS view of the Gaia–Enceladus–Sausage – an investigation of the metallicity and mass of the Milky Way’s last major merger. *Monthly Notices of the Royal Astronomical Society*. https://doi.org/10.1093/mnras/staa1888
   - Shows that action space plus photometric metallicity gives the cleanest GSE sample and estimates its mass.
9. Valenzuela, L. M., Remus, R. S., McKenzie, M., & Forbes, D. A. (2023). Galaxy archaeology for wet mergers: Globular cluster age distributions in the Milky Way and nearby galaxies. *A&A 687, A104 (2024)*. https://doi.org/10.1051/0004-6361/202348010
   - Globular-cluster age bimodality as a tracer of wet mergers in the Milky Way and nearby galaxies.
10. Massari, D., Agelet, F. A., Monelli, M., Cassisi, S., Pancino, E., Saracino, S., …, & Ceccarelli, E. (2023). Cluster Ages to Reconstruct the Milky Way Assembly (CARMA). *Astronomy and Astrophysics*. https://doi.org/10.1051/0004-6361/202347289
11. Haywood, M., Matteo, P. D., Lehnert, M. D., Snaith, O. N., Александрович, Х. С., & Gómez, A. (2018). In Disguise or Out of Reach: First Clues about In Situ and Accreted Stars in the Stellar Halo of the Milky Way from Gaia DR2. *The Astrophysical Journal*. https://doi.org/10.3847/1538-4357/aad235
   - Interprets Gaia DR2's dual halo sequence as accreted stars plus heated thick disc.
12. Plevne, O., & Akbaba, F. (2025). Estimating Initial Mass of Gaia-Enceladus Dwarf Galaxy with Chemical Evolution Model. *arXiv*. [Preprint — not peer-reviewed] https://arxiv.org/abs/2508.14890
   - Preprint; HDBSCAN-selected members and an OMEGA+ chemical evolution fit for GSE's initial mass.
13. Buck, T., Obreja, A., Ratcliffe, B., Lu, Y., Minchev, I., & Macciò, A. V. (2023). The impact of early massive mergers on the chemical evolution of Milky Way-like galaxies: insights from NIHAO-UHD simulations. *Monthly Notices of the Royal Astronomical Society*. https://doi.org/10.1093/mnras/stad1503
14. Merrow, A., Grand, R. J. J., Fragkoudi, F., & Martig, M. (2024). Did the Gaia Enceladus/Sausage merger form the Milky Way’s bar?. *Monthly Notices of the Royal Astronomical Society*. https://doi.org/10.1093/mnras/stae1250
15. Deng, M., Du, C., Yang, Y., Liao, J., & Ye, D. (2024). A Potential Dynamical Origin of the Galactic Disk Warp: The Gaia–Sausage–Enceladus Major Merger. *The Astrophysical Journal*. https://doi.org/10.3847/1538-4357/ad7799
16. Matsuno, T., Hirai, Y., Tarumi, Y., Hotokezaka, K., Tanaka, M., & Helmi, A. (2021). $R$-process enhancements of Gaia-Enceladus in GALAH DR3. *A&A 650, A110 (2021)*. https://doi.org/10.1051/0004-6361/202040227
17. Ernandes, H., Feuillet, D., Feltzing, S., & Skúladóttir, Á. (2024). Gaia-Sausage-Enceladus star formation history as revealed by detailed elemental abundances. *A&A 691, A333 (2024)*. https://doi.org/10.1051/0004-6361/202450827
   - Uses Eu, Ba, Mg and Fe ratios to reconstruct GSE's star formation history.
18. Ibata, R., Malhan, K., & Martin, N. F. (2019). The Streams of the Gaping Abyss: A Population of Entangled Stellar Streams Surrounding the Inner Galaxy. *The Astrophysical Journal*. https://doi.org/10.3847/1538-4357/ab0080
19. Bonaca, A., & Price-Whelan, A. M. (2024). Stellar streams in the Gaia era. *New Astronomy Reviews*. https://doi.org/10.1016/j.newar.2024.101713
20. Belokurov, V. A., & Kravtsov, A. V. (2022). From dawn till disc: Milky Way’s turbulent youth revealed by the APOGEE+ Gaia data. *Monthly Notices of the Royal Astronomical Society*. https://doi.org/10.1093/mnras/stac1267
21. Deason, A. J., & Belokurov, V. A. (2024). Galactic Archaeology with Gaia. *New Astronomy Reviews*. https://doi.org/10.1016/j.newar.2024.101706
