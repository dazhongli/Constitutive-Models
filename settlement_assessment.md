---
bibliography: [constitutive_model.bib, ../stone-column/reclamation.bib]
---

\pagebreak

# Introduction

In the offshore geological conditions of Hong Kong, the bearing stratum for Deep Cement Mixing (DCM) treatment for seawalls typically consists of alluvium, which exhibits a layered soil composition resulting from complex depositional processes. To ensure overall stability, a numerical assessment using the finite element method is commonly employed to evaluate slope stability, bearing resistance, and sliding failures. Stability analyses often utilize a strength reduction approach, wherein the soil strength is gradually reduced by a multiplier until the model fails to converge.

Furthermore, in addition to stability assessment, finite element analyses are utilized to conduct more detailed deformation analysis, including the evaluation of consolidation settlement and seawall movement. These analyses are particularly valuable when dealing with composite ground and the time-dependent response of the system, as classical analytical solutions may not adequately capture these complexities due to simplified assumptions.

This note offers commentaries on the material models available in Plaxis. It also provides suggested typical soil parameters that can be utilized for preliminary analysis. However, it is essential for the designer to consider site-specific data and possess a comprehensive understanding of advanced soil models to ensure a professional and accurate assessment of the stability of DCM-treated seawalls in the offshore geological conditions of Hong Kong.

# Stability Analyses

## Undrained Analyses - Short Term Stability Analysis

In the case of seawall design for reclamation, the primary focus is on the temporary conditions during the construction phase. These conditions involve significant surcharge loading on the seawall while the strength of the marine deposit remains insufficiently improved. Due to the low permeability of both the MD and deep-mixed soils, undrained analyses are essential to accurately assess stability. To ensure a well-defined strength reduction approach and certainty regarding shear strength at failure, it is recommended to employ the _Mohr-Coulomb model_.

As shear walls are typically arranged perpendicular to the seawall cope line, the DCM-treated area beneath the seawall is commonly represented as a composite mass in a two-dimensional plane strain modelthe mechanical properties of the composite mass are expressed using Eq.(\ref{eq_su_comp}) and Eq.(\ref{eq_E_comp}). It is important to note that the contribution from the soft soils is conservatively disregarded in this representation.

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

## Drained Analyses - Long-term Seawall Stability

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

# Settlement Assessment

Compared the `Mohr-Coulumb` model, the advanced soil models have several features that we are well understood for soft soils, therefore it is no point for using Mohr-Coulomb model for deformation analysis, unless an crude estimate is warranted in the design.

- nonlinear stiffness of soils
- higher unloading-reloading stiffness

There are several available advanced soil models available in Plaxis that are intended for soft clay including:

- Modified Camclay model
- Soft Soil Model
- Soft Soil Creep Model
- Hardening Soil Model

Other soil models exsit taking account of strength annostrop, NGI ADP model and cyclic behaviour soils UDCAM-S model which are generally not the primary concern for a reclamation projects.

To investigate the predictive capability of different material models for consolidation analyese, a series of FEA experiments were carried out and results are compared with the classic

![Plaxis Model \label{f_plaxi_model}](image/mode_set_up_Layer%201_copy_1.pdf){width=250}

## Settlement Predictive Capacities of the Existing Advanced Soil Models

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

### Modified Camclay Model (MCC)

According @Plaxis2021Mat[p.98], MCC model can be treated as an educational model available in Plaxis, its use in practical application is not recommended.

> The Modified Cam-Clay model may allow for extremely large shear stresses. This is particularly the case for stress paths that cross the critical state line. Furthermore, the Modified Cam-Clay model may give softening behaviour for particular stress paths. Without special regularization techniques, softening behaviour may lead to
> mesh dependency and convergence problems of iterative procedures. Moreover, the Modified Cam-Clay model cannot be used in combination with Safety analysis by means of phi-c reduction. The use of the Modified CamClay model in practical applications is not recommended.

### Soft Soil Model

## Hardening Soil Model (HS)

