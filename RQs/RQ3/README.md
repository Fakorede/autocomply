# RQ 3: Comparison with Existing Tools

> How does AutoComply compare with existing Android Auto analysis tools in terms of issue coverage and accuracy?

To evaluate AutoComply against existing Android Auto analysis tools, we compare it with Android Lint, which, to the best of our knowledge, is the only tool that includes built-in checks for Android Auto compatibility violations. 

**Table: Performance comparison between AutoComply and Android Lint on the 15 apps in Corpus-G with detected issues**

| Evaluation Metrics  | AutoComply | Android Lint |
|---|---|---|
| \# of Issues Detected  | 27 | 2 |
|  True Positives | 27 | 2 |
|  False Positives | 0 | 0 |
|  GeoMean Time(s) | 4.2 | 11.1 |

Details of the detected issues are available [here](https://anonymous.4open.science/r/autocomply/RQs/RQ2/RQ2%20-%20Detailed%20Issues%20Report/).

[RQ2.csv](https://anonymous.4open.science/r/autocomply/RQs/RQ2/RQ2.csv) contains the table summarizing these issues.

## Answer

AutoComply significantly outperforms Android Lint by detecting 27 issues compared to only 2, while both tools report zero false positives. Additionally, AutoComply runs more than 2X faster, making it a more comprehensive and efficient solution for Android Auto compliance analysis.
