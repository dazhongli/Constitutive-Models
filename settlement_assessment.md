---
bibliography: [constitutive_model.bib, ../stone-column/reclamation.bib]
---

\pagebreak

# Introduction

In the offshore geological conditions of Hong Kong, the bearing stratum for Deep Cement Mixing (DCM) treatment for seawalls typically consists of alluvium, which exhibits a layered soil composition resulting from complex depositional processes. To ensure overall stability, a numerical assessment using the finite element method is commonly employed to evaluate slope stability, bearing resistance, and sliding failures. Stability analyses often adopt a strength reduction approach, wherein the soil strength is gradually reduced by a multiplier until the model fails to converge.

Furthermore, in addition to stability assessment, finite element analyses are utilized to conduct more detailed deformation analysis, including the evaluation of consolidation settlement and seawall movement. These analyses are particularly valuable when dealing with composite ground and the time-dependent response of the system, as classical analytical solutions may not adequately capture these complexities due to simplified assumptions.

This Note offers commentaries on the material models available in Plaxis. It also provides suggested typical soil parameters that can be used for preliminary analysis. However, it is essential for the designer to consider site-specific data and possess a comprehensive understanding of advanced soil models to ensure a professional and accurate assessment of the stability of DCM-treated seawalls in the offshore geological conditions of Hong Kong.

# Stability Analyses

## Undrained Analyses - Short Term Stability Analysis

In the case of seawall design for reclamation, the primary focus is on the temporary conditions during the construction phase. These conditions involve significant surcharge loading on the seawall while the strength of the marine deposit remains insufficiently improved. Due to the low permeability of both the MD and deep-mixed soils, undrained analyses are essential to accurately assess stability. To ensure a well-defined strength reduction approach and certainty regarding shear strength at failure, it is recommended to employ the _Mohr-Coulomb model_.

As shear walls are typically arranged perpendicular to the seawall cope line, the DCM-treated area beneath the seawall is commonly represented as a composite mass in a two-dimensional plane strain model the mechanical properties of the composite mass are expressed using Eq.(\ref{eq_su_comp}) and Eq.(\ref{eq_E_comp}). It is important to note that the contribution from the soft soils is conservatively disregarded in this representation.

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

Typical design parameters adopted for the undrained analyses are included in **Table \ref{t_D_input}**

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

Compared to the Mohr-Coulomb model, the advanced soil models have several features that are well-suited for modeling soft soils. The key advantages include:

- Consideration of nonlinear stiffness of soils
- Ability to capture higher unloading-reloading soil stiffness

Given these capabilities that better reflect the behavior of soft soils, there is little justification for using the simpler Mohr-Coulomb model in deformation analyses, unless a very crude estimate suffices for initial design scoping purposes. The advanced models are better equipped to predict consolidation behavior.

## Available Advanced Soil Models

There are several advanced soil models available in Plaxis that are intended for modeling soft clay, including:

- Modified Camclay model (MCC)
- Soft Soil Model (SS)
- Soft Soil Creep Model (SSC)
- Hardening Soil Model (HS)

Other soil models exist that take into account strength anisotropy, such as the NGI-ADP model, or cyclic behavior in soils like the UDCAM-S model; however, these are generally not the primary design concern for reclamation projects and hence will not be discussed.

To investigate the predictive capabilities of different material models for consolidation analyses, a series of FEA experiments were carried out and results are compared with classic consolidation theory.

### Modified Camclay Model (MCC)

According @Plaxis2021Mat[p.98], MCC model can be treated as an educational model available in Plaxis, its use in practical application is not recommended.

> The Modified Cam-Clay model may allow for extremely large shear stresses. This is particularly the case for stress paths that cross the critical state line. Furthermore, the Modified Cam-Clay model may give softening behaviour for particular stress paths. Without special regularization techniques, softening behaviour may lead to
> mesh dependency and convergence problems of iterative procedures. Moreover, the Modified Cam-Clay model cannot be used in combination with Safety analysis by means of phi-c reduction. The use of the Modified CamClay model in practical applications is not recommended.

In Plaxis, the MCC model was implemented with a Drucker-Prager failure surface, i.e., representing a cone in the principle stress space, rather than the Mohr-Coulomb failure surface commonly adopted. The $M$ value is therefore should be determined based on the stress state. In the following numerical experiments as the only consolidation analyses are concerned, we will use $\frac{6\sin(\varphi)}{3+\sin(\varphi)}$.