Soft soils can be analyzed with the HS; however, the hardening soil models are not suitable for very soft soil with high compressibility, i.e., $E_{oed}^{ref}/E_{50}^{ref}<0.5$ [@Plaxis2021Mat, p.110].

## Soft Soil Creep Model

The most significant feature of this model is that it can consider creep of the clay, i.e., commonly known as the secondary compression. There is ongoing debate on the uniqueness of the end-of-primary void ratio, two different side of supporter on this issue for Hypothesis A and Hypothesis B.

The use of this model will yield larger settlement given fed with the same set of parameters as in SS and HS model and settlement will continue to increase after the end of the primarily consolidation. This model provide a very handy tool for analysing the problem. The implementation of this model is considered a rigorous Hypothesis B model.

It is commented that this model is very sensitive to the specified OCR and can lead to significant amount of the creep settlement from model and is not recommended by @Karstunen2017 for engineers.

### Comparison of the Predictive Capabilities of the Advanced Constitutive Models

In this section, we will investigate the predictive capability of the available available soil models in **Table \ref{t_soil_model}** in terms of the consolidation analyses. Reclamation design is customarily carried assuming the 1D consolidation theory and applying Terzaghi's consolidation theory [@Terzaghi1943] or Barron's theory [@barron1948consolidation] when vertical drains are introduced. In the following numerical experiments, a series of unit cell models will be carried with same model configuration and soil properties, four(4) different soils model that are relevant to the consolidation analysis are employed to show the difference both the predicted total settlement as well as the associated time rate. The calculated results are then compared with that by 1D consolidation theory as recommended in Port Work Design Manual Part 3 [@CEO2002].

It should be noted that total magnitude of the consolidation is relatively less of uncertainty compared with rate of consolidation, which is subject to a number of factors that is normally difficult to quantify e.g., smear effect, well-resistance.

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

where

- $\Delta \sigma$ = added pressured at the top of soil
- $\gamma'$ = submerged unit weight of the soils
- $H$ = thickness of soils
- $e_0$ = initial void ratio
- $C_c$ = compression index, i.e., the slope of the virgin consolidation line under log10 scale of pressure
- $\sigma'_{vi}$ the effective vertical stress at the depth of $z_i$
- $z$ = depth of soil measured from the top where the loading is applied.

$$
\begin{equation}[label@eq_OCR1_20]
\begin{aligned}
H &= 10 \;
\\[8pt]
C_{c} &= 1.20 \;
\\[8pt]
e_{0} &= 2.00 \;
\\[8pt]
\gamma &= 6.00 \;
\\[8pt]
q &= 20 \;
\\[8pt]
Settlement &= \frac{ C_{c} }{ 1 + e_{0} } \cdot \left( H \cdot \log_{10} \left( \frac{ q + \gamma \cdot H }{ \gamma \cdot H } \right) - \frac{ q }{ \gamma } \cdot \log_{10} \left( q \right) + \frac{ q }{ \gamma } \cdot \log_{10} \left( q + \gamma \cdot H \right) \right) \\&= \frac{ 1.20 }{ 1 + 2.00 } \cdot \left( 10 \cdot \log_{10} \left( \frac{ 20 + 6.00 \cdot 10 }{ 6.00 \cdot 10 } \right) - \frac{ 20 }{ 6.00 } \cdot \log_{10} \left( 20 \right) + \frac{ 20 }{ 6.00 } \cdot \log_{10} \left( 20 + 6.00 \cdot 10 \right) \right) \\&= 1.30  \\[8pt]
\end{aligned}
\end{equation}
$$

