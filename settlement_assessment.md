---
bibliography: [constitutive_model.bib, ../stone-column/reclamation.bib]
---

\pagebreak

# Introduction

Deep Cement Mixing (DCM) treatment for seawalls in the context of alluvial deposits typically characterized the layered soil composition resulting from complex depositional processes. To ensure overall stability, numerical assessment is necessary for checking the slope stability, bearing resistance, and sliding failures. These stability analyses commonly employ a strength reduction approach, gradually reducing the soil strength until the model fails to converge. For stability assessment, the Mohr-Coulomb model recommended to be adopted for both deep-mixed zone and untreated soils.

# Undrained Analyses

In the case of seawall design for reclamation, the governing load case in terms of stability is the temporary conditions where the seawall retains significant surcharge loading at the main reclamation area while the strength of the marine deposit remains insufficiently improved. Given the low permeability of both the marine deposit MD and deep-mixed soils, undrained analyses are essential during the construction phase. It is recommended to employ the Mohr-Coulomb model to ensure a well-defined strength reduction approach and certainty regarding shear strength at failure. As shear walls are typically arranged perpendicular to the seawall cope line, the DCM treated area beneath the seawall is commonly represented as a composite mass in 2D plane strain model and the smeared properties are adopted in the format. The mechanical properties for the composite mass can be expressed as Eq.(1), note the contribution from the soft soils are conservatively disregarded.

$$
\begin{equation}[label@eq_su_comp]
s_u = \alpha_s \cdot s_{dm}
\end{equation}
$$

$$
\begin{equation}[label@eq_E_comp]
E_{comp} = \alpha_s \cdot E_{dm}
\end{equation}
$$

where

- $\alpha_s$ = area replacement ratio
- $s_{dm}$ = design shear strength of the deep-mixed soils
- $E_{dm}$ = design elastic modulus of deep mixed soils

For a typical DCM treatment using wet mixing and good quality control, the elastic modulus of DCM may be taken as 300UCS, i.e., given a design UCS of 1MPa, the $E_dm$ = 300MPa.
Since the failure criterion for both DCM and MD are stress independent, reducing concerns of increased shear resistance within deep-mixed soils due to stress concentration, which is more critical to granular inclusions such as stone columns. As such, the deformation parameters are less critical provided movement prediction is not the primary concern of the analysis.

Kitazume et al. reported that a 15% of the UCS strength is used in Japan with wet mixing method and the in US practice, tensile strength is generally not relied on in the design [@FHADM2013, P.46]. It is recommended that "Tension cut-off" is always activated and the tensile strength is set as 0 kPa.

# Drained Analyses - Long-term Seawall Stability

Long-term stability analyses are conducted considering sufficient time for excess pore water pressure to dissipate. This aspect primarily governs design situations involving stiff/hard clay existing at shallower depth, where the undrained strength exceeds the drained strength. However, in the case of DCM design in the context of the offshore geological condition in Hong Kong, presence of the stiff/hard clay is not common, and the long-term stability using drained parameters do not typically govern the design.

Nevertheless, to perform an effective stress analysis under a drained condition, the corresponding effective friction angles and cohesion should be specified for the DCM treated blocks. For DCM treated soils, the literature indicates that under the typical stress range, $c'$=400kPa and $\varphi'$=58&deg; is recommended by Li and Kwok (2023) for a stress range of 50 ~ 200kPa. In the drained analysis, considering the effective friction angle of marine deposit ranging from 20~30&deg;, the contribution of the MD in the drained analysis would be too significant to ignore and therefore the equivalent parameter for drained analysis is calculated as below.

$$
\begin{equation}[label@eq_phi_comp]
\varphi'_{comp} = \tan^{-1}(\alpha_s \cdot \varphi'_{dm} + (1-\alpha_s)\cdot \varphi'_s)
\end{equation}
$$

$$
\begin{equation}[label@eq_c_comp]
c'_{comp} = \alpha_s \cdot c'_{dm} + (1-\alpha_s)\cdot c'_s
\end{equation}
$$

# Recommended Soil Models and Parameters for Settlement Assessment

Mohr-Coulomb materials are known to not perform well for settlement assessment. Therefore, the movement obtained using the Mohr-Coulomb model should be considered as a first-order approximation. We will limit our discussion on the constitutive soil models within Plaxis which are most familiar to the local practicing engineers.

To calculate the time-rate of the settlement, advanced soil models should be used. The available advanced soil models that are available in Plaxis include the following. Other than typical engineering properties, some unique input for the advanced models are presented in **Table \ref{t_soil_model}**.

Table: Advanced Materials Models for Soils in Plaxis \label{t_soil_model}

| Soil Model            | Required Input                               | Remarks |
| --------------------- | -------------------------------------------- | ------- |
| Modified Camclay      | $\lambda = \frac{C_c}{2.3}$                  |         |
|                       | $\kappa = \frac{C_s}{2.3}$                   |         |
|                       | $M_{SCL} = \frac{C_s}{2.3}$                  |         |
| Soil Soil Model       | $\lambda^* = \frac{C_s}{2.3(1+e_0)}$         |         |
|                       | $\kappa^* \approx \frac{2.0C_s}{2.3(1+e_0)}$ |         |
| Soil Soil Creep Model | $\lambda^*, \kappa^*$                        |         |
| Hardening Soil Model  | $E_{50}, E_{oed}, E_{ref}$                   |         |
| Hardening Soil Model  | $m=1$ for soft clay                          |         |

## Hardening Soil Model

Hardening soils allows alternative input parameters using $C_c$ and $C_s$, which is readily available from the odometer tests results.

# Calibration of Soil Models

## Normally Consolidated Clay

The following typical design parameters will be used for this calibration purpose.

Table:Design Parameters for Normally Consolidated Marine Deposit \label{t_design_params}

| Desorption                    |  Notation |  Value |
| ----------------------------- | --------: | -----: |
| Compression Index             |     $C_c$ |    1.2 |
| Initial Void Ratio            |     $e_0$ |    2.0 |
| Over Consolidation Ratio      |     $OCR$ |    1.0 |
| Submerged unit weight of soil | $\gamma'$ |    6.0 |
| Thickness of Soils            |       $H$ | varies |

$$
\begin{equation}[label@eq_]
s_i = \frac{C_c}{1+e_0} \cdot \log\bigg(\frac{\sigma'_{vi} + \Delta\sigma_v}{\sigma'_{vi}}\bigg)
\end{equation}
$$

For the normally consolidated clay with OCR of 1.0, the initial effective stress can be calculated as $\sigma'_{vi} = z \cdot \gamma$ and therefore the total settlement for a given thickness $H$ of MD can be calculated as in Eq.(\ref{eq_stotal}).

$$
\begin{equation}[label@eq_]
s = \int_0^H \frac{C_c}{1+e_0} \log\bigg(\frac{z\cdot \gamma' + \Delta\sigma_v}{z\cdot \gamma'}\bigg) dz
\end{equation}
$$

$$
\begin{equation}[label@eq_stotal]
S(H)= \frac{C_c}{1+e_0} \bigg[H \cdot \log\bigg(\frac{\Delta\sigma+\gamma'\cdot H}{\gamma' H}\bigg) - \frac{\Delta\sigma}{\gamma'}\log(\Delta\sigma) + \frac{\Delta\sigma}{\gamma'}\log(\Delta\sigma+\gamma'H)\bigg]
\end{equation}
$$

\pagebreak

# Reference
