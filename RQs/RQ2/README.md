# RQ 3: Effectiveness

> Can AutoComply effectively and precisely detect Android Auto compliance issues in real-world apps?

To evaluate the effectiveness of AutoComply, we applied it to [Corpus-G](https://anonymous.4open.science/r/autocomply/RQs/RQ3/Corpus-G.csv), a dataset of 31 open-source Android Auto apps spanning diverse categories and development practices. 
The objective was to assess whether AutoComply could effectively detect compliance violations across various real-world apps and remain computationally efficient for large-scale analysis.

Apps in Corpus-G are made available in the `/apks` folder [here](https://anonymous.4open.science/r/autocomply/apks/).


**Table: AutoComply's performance on open-source Android Auto applications in *Corpus-G***

|  AutoComply Evaluation Metrics | Corpus-G |
|---|---|
| \# of Apks | 31 |
| \# of Apps w Issues | 15|
| \# of Issues Detected | 27 |
| GeoMean Time(s) | 5.6 |
| LoC  | 6.5m  |


**Table 2: Detailed static analysis results when Android Lint and AutoComply applied on selected Android Auto apps. Stars: Number of GitHub stars; Downloads: Downloads on Google Play; KLOC: Source code size (thousands of lines); Commit: Latest commit hash; TP: True Positives; FP: False Positives; Time: Analysis time in seconds.**

| # | Repository | Stars | Downloads | KLOC | Commit | Android Lint TP | Android Lint FP | Android Lint Time | AutoComply TP | AutoComply FP | AutoComply Time |
|---|------------|-------|-----------|------|--------|-----------------|-----------------|-------------------|---------------|---------------|-----------------|
| 1 | anandnet/Harmony-Music | 1.4K | -- | 35 | ff91d19 | 0 | 0 | 1 | 3 | 0 | 1 |
| 2 | antoinepirlot/Satunes | 38 | -- | 138.8 | 24e3933 | 0 | 0 | 1 | 2 | 0 | 18 |
| 3 | DJDoubleD/refreezer | 433 | 49K | 34.7 | aecf242 | 0 | 0 | 1 | 1 | 0 | 4 |
| 4 | gokadzev/Musify | 2.4K | 467K | 9.5 | f524674 | 0 | 0 | 1 | 3 | 0 | 2 |
| 5 | jellyfin/jellyfin-android | 1.7K | 1M+ | 158.9 | 7886df9 | 0 | 0 | 140 | 2 | 0 | 7 |
| 6 | KRTirtho/spotube | 33.9K | -- | 68.2 | 8c1337d | 0 | 0 | 1 | 3 | 0 | 2 |
| 7 | LISTEN-moe/android-app | 258 | -- | 90.4 | 4194aeb | 0 | 0 | 30 | 2 | 0 | 3 |
| 8 | namidaco/namida | 2.9K | 289K | 92.9 | 675dc79 | 0 | 0 | 1 | 2 | 0 | 3 |
| 9 | nextcloud/news-android | 705 | 5K+ | 223.5 | 9636d61 | 0 | 0 | 18 | 1 | 0 | 5 |
| 10 | nt4f04uNd/sweyer | 209 | -- | 27.5 | e5abe5a | 0 | 0 | 1 | 3 | 0 | 2 |
| 11 | OxygenCobalt/Auxio | 2.3K | -- | 47.9 | fce77ec | 1 | 0 | 198 | 1 | 0 | 6 |
| 12 | quran/quran_android | 2.1K | 50M+ | 58.2 | f5bd3dc | 0 | 0 | 138 | 1 | 0 | 6 |
| 13 | Simple-Music-Player | 1.3K | -- | 215.3 | 498086a | 0 | 0 | 64 | 1 | 0 | 8 |
| 14 | sosauce/CuteMusic | 363 | 4K | 30.4 | 97bb20b | 1 | 0 | 119 | 1 | 0 | 2 |
| 15 | timusus/Shuttle2 | 208 | -- | 295.5 | 6fd520f | 0 | 0 | 315 | 1 | 0 | 21 |
| **Total Issues / Geomean Time (s)** | | | | | | **2** | **0** | **11.1** | **27** | **0** | **4.2** |



## Answer

AutoComply achieves high accuracy in detecting Android Auto compliance issues, correctly identifying 27 issues with no false positives or false negatives. These results demonstrate that AutoComply provides reliable checks on real-world Android Auto apps.