$$
\begin{equation}[label@eq_OCR1_200]
\begin{aligned}
q &= 200 \;
\\[8pt]
Settlement &= \frac{ C_{c} }{ 1 + e_{0} } \cdot \left( H \cdot \log_{10} \left( \frac{ q + \gamma \cdot H }{ \gamma \cdot H } \right) - \frac{ q }{ \gamma } \cdot \log_{10} \left( q \right) + \frac{ q }{ \gamma } \cdot \log_{10} \left( q + \gamma \cdot H \right) \right) \\&= \frac{ 1.20 }{ 1 + 2.00 } \cdot \left( 10 \cdot \log_{10} \left( \frac{ 200 + 6.00 \cdot 10 }{ 6.00 \cdot 10 } \right) - \frac{ 200 }{ 6.00 } \cdot \log_{10} \left( 200 \right) + \frac{ 200 }{ 6.00 } \cdot \log_{10} \left( 200 + 6.00 \cdot 10 \right) \right) \\&= 4.07  \\[8pt]
\end{aligned}
\end{equation}
$$

Comparing the results from the 1D consolidation with **Figure \ref{f_OCR1_20kP}** and **Figure \ref{f_OCR1_200kPam}**, both Soft Soil Model and Hardening Model reasonable agreement with the analytical solution, whereas Modified Camclay model predicts much larger settlement, particularly under larger loading pressure.

When OCR is greater than 1.0, the compression of the soil will be greater, the total settlement can be calculated using a spreadsheet for OCR = 2.0,

Table:Ultimate Consolidation Settlement for OCR=2.0, H=10m (1D) \label{t_s_OCR2_H10}

| Surcharg Load | OCR | Settlement | Remarks                     |
| ------------: | --: | ---------: | --------------------------- |
|           kPa |   - |          m | -                           |
|            20 | 1.0 |       1.30 | Eq.(\ref{eq_OCR1_20})       |
|           200 | 1.0 |       4.07 | Eq.(\ref{eq_OCR1_200})      |
|            20 | 2.0 |       0.53 | Calculated with spreadsheet |
|           200 | 2.0 |       3.14 | Calculated with spreadsheet |

## Consolidation without Change in Permeability

It is noted with constant permeability within marine deposit, the consolidation under higher surcharge loading occurs much faster than under lower loading comparing **Figure \ref{f_OCR1_20kPam}** and **Figure \ref{f_OCR1_200kPam}**. It is shown from these figures, that the predictive capacity of Soft Soil Model and Hardening in terms of consolidation analysis are almost identical, whereas the Modified Camclay model, serving an educational model in Plaxis appears to overestimate of the total settlement.

![Settlement Curve for 10m Marine Deposit (OCR=1, $\Delta\sigma$ =20kPa and H = 10m)\label{f_OCR1_20kPam}](image/Soft_Soil_Creep_H_10_20kPa_OCR=1.pdf){width=550}

![Settlement Curve for 10m Marine Deposit (OCR=1, $\Delta\sigma$ =200kPa and H = 10m)\label{f_OCR1_200kPam}](image/Soft_Soil_Creep_H_10_200kPa_OCR=1.pdf){width=550}

![Settlement Curve for 10m Marine Deposit (OCR=2, $\Delta\sigma$ =20kPa and H = 10m)\label{f_OCR2_20kPam}](image/Soft_Soil_Creep_H_10_20kPa_OCR=2.pdf){width=550}

![Settlement Curve for 10m Marine Deposit (OCR=2, $\Delta\sigma$ =200kPa and H = 10m)\label{f_OCR2_100kPa}](image/Soft_Soil_Creep_H_10_200kPa_OCR=2.pdf){width=550}

From **Figure \ref{f_10m}**, other than Soft Soil Creep model, which incorporate the creep in to the calculation, the performance of the three models are quite similar

## Change the Permeability

As we have demonstrated with the constant permeability throughout the entire the consolidation process, the consolidation will depend on the applied stresses. In this section, we will explain the cause of this and further setting that is necessary to make the numerical modelling yield a consistent with classic Terzaghi's consolidation theory.

For consolidation analyses, the degree of consolidation at any time $t$ is governed by a coefficient of consolidation, defined in Eq.(\ref{eq_ch}). This reflect the two factors that contribute to the consolidation, $E_oed$ is constrained modulus and $k$ is the permeability of materials.

