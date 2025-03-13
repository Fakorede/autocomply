# RQ 2: Common Issues and Causes

> What are the basic types of Android Auto compatibility issues? Are there any common causes?

To investigate the issues in more detail, we focus on
the subset of apps that have explicitly added support for Android
Auto and have [reported issues](https://anonymous.4open.science/r/carcompat-0503/RQs/RQ2/Issues.csv) in their repositories. This refined
dataset is referred to as [Corpus-R](https://anonymous.4open.science/r/carcompat-0503/RQs/RQ2/Corpus-R.csv).

### Breakdown of Android Auto App Issues in Different Categories for *Corpus-R*.

| Issue Category | Number of Issues |
|----------------|------------------|
| Media Playback functionality | 104 (70.7%) |
| User Interface problems | 36 (24.4%) |
| Voice Command problems | 7 (4.8%) |
| Total | 147 |

## Answer

We manually examine each Android Auto issue and classify them based on their manifestation. Following analysis and discussion, all authors reached a consensus on three primary categories: `T1 - Media Playback`, `T2 - User Interface`, and `T3 - Voice Commands`.

A common theme among
these three issues is an oversight by developers when implement-
ing all the necessary requirements defined by the car app quality
guidelines, depending on the app category, when adding support
for Android Auto. The absence of automated testing tools further exacerbates the prevalence of these issues, compounding the chal-
lenges in both the development and deployment phases of Android
Auto-compatible apps
