# RQ 3: Applicability

> Can CarCompat be applied to real-world apps and find issues?

To evaluate the applicability of CarCompat, we applied it to [Corpus-G](https://anonymous.4open.science/r/carcompat-0503/RQs/RQ3/Corpus-G.csv), a dataset of 44 open-source Android Auto apps spanning diverse categories and development practices. 
The objective was to assess whether CarCompat could effectively detect compatibility issues across various real-world apps and remain computationally efficient for large-scale analysis.

This directory contains the complete results of our evaluation of `CarCompat` on all apps in **Corpus-G**.

Apps in Corpus-G are made available in the `/apks` folder [here](https://anonymous.4open.science/r/carcompat-0503/apks/).


**Table: CarCompat's performance on open-source Android Auto applications in *Corpus-G***

|  CarCompat Evaluation Metrics | Corpus-G |
|---|---|
| \# of Apks | 44 |
| \# of Apps w Issues | 15|
| \# of Issues Detected | 27 |
| GeoMean Time(s) | 5.6 |
| LoC  | 6.5m  |


## Answer

CarCompat is applicable to real-world Android Auto apps and achieves low runtime, enabling efficient detection of compatibility issues in real-world Android Auto apps. Its scalability makes it a practical tool for identifying and addressing compatibility challenges across diverse codebases.



