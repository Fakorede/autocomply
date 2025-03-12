# RQ 3: Applicability

> Can CarCompat be applied to real-world apps and find issues?

To evaluate the applicability of CarCompat, we analyzed its performance on two datasets: Corpus-G, consisting of open-source Android Auto apps, and Corpus-P, comprising proprietary commercial apps.

This directory contains the complete results of our evaluation of `CarCompat` on all apps in **Corpus-G**.

Apps in Corpus-G are made available in the `/apks` folder [here](/apks/).

Apps in Corpus-P are unavailble due to Google's distribution policy.


### Comparison of CarCompat's performance on open-source and commercial Android Auto applications

|  CarCompat Evaluation Metrics | Corpus-G | Corpus-P |
|---|---|---|
| \# of Apks | 44 | 13 |
| \# of Apps w Issues | 15| 2 |
| \# of Issues Detected | 27 | 4 |
| GeoMean Time(s) | 5.6 | 7.2 |
| LoC  | 6.5m  | -  |


## Answer

CarCompat is applicable to both open-source and commercial Android Auto apps, detecting compatibility issues efficiently. Its scalability allows analysis across diverse codebases, enabling early issue detection and compliance with platform requirements.