$$
\begin{equation}[label@eq_ch]
c_h = \frac{E_{oed\cdot k}}{\gamma_w}
\end{equation}
$$

$$
\begin{equation}[label@eq_Eoed]
E_{oed} = \frac{\sigma_v'}{\lambda^*}
\end{equation}
$$

![Typical Stress Strain Relationship for Soft Soil \label{f_stress_strain}](image/stress_stain_soft_soil.pdf){width=300}

As shown in **Figure \ref{f_stress_strain}**, as the soil consolidates, it gets stiffer with and increased compression modulus denoted as $E_{oed}$, and it can be expressed as Eq.(\ref{eq_Eoed}). If we maintain the permeability constant, according Eq.(\ref{eq_ch}), the coefficient will increase during the consolidation with an increased effective vertical stress.

![Degree of Consolidation under Different Consolidation Pressure with Constant Permeability\label{f_doc_k_const}](image/Soft_Soil_Creep_H_10-DoC%20constant%20k.pdf){width=450}

In Terzaghi's solution, the coefficient of the consolidation remains constant during the entire consolidation process. This assumptions was made simply to get a solution of the set of partial differential equations. To keep consistent with this assumption, we will need to have $c_{h,1} = c_{h,2}$, i.e.,

$$
\begin{equation}[label@eq_k_stress]
c_{h,1} = c_{h,2} \Rightarrow \frac{E_{oed,0} \cdot k_0}{\gamma_w} = \frac{E_{oed,1} \cdot k_1}{\gamma_w} \Rightarrow \log\bigg(\frac{k_1}{k_0}\bigg) = \log\bigg(\frac{\sigma_1}{\sigma_0}\bigg)
\end{equation}
$$

In the case of typical soft clay, it is often observed that the virgin compression line exhibits a nearly linear relationship in an $e-\log\sigma'$ space, with a slope defined as the compression index $C_c$, as shown in Eq.(\ref{eq_delta_e}). By substituting Eq.(\ref{eq_delta_e}) into Eq.(\ref{eq_k_stress}), we obtain Eq.(\ref{eq_k_change}). This relationship holds true when we make the same assumption as classical soil mechanics, namely that the coefficient of consolidation remains constant during consolidation.

The assumption of a constant coefficient of consolidation is reasonable due to the opposing effects of increasing stiffness and decreasing permeability as the void ratio decreases. These effects tend to balance each other out. However, it is important to note that this assumption was initially made to simplify the solution of the system.

In the Plaxis, a generic term $c_k$ is adopted instead of $c_c$ in Eq.(\ref{eq_k_change}). Typically, detailed permeability measurements are rarely conducted in practical applications. Therefore, it is recommended to enable this advanced function in order to ensure consistency with conventional assumptions, despite the limited availability of comprehensive permeability data.

$$
\begin{equation}[label@eq_delta_e]
\Delta e = -C_c \cdot \log\bigg(\frac{\sigma_1}{\sigma_0}\bigg)
\end{equation}
$$

$$
\begin{equation}[label@eq_k_change]
\log \bigg(\frac{k}{k_0}\bigg) = \frac{\Delta e}{C_c}
\end{equation}
$$

$$
\begin{equation}[label@eq_k_plaxis]
\log \bigg(\frac{k}{k_0}\bigg) = \frac{\Delta e}{c_k}
\end{equation}
$$

![Degree of Consolidation under Different Consolidation Pressure with Changing Permeability\label{f_doc_change_k}](image/Soft_Soil_Creep_H_10-DoC%20changing%20k.pdf){width=450}

As can be seen from **Figure \ref{f_doc_change_k}**, after considering the changing of permeability with $c_k = C_c$, the time-rate of consolidation under different loadings are getting similar.

## Initial Stiffness and Convergence Analysis

In the preceding section, we have demonstrated that it is necessary update the permeability order to be consistent with the classical consolidation theory that the coefficient of consolidation remains constant throughout the entire consolidation process. In this section, we will further investigation how to specify the permeability which was left unaddressed so far.

In the intial design the coefficient is typically used and often this is based on the back-calculated data from previous experience. Based on the experience of the recent reclamation project, a lumped $c_h = 1.2m^2/year$ is considered, this lumped parameter is supposed to already accounted for the smear effect and well-resistance which is typically difficult to quantify with accuracy.

To compare with the analytical solutions, we will this $c_h$, 

### Parameters in Hardening Soil Model

We have demonstrated that the hardening soil model, which is the latest soil with an attempt to improve the prediction performance over the educational model Modified Camclay model and as and extension of soft soil model. In this section, the input parameter is discussed and how the design parameters can be approximated.

In Hardening soil model, it is assumed that the stiffness varies with the stress level as shown in Eq.XXX and Eq.XXX and Eq.xXX, i

It should be noted that for $E_{oed}^{ref}$ the reference stress is $\sigma_1'$ whereas for $E_{ur}^{ref}$ and $E_{50}^{ref}$, the reference stress is $\sigma'_3$, this is to be consistent with the testing method, that is, the $E_{oed}$ is determined from the oedometer tests, the stress level specified is typically $\sigma_1$ while the $E_{50}^{ref}$ and $E_{ur}^{ref}$ are determined from the triaxial test, the specified stress level is the confining pressure, i.e., $\sigma_3$.

We will limit our discussion for now on soft soil only, though Hardening soils can also be used for granular material. 

$$ 
\begin{equation}[label@eq_oed]
E_{\text{oed}} = E_{\text{oed}}^{\text{ref}} \left( \frac{-\sigma_{1}'}{p^{\text{ref}}} \right)^m
\end{equation}
$$

$$ 
\begin{equation}[label@eq_E50]
E_{50} = E_{50}^{\text{ref}} \left( \frac{c\cos(\varphi) - \sigma_{3}'\sin(\varphi)}{c\cos(\varphi) + p^{\text{ref}}\sin(\varphi)} \right)^m
\end{equation}
$$

$$ 
\begin{equation}[label@eq_Eur]
E_{ur} = E_{ur}^{\text{ref}} \left( \frac{c\cos(\varphi) - \sigma_{3}'\sin(\varphi)}{c\cos(\varphi) + p^{\text{ref}}\sin(\varphi)} \right)^m
\end{equation}
$$

> @Plaxis2021Mat[p.69] "In many practical application, it is appropriate to set $E_{ur}^{ref}$ = 3$E_{50}^{ref}$

### Design Parameters for Marine Deposit in Hong Kong

#### $m$ 

m =1 is a good estimate of the most of the soft soils and such assumption is consistent with the conventional assumption on consolidation assessment, please see Eq.(\ref{eq_eq_Eoed}), where we've already implicitly assumed $m=1$, i.e., the compression curve is linear in $e-\log\sigma$ space.

#### $E_{oed}$ 

$E_{oed}$ is defined as 



### DCM Treated Area

In this Section, a plane strain model will be used to study the load shear of the shear wall, and the particular focus is made on the load shearing between the DCM columns and the tributary soils and the stress concentration.

Given the typical column width of 0.6m and spacing of 1.2m, the unit model at the area can be shown in Figure XXX. Hardening soil model will be adopted for MD and Mohr Column soil models is used for DCM columns. It is assumed that the stone columns are linear elastic and not subjected to consolidation process.

For reclamation projects, the significant portion of the settlement are due to the compression of soft marine clay. Once treated, the total compression of this layer can be reduced significantly. Consider a typcial

# Recommendation

We have demonstrated using a unit cell model the following:

The predictive capacities of the _Soft Soil_ (SS) model and the _Hardening Soil_ (HS) model are comparable in terms of consolidation analyses. The HS model was developed later to extend the analyses to cover over-consolidated clay. As shown, when the parameter $m=1$ is set, the HS model provides a good representation of soft soils.
Input Parameters: However, the HS model requires significantly more input parameters than the SS model, which can be confusing for practicing engineers.
Underlying Alluvial Clay: For the underlying alluvial clay, which is typically in an over-consolidated state in situ, further consolidation of the alluvial clay can become an issue.

It is not recommended to use advanced soil models for stability analyses. Instead, stability analyses should be performed using the Mohr-Coulomb model, and the strength gain can be assessed using the Stress History and normalized soil engineering properties (SHANSEP) concept.
If advanced models are to be adopted in a project, it is recommended that laboratory testing be carried out by practicing engineers to ensure that the model can predict the expected response, at least under given boundary conditions. Particularly, the increase in strength should be carefully evaluated.

The typical elastic stiffness of soft soils in Hong Kong is related to the significant amount of consolidation settlement within the main reclamation area. Settlement can be on the order of 6 meters, with most of this settlement occurring in the early stages of sandfilling. Even with high-quality site control, lateral displacement and squeezing of marine deposits (MD) are very difficult to control.

The estimate of total settlement on site is typically very rough, making the application of a more advanced model less justified.
Consolidation Period: For reclamation projects, handover criteria commonly include the rate of settlement or the estimate of residual settlement. In both Hypothesis A and Hypothesis B, it is assumed that there is a constant slope in the log(t) scale.
Underlying Clay: Unlike locations with very thick underlying clay layers, such as Japan's airport, the alluvial clay underlying the reclamation in Hong Kong is layered. It is not expected that significant differences between Hypothesis A and Hypothesis B will yield large differences in outcomes.
Despite ongoing developments, as demonstrated above, Hypothesis B provides an elegant way of analyzing the project and presents a modern method for estimating creep

\pagebreak


# Appendix A - Example of Derivation of the Permeability {-}

Certainly! Here is the digitized version with equations wrapped using `$$ \begin{equation} ... \end{equation} $$`:

---



$$
\begin{equation}
\sigma_v' \text{ at } 2.5 \text{ m} = \sigma_v' = 2.5 \times 6 = 15 \text{ kPa}
\end{equation}
$$

$$
\begin{equation}
E_{eod} = 2.3 \times \frac{1 + e_0}{C_c} \cdot \sigma_v'
\end{equation}
$$

$$
\begin{equation}
E_{eod} = 2.3 \times \frac{1 + 2.0}{1.2} \times 15
\end{equation}
$$

$$
\begin{equation}
E_{eod} = 86.25 \text{ kPa}
\end{equation}
$$

$$
\begin{equation}
C_h = \frac{E_{eod} \cdot K}{\gamma_w}
\end{equation}
$$

$$
\begin{equation}
\Rightarrow K = \frac{\gamma_w \cdot C_h}{E_{eod}}
\end{equation}
$$

Given:
$$
\begin{equation}
C_h = 1.2 \text{ m}^2/\text{year}
\end{equation}
$$

$$
\begin{equation}
K_h = \frac{10.0 \times 1.2}{365 \times 86.25}
\end{equation}
$$

$$
\begin{equation}
K_h = 3.81 \times 10^{-4} \text{ m}^2/\text{day}
\end{equation}
$$


$$
\begin{equation}
4 \times 100
\end{equation}
$$

$$
\begin{equation}
d_{w} = \frac{2 \times (4 + 100)}{\pi} = 66.28 \text{ mm} \approx 0.066 \text{ m}
\end{equation}
$$

$$
\begin{equation}
r_{w} = \frac{d_{w}}{2} = 0.033 \text{ m}
\end{equation}
$$

$$
\begin{equation}
r_e = 0.67 \text{ m}
\end{equation}
$$

$$
\begin{equation}
n = \frac{d_e}{d_{w}} = \frac{0.67 \times 2}{0.066} = 20.303
\end{equation}
$$

$$
\begin{equation}
d_e = 1.2 \times 1.05 = 1.26 \text{ m}
\end{equation}
$$

$$
\begin{equation}
r_e = \frac{1.26}{2} = 0.63 \text{ m}
\end{equation}
$$
