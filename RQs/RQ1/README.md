# RQ 1: Landscape 

> What are the most prevalent types of Android Auto compliance violations, and what platform-specific factors contribute to their occurrence?

We collected all available apps from F-Droid, resulting in a [dataset](https://anonymous.4open.science/r/autocomply/RQs/RQ1/fdroid-apps.csv) of 4,387
Android apps [fdroid-apps](https://anonymous.4open.science/r/autocomply/RQs/RQ1/fdroid-apps.csv).

**Android Auto App Filtering.** To identify apps with Android Auto support, we analyzed each app's `AndroidManifest.xml` file for Android Auto-specific declarations. Apps must declare both automotive metadata and `MediaBrowserService` registration to support Android Auto, as shown in Listing 1.

This filtering identified 37 apps where developers explicitly declared intent to support Android Auto. We refer to this dataset as ***Corpus-F***. These apps represent developers' attempts to implement Android Auto support, making them ideal for studying compliance challenges.

Our analysis identified 98 Android Auto issues across 14 repositories. Table 1 presents the complete taxonomy showing issue types, their root causes, and representative examples. Media playback violations dominate (59 issues, 60.2%), reflecting that most Android Auto apps are media players where playback control is fundamental functionality. UI violations account for 31 issues (31.6%), while voice command violations represent 8 issues (8.2%).

Of the 37 apps in [Corpus-F](https://anonymous.4open.science/r/autocomply/RQs/RQ1/fdroid-apps.csv), we found 98 Android Auto-specific issues in 14 apps that had public issue trackers with relevant reports.



**Table 1: Android Auto Issue Types and Root Causes**

| Type | Root Cause | Issue Example | Issue Description |
|------|-----------|---------------|-------------------|
| **T1: Media Playback** | Incomplete callback implementation | AntennaPod #2380 | After completing a podcast episode, the app displays the episode list instead of showing information about the next podcast being played. |
| | State management errors | Vinyl Music Player #348 | The app crashes when a song is liked using Android Auto. |
| **T2: User Interface** | Missing callbacks | Harmony-Music #111 | No user interface displayed in Android Auto. |
| | Incorrect hierarchy structure | Podcini #57 | The Android Auto UI has been broken for several releases. |
| **T3: Voice Commands** | Missing intent filter | Ultrasonic #827 | App fails to support all required voice commands, such as not switching to the requested audio track when a voice command is issued. |
| | Unimplemented callback | Vinyl Music Player #376 | Required voice commands not supported, such as failing to start the requested track after recognizing the command. |


## Answer

Our study reveals that Android Auto compliance violations fall into three categories corresponding to the platform's core requirements: **media playback control** (60.2\%), **UI content provision** (31.6\%), and **voice command handling** (8.2\%). These violations mostly stem from Android Auto's inverted control model, where the vehicle system, not the app, initiates callbacks to render UI and handle user interactions.