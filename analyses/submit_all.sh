module load python
conda activate flamedisx

# ## SI WIMP
cd SI_WIMP_sensitivity
## LNGS
source run_analysis.sh default_60t_100ty_LNGS.ini ../v2.1_nominal_SI_WIMP.pkl default_LNGS.ini SI_WIMP_60t_100ty_LNGS SLURM
source run_analysis.sh default_60t_300ty_LNGS.ini ../v2.1_nominal_SI_WIMP.pkl default_LNGS.ini SI_WIMP_60t_300ty_LNGS SLURM
source run_analysis.sh default_60t_600ty_LNGS.ini ../v2.1_nominal_SI_WIMP.pkl default_LNGS.ini SI_WIMP_60t_600ty_LNGS SLURM
source run_analysis.sh default_60t_1000ty_LNGS.ini ../v2.1_nominal_SI_WIMP.pkl default_LNGS.ini SI_WIMP_60t_1000ty_LNGS SLURM
cd ..

## O6 (scalar) NREFT WIMP
cd EFT_O6_s_WIMP_sensitivity
## LNGS
source run_analysis.sh default_60t_100ty_LNGS.ini ../v2.1_nominal_EFT_O6_s_WIMP.pkl default_LNGS.ini EFT_O6_s_WIMP_60t_100ty_LNGS SLURM
source run_analysis.sh default_60t_300ty_LNGS.ini ../v2.1_nominal_EFT_O6_s_WIMP.pkl default_LNGS.ini EFT_O6_s_WIMP_60t_300ty_LNGS SLURM
source run_analysis.sh default_60t_600ty_LNGS.ini ../v2.1_nominal_EFT_O6_s_WIMP.pkl default_LNGS.ini EFT_O6_s_WIMP_60t_600ty_LNGS SLURM
source run_analysis.sh default_60t_1000ty_LNGS.ini ../v2.1_nominal_EFT_O6_s_WIMP.pkl default_LNGS.ini EFT_O6_s_WIMP_60t_1000ty_LNGS SLURM
cd ..

## ALP
cd ALP_sensitivity
source run_analysis.sh default_60t_100ty.ini ../v2.1_nominal_ALP.pkl default.ini ALP_60t_100ty SLURM
source run_analysis.sh default_60t_300ty.ini ../v2.1_nominal_ALP.pkl default.ini ALP_60t_300ty SLURM
source run_analysis.sh default_60t_600ty.ini ../v2.1_nominal_ALP.pkl default.ini ALP_60t_600ty SLURM
source run_analysis.sh default_60t_1000ty.ini ../v2.1_nominal_ALP.pkl default.ini ALP_60t_1000ty SLURM
cd ..

## HP
cd HP_sensitivity
source run_analysis.sh default_60t_100ty.ini ../v2.1_nominal_HP.pkl default.ini HP_60t_100ty SLURM
source run_analysis.sh default_60t_300ty.ini ../v2.1_nominal_HP.pkl default.ini HP_60t_300ty SLURM
source run_analysis.sh default_60t_600ty.ini ../v2.1_nominal_HP.pkl default.ini HP_60t_600ty SLURM
source run_analysis.sh default_60t_1000ty.ini ../v2.1_nominal_HP.pkl default.ini HP_60t_1000ty SLURM
cd ..