$$
\begin{equation}[label@eq_MMCC]
M =
\begin{cases}
\frac{6 \sin \varphi}{3 - \sin \varphi} & \text{(for initial compression stress states)} \quad (\sigma_1' < \sigma_2' = \sigma_3') \\
\frac{6 \sin \varphi}{3 + \sin \varphi} & \text{(for initial compression stress states)} \quad (\sigma_1' = \sigma_2' \leq \sigma_3') \\
\sqrt{3} \sin \varphi & \text{(for plane strain stress states)}
\end{cases}
\end{equation}
$$

![Drucker-Prager vs Mohr Columb \label{f_DP_VS_MD}](image/DP_VS_MC_yield_surface.png){width=450}

### Soft Soil Model

The Soft Soil model was inspired by the Modified Camclay model with a few modification or improvements. It is not clear from the Plaxis material manual who first proposed such modification to the MCC model. From the formulation, it appears that Soft Soil Model is better version of the MCC and should supersede the MCC model.

### Hardening Soil Model (HS)

Hardening Soil Model was developed by @Schanz1999 and this model is widely used for both clay and sand. Soft soils can be analyzed with the HS; however, the hardening soil models are not suitable for very soft soil with high compressibility, i.e., $E_{oed}^{ref}/E_{50}^{ref}<0.5$

> @Plaxis2021Mat[p.113] "From the above considerations it would seem that the Hardening Soil model is quite suitable for soft soils. Indeed, most soft soil problems can be analysed using this model, but the Hardening Soil model is not suitable when considering very soft soils with a high compressibility, i.e $E_{oed}^{ref} / E_{50}^{ref} < 0.5$. For such soils, the Soft Soil model may be used."

### Soft Soil Creep Model

Soft Soil Creep Model was developed by @Vermeer1998. The most significant feature of this model is that it can consider creep of the clay, i.e., commonly known as the secondary compression. There is ongoing debate on the uniqueness of the end-of-primary void ratio, two different side of supporter on this issue for Hypothesis A and Hypothesis B.

The use of this model will yield larger settlement given fed with the same set of parameters as in SS and HS model and settlement will continue to increase after the end of the primarily consolidation. This model provide a very handy tool for analysing the problem. The implementation of this model is considered a rigorous Hypothesis B model.

It is commented that this model is very sensitive to the specified OCR and can lead to significant amount of the creep settlement from model and is not recommended by @Karstunen2017 for engineers.

## Comparison of the Predictive Capabilities of the Advanced Constitutive Models

In this section, we aim to evaluate the predictive capabilities of the available soil models listed in **Table \ref{t_soil_model}** in terms of consolidation analyses. Reclamation design is customarily conducted under the assumption of one-dimensional (1D) consolidation theory, applying Terzaghi's consolidation theory [@Terzaghi1943] or Barron's theory [@barron1948consolidation] when vertical drains are introduced. In the following numerical experiments, a series of unit cell models will be conducted with identical configurations and soil properties. Four different soil models relevant to consolidation analysis will be employed to demonstrate differences in both predicted total settlement and associated time rates. The calculated results will then be compared to those from the 1D consolidation theory recommended in the Port Work Design Manual Part 3 [@CEO2002].

It should be noted that the total magnitude of consolidation is relatively less uncertain than the consolidation rate, which is subject to numerous difficult-to-quantify factors such as smear effect and well resistance.


![Axisymetric Plaxis Model \label{f_plaxi_model}](image/mode_set_up_Layer%201_copy_1.pdf){width=250}

### 1D Consolidation Solution

$$
\begin{equation}[label@eq_]
S(t) = S_{\infty} \cdot U
\end{equation}
$$

where:

- $S_{\infty}$ = the ultimate consolidation settlement, and
- $U$ = degree of consolidation

To simplify the comparison, we will only consider the horizontal drainage. The average degree of consolidation can be expressed as Eq.(\ref{eq_doc_h}).

$$
\begin{equation}[label@eq_doc_h]
U =  1 - e^{\left(-\frac{8c_ht}{D^2 F(n)}\right)}
\end{equation}
$$

$$
\begin{equation}
s_i = \frac{C_c}{1+e_0} \cdot \log\bigg(\frac{\sigma'_{vi} + \Delta\sigma_v}{\sigma'_{vi}}\bigg)
\end{equation}
$$

For the normally consolidated clay with OCR of 1.0, the initial effective stress can be calculated as $\sigma'_{vi} = z \cdot \gamma$ and therefore the total ultimate consolidation settlement for a given thickness $H$ of MD can be calculated as in Eq.(\ref{eq_stotal}).

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
S_{\infty}(20\text{kPa}) &= \frac{ C_{c} }{ 1 + e_{0} } \cdot \left( H \cdot \log_{10} \left( \frac{ q + \gamma \cdot H }{ \gamma \cdot H } \right) - \frac{ q }{ \gamma } \cdot \log_{10} \left( q \right) + \frac{ q }{ \gamma } \cdot \log_{10} \left( q + \gamma \cdot H \right) \right) \\&= \frac{ 1.20 }{ 1 + 2.00 } \cdot \left( 10 \cdot \log_{10} \left( \frac{ 20 + 6.00 \cdot 10 }{ 6.00 \cdot 10 } \right) - \frac{ 20 }{ 6.00 } \cdot \log_{10} \left( 20 \right) + \frac{ 20 }{ 6.00 } \cdot \log_{10} \left( 20 + 6.00 \cdot 10 \right) \right) \\&= 1.30  \\[8pt]
\end{aligned}
\end{equation}
$$

$$
\begin{equation}[label@eq_OCR1_200]
\begin{aligned}
q &= 200 \;
\\[8pt]
S_{\infty}(\text{200kPa}) &= \frac{ C_{c} }{ 1 + e_{0} } \cdot \left( H \cdot \log_{10} \left( \frac{ q + \gamma \cdot H }{ \gamma \cdot H } \right) - \frac{ q }{ \gamma } \cdot \log_{10} \left( q \right) + \frac{ q }{ \gamma } \cdot \log_{10} \left( q + \gamma \cdot H \right) \right) \\&= \frac{ 1.20 }{ 1 + 2.00 } \cdot \left( 10 \cdot \log_{10} \left( \frac{ 200 + 6.00 \cdot 10 }{ 6.00 \cdot 10 } \right) - \frac{ 200 }{ 6.00 } \cdot \log_{10} \left( 200 \right) + \frac{ 200 }{ 6.00 } \cdot \log_{10} \left( 200 + 6.00 \cdot 10 \right) \right) \\&= 4.07  \\[8pt]
\end{aligned}
\end{equation}
$$

Table:Ultimate Consolidation Settlement for OCR=2.0, H=10m (1D) \label{t_s_OCR2_H10}

| surcharge loading | OCR | Settlement | Remarks                     |
| ----------------: | --: | ---------: | --------------------------- |
|               kPa |   - |          m | -                           |
|                20 | 1.0 |       1.30 | Eq.(\ref{eq_OCR1_20})       |
|               200 | 1.0 |       4.07 | Eq.(\ref{eq_OCR1_200})      |
|                20 | 2.0 |       0.53 | Calculated with spreadsheet |
|               200 | 2.0 |       3.14 | Calculated with spreadsheet |

## Consolidation without Void Ratio Dependency

The input parameters consistent among the soil models and presented in **Appendix C**. The horizontal permeability is set to achieve a $c_h = 1.2m^2\text{year}$. In this series of numerical assessment, the permeability was kept unchanged.

![Settlement Curve for Various Soil Models \label{f_settlement_const_k}](image/OCR_1_ck_no_activate.pdf){width=650}

**Figure \ref{f_settlement_const_k}** illustrates the settlement behaviour of a 10-m thick marine deposit under two different stress levels, as modelled using various soil models. The Hardening Soil and Soft Soil models exhibit similar predictive capabilities, closely aligning with the theoretical 1D consolidation results for the ultimate settlement. This indicates their effectiveness in capturing total settlement behaviour against 1D consolidation theory. In contrast, the Modified Cam Clay model shows a greater total settlement compared to the 1D consolidation theory, suggesting a tendency to overestimate settlement (**DONT KNOW WHY**). The Soft Soil Creep model, as expected, predicts a linear increase (in logarithmic scale) in settlement after the consolidation phase, reflecting the ongoing deformation due to creep.

In term of the predicted rate of settlement, at a lower stress level of 20kPa, a good agreement can be observed; however, when subjected to larger stress level of 200kPa, the numerical modelling assuming constant permeability tends to consolidation much faster compared with Barron's solution.

This can be better illustrated by plotting the data in terms of degree of consolidation in **Figure \ref{f_doc_change_k}**. In the figure, the degree of consolidation by Barron's solution for different stress level overlap and it is clear that the black lines (200kPa) are much earlier than the blue lines(20kPa).

![Degree of Consolidation for Various Soil Model (Constant Permeability) \label{f_doc_const_k}](image/DOC_OCR_1_ck_no_activate.pdf){width=650}

## Consolidation with Void Ratio Dependency

In this section, we will explain the cause of this phenomenon and further considerations necessary to make the numerical modelling consistent with classic Terzaghi's consolidation theory.

In Terzaghi and Barron's solution, the degree of consolidation at any time t is governed by a coefficient of consolidation, defined in Eq.(\ref{eq_ch}). This reflects the two factors that contribute to consolidation - $E_oed$, the constrained modulus, and $k$, the permeability of the material.

$$
\begin{equation}[label@eq_ch]
c_h = \frac{E_{oed\cdot k}}{\gamma_w}
\end{equation}
$$

$$
\begin{equation}[label@eq_Eoed]
E_{oed} = \frac{\sigma_v'}{\lambda^*} = \ln(10) \cdot \frac{1+e_0}{C_c} \cdot \sigma_v'
\end{equation}
$$

![Typical Stress Strain Relationship for Soft Soil \label{f_stress_strain}](image/stress_stain_soft_soil.pdf){width=300}

As shown in **Figure \ref{f_stress_strain}**, as the soil consolidates, it gets stiffer with an increased compression modulus denoted as $E_{oed}$, and it can be expressed as Eq.(\ref{eq_Eoed}). If we maintain the permeability constant, according Eq.(\ref{eq_ch}), the coefficient will increase during the consolidation with an increased effective vertical stress.

In Terzaghi's classic solution, the coefficient of consolidation is assumed to remain constant throughout the entire consolidation process. This simplifying assumption allowed Terzaghi to obtain a solution to the governing partial differential equations. To maintain consistency with Terzaghi's conceptual model, wherein the coefficient remains unchanged over time, the numerical modeling must likewise satisfy $c_{h,0} = c_{h,1}$. In other words, the coefficient of consolidation calculated at any two points in time during the consolidation process must be equal. This constraint is necessary to achieve solutions that align with Terzaghi's theory, in which consolidation is modeled as a linear, time-dependent process governed by a fixed coefficient.

$$
\begin{equation}[label@eq_k_stress]
c_{h,0} = c_{h,1} \Rightarrow \frac{E_{oed,0} \cdot k_0}{\gamma_w} = \frac{E_{oed,1} \cdot k_1}{\gamma_w} \Rightarrow \log\bigg(\frac{k_1}{k_0}\bigg) = \log\bigg(\frac{\sigma_1}{\sigma_0}\bigg)
\end{equation}
$$

In the case of typical soft clay, it is often observed that the virgin compression line exhibits a nearly linear relationship in an $e-\log\sigma'$ space, with a slope defined as the compression index $C_c$, as shown in Eq.(\ref{eq_delta_e}). By substituting Eq.(\ref{eq_delta_e}) into Eq.(\ref{eq_k_stress}), we obtain Eq.(\ref{eq_k_change}). This relationship holds true when we make the same assumption as classical soil mechanics, namely that the coefficient of consolidation remains constant during consolidation.

The assumption of a constant coefficient of consolidation is reasonable due to the opposing effects of increasing stiffness and decreasing permeability as the void ratio decreases. These effects tend to balance each other out. However, it is important to note that this assumption was initially made to simplify the solution of the system.

In the Plaxis, a generic term $c_k$ is adopted instead of $c_c$ in Eq.(\ref{eq_k_change}) as this void ratio dependency was meant for a more general purpose. Typically, for consolidation of soft clay, detailed permeability measurements are rarely conducted in practical applications. Therefore, it is recommended to enable this advanced function in order to ensure consistency with conventional assumptions, despite the limited availability of comprehensive permeability data.

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

![Settlement of Curve for Various Soil Model (with void ratio dependency) \label{f_settlement_k_vary}](image/OCR_1_ck_activate.pdf){width=650}

![Degree of Consolidation for Various Soil Model (with void ratio dependency) \label{f_doc_k_vary}](image/DOC_OCR_1_ck_activate.pdf){width=650}

## Initial Stiffness and Convergence Analysis

In the preceding sections, we have demonstrated that it is necessary to update the permeability in order to remain consistent with the classical consolidation theory wherein the coefficient of consolidation is assumed to remain constant throughout the entire consolidation process. In this section, we will conduct further investigation into how to appropriately specify the permeability parameter, an issue that has yet to be addressed.

In the initial design phase, the coefficient of consolidation is typically used and often this value is based on back-calculated data from previous, similar projects. Based on experience from a recent reclamation project, a lumped $c_h = 1.2\;m^2/\text{year}$ is considered appropriate. This lumped parameter is intended to already account for effects like soil smear and well resistance that are typically difficult to quantify with full accuracy during the initial design stage.

The results presented so far are based on a single layer the permeability is back-calculated at the mid point of the soil layer (refer to **Appendix A** for an example of 2.5m). We will further divide the soil layers in to smaller segments and specify the permeability at different levels (as shown in **Figure \ref{f_soil_segment}**), in such a way, the calculated results will theoretically approach a constant $c_h$ assumption. In this exercise, Hardening Soil Model will be used.

![Soil Segments \label{f_soil_segment}](image/soi_segment.pdf){width=450}

![Settlement vs Soil Segments (Hardening Soil Model) \label{f_convergency}](image/convergency.pdf){width=650}

## Parameters in Hardening Soil Model {#HS_Parm}

We have demonstrated that the hardening soil model, which represents the latest attempt to improve predictive performance over the established Modified Camclay model and as an extension of soft soil models. In this section, we discuss the input parameters and how design parameters can be approximated for Hardening Soil Model. 

In Hardening soil model, it is assumed that the stiffness varies with the stress level as shown in Eq.(\ref{eq_oed}), Eq.(\ref{eq_E50}) and Eq.(\ref{eq_Eur})

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

**$m$**

m =1 is a good estimate of the most of the soft soils and such assumption is consistent with the conventional assumption on consolidation assessment, please see Eq.(\ref{eq_eq_Eoed}), where we've already implicitly assumed $m=1$, i.e., the compression curve is linear in $e-\log\sigma$ space.

**i$E_{oed}$**

$E_{oed}^[ref]$ can be determined using Eq.(\ref{eq_oed}) by relating to compression index $C_c$ and as shown in **Table \ref{t_typical_value}**, the compression index of MD vary within a relatively narrow range and in a order of 1.0 for recent reclamation projects.

\blandscape

Table:Some Properties of Marine Mud[@Kwong1997, p.30]\label{t_typical_value}

| Reference              | Premchitt & Shaw (1991) | Foott et al (1987) | Premchitt et al (1990)   | Lumb (1977) | Bramall & Raybould (1993) | Scott Wilson Kirkpatrick & Partners (1987) | Mott MacDonald et al (1991) | Maunsell Geotechnical Services Ltd. (1995) | Maunsell Geotechnical Services Ltd. (1995) | Hunt et al (1982) | Carter (1996) |
| ---------------------- | ----------------------- | ------------------ | ------------------------ | ----------- | ------------------------- | ------------------------------------------ | --------------------------- | ------------------------------------------ | ------------------------------------------ | ----------------- | ------------- |
| Site                   | CLK                     | CLK                | CLK                      | LCK         | LCK                       | LCK                                        | TC                          | NLE                                        | CT10/CT11                                  | CPB               | Macau         |
| PI (%)                 | 50                      | 45-65              | 30-70                    | 30          | 24-35                     | 29                                         | 20-60                       | 41-42                                      | 40                                         | 20-40             | 30-40         |
| LL (%)                 | -                       | 70-100             | 55-95                    | 58          | 45-74                     | 57                                         | 60-80                       | 72-84                                      | 74                                         | 45-70             | 60-75         |
| $C_v$ (m²/yr)          | 1.5                     | 1.3                | 1.5                      | 0.3-3.2     | 0.7-2.4                   | 1.07                                       | 2.0                         | 1.2                                        | 1.0                                        | 2.0               | 1.8-2.6       |
| $k$ (m/s)              | $1.0 \times 10^{-7}$    | -                  | $0.1-1.0 \times 10^{-8}$ | -           | $1.2-3.2 \times 10^{-10}$ | $1.0 \times 10^{-9}$                       | $0.96-3.2 \times 10^{-9}$   | -                                          | -                                          | -                 | -             |
| $e_0$ (@ $p_0'$ =1kPa) | -                       | -                  | 2.3                      | 1.9         | 2.2-2.6                   | 2.3                                        | 1.5-2.0                     | -                                          | -                                          | 1.0-2.3           | 1.8-2.0       |
| $C_c$                  | 1.0                     | 0.4                | 1.0                      | -           | 0.5-0.8                   | 0.7                                        | 0.5-0.9                     | -                                          | -                                          | 0.5-0.8           | 0.6-0.7       |
| Nat. mc (%)            | up to 100               | >100               | 100                      | -           | 24-97                     | 68                                         | 60-90                       | 70-83                                      | 88                                         | 50-90             | 60-75         |
| Density (kN/m³)        | 15                      | -                  | 13-17                    | -           | 14-20                     | 16                                         | -                           | 15.7-16                                    | 15.6                                       | 8-11              | 15.5-16.5     |
| $C_R$                  | -                       | 0.4                | 0.3                      | -           | -                         | -                                          | 0.2-0.3                     | -                                          | -                                          | -                 | -             |
| $c'$ (kPa)             | -                       | -                  | 0                        | -           | -                         | -                                          | 2.5                         | -                                          | -                                          | 0                 | -             |
| $\phi'$ (deg)          | -                       | -                  | 28                       | -           | -                         | 29                                         | -                           | -                                          | -                                          | 19-30             | -             |

**Notes:**

- CLK - Chek Lap Kok
- LCK - Lai Chi Kok
- TC - Tung Chung
- NLE - North Lantau Expressway
- CT10/
- CT10/CT11 - Container Terminals 10 & 11
- CPB - Castle Peak Bay

\elandscape

## Soil Structure Interaction and DCM

In this Section, a plane strain model will be used to study the load shearing of the shear wall, and the particular focus is made on the load shearing between the DCM columns and the tributary soils and the stress concentration variation against time. 

Given the typical column width of 0.6m and spacing of 1.2m, the unit model at the area can be shown in Figure XXX. Hardening soil model will be adopted for MD and Mohr Column soil models is used for DCM columns. It is assumed that the stone columns are linear elastic and not subjected to consolidation process.

-[] to do

# Remarks on Soil Models on Consolidation Analysis

The following conclusions can be drawn from these numerical experiments:

1. The Soft Soil model and Hardening Soil model demonstrate comparable predictive capabilities for consolidation analyses. Both models can produce results similar to conventional one-dimensional (1D) consolidation theory commonly applied in previous reclamation projects. 

2. The Modified Cam Clay model, implemented in Plaxis as an educational tool with a Drucker-Prager failure criterion, is not recommended for practical application. Its predictions of consolidation seems do not agree well from 1D theory, warranting further investigation[^2].

3. The Soft Soil Creep model can capture secondary compression of soft soils if deemed desirable. 

4. For accurate consolidation analyses, advanced soil models should incorporate permeability dependent on void ratio, consistent with the assumptions of classical consolidation theory.

[^2]: This does not seem to be reasonable, need to interrogate the input

\pagebreak

\setcounter{equation}{0}
\renewcommand{\theequation}{A.\arabic{equation}}

# Appendix A - Example of Derivation of Soil Permeability {-}

The determination of soil permeability is known to have high uncertainties. We will assume that the coefficient of consolidation is known, as it is typically back-calculated from field observations. In the recent reclamation project, a value of $c_h = c_v = 1.2 , \text{m}^2/\text{year}$ was adopted and found to fit the monitoring data well.

**Example: Permeability at 2.5m below the seabed level**

$$
\begin{equation}[label@eq_]
\sigma_v' = \gamma'\cdot H = 6\cdot 2.5 = 15 \text{kPa}
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
C_h = \frac{E_{eod} \cdot k_h}{\gamma_w}
\end{equation}
$$

$$
\begin{equation}
\Rightarrow k_h = \frac{\gamma_w \cdot C_h}{E_{eod}}
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

\pagebreak

\setcounter{equation}{0}
\renewcommand{\theequation}{B.\arabic{equation}}

# Appendix B - Hardening Soil Parameters{-}

## Hardening Soils for Clay

For clay modeled with Hardening Soil model, the $E_{oed}^{ref}$ should be easily determined using Eq.(\ref{eq_Eoed}).

**$E_{50}^{ref}$**

In the absence of triaxial data for $E_{50}$, the stiffness of soft soils can be estimated using empirical relations. The undrained elastic modulus of clay is commonly taken as $E_u = 300\cdot s_u$, which seems to be widely accepted in industry based on early work by Jamiolkowski (1981).

The undrained shear strength of soft clay can be estimated using the concept of Stress History And Normalised Engineering Properties (SHANSEP), where the undrained strength of over-consolidated clay can be correlated to that of normally consolidated clay using the relationship in Eq.(\ref{eq_su_shansep}).

$$
\begin{equation}[label@eq_su_shansep]
S_u = S \cdot OCR^m \cdot \sigma'_{\text{v}}
\end{equation}
$$

Typically, for a normally consolidated clay, 0.22 can be adopted for a quick assessment.

$$
\begin{equation}
S_u = 0.22 \cdot \sigma'_{\text{v}}
\end{equation}
$$

$$
\begin{equation}
E_u = 300 \cdot S_u = 300 \cdot (0.22 \cdot \sigma'_{\text{v}}) = 66 \cdot \sigma'_{\text{v}}
\end{equation}
$$

In Plaxis, the input parameter for Hardening Soils are effective stiffness, we know that the stiffness of shear modulus for drained and undrained should be equal, as water does not take shear stress.

$$
\begin{equation}
G' = G_u \Leftrightarrow \frac{E'}{2(1+\nu)} = \frac{E_u}{2(1+\nu_u)}
\end{equation}
$$

$$
\begin{equation}
\nu_u = 0.5 \quad \Rightarrow \quad E' = \frac{2(1+\nu')}{3} E_u \Rightarrow \quad E' \approx 0.8 \cdot E_u
\end{equation}
$$

In addition, the reference stress for $E_{50}^{ref}$ and $E_{oed}^{ref}$ refer to $\sigma'_3$, i.e., the confining pressure during the triaxial testing, we will need to work out the relationship with $\sigma_h'$

$$
\begin{equation}
\sigma'_{\text{h}} = k_0 \cdot \sigma'_{\text{v}} \quad \Rightarrow \quad \sigma'_{\text{v}} = \frac{1}{k_0} \cdot \sigma'_{\text{h}}
\end{equation}
$$

$$
\begin{equation}
E_{50} = \frac{2}{3} \cdot (1+\nu') \cdot 66 \cdot \frac{1}{k_0} \cdot \sigma'_{\text{h}}
\end{equation}
$$

$$
\begin{equation}
E_{50} = 44 \cdot (1+\nu') \cdot \frac{1}{k_0} \cdot \sigma'_{\text{h}}
\end{equation}
$$

**Example:**

$$
\begin{equation}
\sigma'_{\text{ref}} = 100 \, \text{kPa}, \quad k_0 = 1 - \sin 26^\circ = 0.56, \quad \nu' = 0.2
\end{equation}
$$

$$
\begin{equation}
E_{50}^{ref} = 44 \cdot (1 + 0.2) \cdot \frac{1}{0.56} \cdot 100 = 9428\, \text{kPa}
\end{equation}
$$

$$
\begin{equation}
E_{50}^{ref}= 9.428\text{MPa} \, \text{MPa}
\end{equation}
$$

It should be noted that $E_{50}^{ref}$ such determined only serve as the starting point for trial, triaxial testing should be performed in Plaxis and corresponding undrained stiffness E*{50}^{u} should be check to ensure this agree with what is assumed and the specified $E*{50}^{ref}$ can yield the targeted undrained stiffness.

**Verifying the criterion $E_{oed}^{ref} /E_{50}^{ref}> 0.5$**

$$
\begin{equation}
E_{\text{oed}} = \frac{\sigma}{\epsilon}
\end{equation}
$$

$$
\begin{equation}
E_{\text{oed}}^{\text{ref}} = \ln 10 \frac{1 + e_0}{C_c} \cdot \sigma_v
\end{equation}
$$

$$
\begin{equation}
E_{\text{oed}}^{\text{ref}} = 2.3 \times \frac{1 + 2.0}{1.0} \times 0.100
\end{equation}
$$

$$
\begin{equation}
E_{\text{oed}}^{\text{ref}} = 0.69 \, \text{MPa}
\end{equation}
$$

$$
\begin{equation}
\frac{E_{\text{oed}}^{\text{ref}}}{E_{50}^{\text{ref}}} = \frac{0.69}{9.428} = 0.073 < 0.5 \, \text{(Plaxis p.110)}
\end{equation}
$$

Therefore, for in-situ marine deposits, Soft Soils seem to be recommended according to Plaxis for analyzing in-situ marine deposit in Hong Kong, characterized by normally/slightly overconsoldiated silty clay. However, as we have demonstrated in the main text of this Note that regarding performance in consolidation prediction, the Hardening Soil model has comparable prediction capacity as Soft Soil. **We've used Hardening Soil Model for MD in offshore wind farm design**.

## Appendix B2 - $E_{ur}^{ref}$ {-}

The $E_{ur}^{ref}$ refer to the triaxial unloading reloading stiffness at the reference stress and this can be correlated with the $C_s$.

> According to @Yin1999[p.1901] "The ratios of $C_r$ to $C_c$ and $C_{\alpha}$ to $C_c$ on average for HKMD-1 are 0.114 and 0.026, respectively. The ratios on average for the upper marine clay are $C_r / C_c = 0.157$ and $C_{\alpha} / C_c = 0.022$ (Koutsoftas et al. 1987). Mesri and Godlewski (1977) summarized the range of $C_{\alpha} / C_c$ values for a number of clays published in the literature and found that they range from 0.025 to 0.075 for inorganic clays and silts and 0.03 to 0.085 for organic clays, silts, and peat. Nakase et al. (1988) reported $C_{\alpha} / C_c = 0.032$ almost constant for $I_p = 10-60\%$ and $C_r / C_c = 0.144$ on average for both Kawasaki clay (mixture series) and reconstituted natural marine clay. By comparison, the values of $C_r / C_c = 0.114$ and $C_{\alpha} / C_c = 0.026$ for HKMD-1 are close to those reported by Koutsoftas et al. (1987) and Nakase et al. The average value of $C_{\alpha} / C_c = 0.026$ for HKMD-1 is near the lower bound of the range of values 0.025-0.075 reported by Mesri and Godlewski (1977) for inorganic clays. The $C_{\alpha} / C_c$ value for HKMD-1 is near the lower bound because HKMD-1 is not all clay but has a sand content of from 14.1\% (C4) to 80\% (C1). The $C_{\alpha} / C_c$ value normally decreases with an increase in sand content."

\pagebreak

\setcounter{table}{0}
\renewcommand{\thetable}{C.\arabic{table}}

# Appendix C - Plaxis Input Parameters{-}

**Table \ref{t_C_input}** summarizes the adopted design parameters used for the numerical experiments presented in this Note. It should be noted the scenario with $OCR=2$ has also been tested and similar findings were observed.

Table:Summary of Plaxis Input Parameters \label{t_C_input}

| **Parameter**             | **Cam Clay** | **Soft Soil** | **Soft Soil Creep** | **Hardening Soil** |
| ------------------------- | -----------: | ------------: | ------------------: | -----------------: |
| **Physical Properties**   |              |               |                     |                    |
| $\gamma_{\text{unsat}}$   |           16 |            16 |                  16 |                 16 |
| $\gamma_{\text{sat}}$     |           16 |            16 |                  16 |                 16 |
| $e_{\text{init}}$         |          2.0 |           2.0 |                 2.0 |                2.0 |
| $K_0$ Determination       |    Automatic |     Automatic |           Automatic |          Automatic |
| **Mechanical Properties** |              |               |                     |                    |
| $\lambda$                 |        0.521 |             - |                   - |                  - |
| $\kappa$                  |       0.0651 |             - |                   - |                  - |
| $\nu_{\text{UR}}$         |         0.25 |          0.25 |                0.25 |               0.25 |
| $M$                       |        0.984 |             - |                   - |                  - |
| Use Alternatives          |        False |          True |                True |               True |
| $C_c$                     |            - |           1.2 |                 1.2 |                1.2 |
| $C_s$                     |            - |         0.149 |               0.149 |              0.149 |
| $C_{\alpha}$              |            - |             - |                0.05 |                  - |
| OCR                       |            1 |             1 |                   1 |                  1 |
| **Strength Parameters**   |              |               |                     |                    |
| $c_{\text{ref}}$          |         0.01 |          0.01 |                0.01 |               0.01 |
| $\psi$                    |          0.0 |           0.0 |                 0.0 |                0.0 |
| $\phi$                    |           25 |            25 |                  25 |                 25 |
| $R_{\text{inter}}$        |         0.75 |          0.75 |                0.75 |               0.75 |
| **Permeability**[^1]      |              |               |                     |                    |
| Void Ratio Dependency     |         True |          True |                True |               True |
| $C_k$                     |          1.2 |           1.2 |                 1.2 |                1.2 |
| **Additional Properties** |              |               |                     |                    |
| Drainage Type             |  Undrained A |   Undrained A |         Undrained A |        Undrained A |
| Tension Cut-Off           |         True |          True |                True |               True |

[^1]: Horizontal Permeability is calculated to achieve $c_h = 1.2\text{m}^2/\text{year}$, refer to **Appendix A**

\pagebreak

\setcounter{table}{0}
\renewcommand{\thetable}{D.\arabic{table}}

# Appendix D - Recommended Design Parameters for Stability Analyses{-}

In the absence of site-specific test data, design parameters from **Table \ref{t_D_input}** can be used as a preliminary reference for initial design work; however, it should be noted the alluvium can be highly variable and underlying soft clay may also be present. Adequate geotechnical investigation data, particularly CPT data, should be reviewed to better inform and assist in the final design.

Table:Typical Design Parameters \label{t_D_input}

| **Materials**    | **$\gamma_{sat}$** | **$c'$** |  **$\phi'$** |              **$s_u$** |                       **$E$** |
| ---------------- | -----------------: | -------: | -----------: | ---------------------: | ----------------------------: |
|                  |             [unit] |    [kPa] |     [Degree] |                  [kPa] |                         [kPa] |
| Fill             |                 19 |        0 |           32 |                    n/a |          $10,000 \sim 15,000$ |
| Rock Fill        |                 20 |        0 |           42 |                    n/a |          $40,000 \sim 50,000$ |
| Deep-mixed Soils |                 16 |      n/a |          n/a |                    500 | $(100 \sim 300) \text{UCS}^*$ |
| Marine Deposit   |                 16 |        0 |           25 | $0.22 \cdot \sigma_v'$ |        $300 \cdot s_u^\wedge$ |
| Alluvial Clay    |                 18 |        0 |           28 |                  40~70 |        $300 \cdot s_u^\wedge$ |
| Alluvial Sand    |                 19 |        0 | $32 \sim 36$ |                    n/a |          $40,000 \sim 50,000$ |

**Note:**

- $^\wedge$: Typical assumption, following @Jamiolkowski1981.
- $^*$: Recommendation from @FHADM2013, 100 for dry and 300UCS for wet mixing

\pagebreak

# Reference {-}
