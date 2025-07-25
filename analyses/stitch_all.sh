module load python
conda activate flamedisx

## SI WIMP
## LNGS
python3 stitch.py -d SI_WIMP_sensitivity/outputs/SI_WIMP_60t_100ty_LNGS
python3 stitch.py -d SI_WIMP_sensitivity/outputs/SI_WIMP_60t_300ty_LNGS
python3 stitch.py -d SI_WIMP_sensitivity/outputs/SI_WIMP_60t_600ty_LNGS
python3 stitch.py -d SI_WIMP_sensitivity/outputs/SI_WIMP_60t_1000ty_LNGS

## O6 (scalar) NREFT WIMP
## LNGS
python3 stitch.py -d EFT_O6_s_WIMP_sensitivity/outputs/EFT_O6_s_WIMP_60t_100ty_LNGS
python3 stitch.py -d EFT_O6_s_WIMP_sensitivity/outputs/EFT_O6_s_WIMP_60t_300ty_LNGS
python3 stitch.py -d EFT_O6_s_WIMP_sensitivity/outputs/EFT_O6_s_WIMP_60t_600ty_LNGS
python3 stitch.py -d EFT_O6_s_WIMP_sensitivity/outputs/EFT_O6_s_WIMP_60t_1000ty_LNGS

## ALP
python3 stitch.py -d ALP_sensitivity/outputs/ALP_60t_100ty
python3 stitch.py -d ALP_sensitivity/outputs/ALP_60t_300ty
python3 stitch.py -d ALP_sensitivity/outputs/ALP_60t_600ty
python3 stitch.py -d ALP_sensitivity/outputs/ALP_60t_1000ty

## HP
python3 stitch.py -d HP_sensitivity/outputs/HP_60t_100ty
python3 stitch.py -d HP_sensitivity/outputs/HP_60t_300ty
python3 stitch.py -d HP_sensitivity/outputs/HP_60t_600ty
python3 stitch.py -d HP_sensitivity/outputs/HP_60t_1000ty
