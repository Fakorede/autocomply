# CarCompat

CarCompat is the static analysis tool we introduce in our paper "Analyzing and Detecting Compatibility Issues in Android Auto Apps".


## Artifacts

### Python Scripts
- [fdroid_crawler.py](https://anonymous.4open.science/r/carcompat-0503/fdroid_crawler.py) - Python script we used for collecting Free and Open Source Software android APKs from [f-droid](https://f-droid.org/en/). Running this script required downloading the Selenium ChromeDriver.
- [helpers.py](https://anonymous.4open.science/r/carcompat-0503/fdroid_crawler.py) - Utility script for functions we used in the `fdroid_crawler.py` script.
- [github_code_search.py](https://anonymous.4open.science/r/carcompat-0503/github_code_search.py) - Python script we used for searching GitHub repositories for android auto patterns. 
- [github_repo_details.py](https://anonymous.4open.science/r/carcompat-0503/github_repo_details.py) - Python script we used for extracting detailed metadata from the GitHub repositories we retrieved.
- [car_feat.py](https://anonymous.4open.science/r/carcompat-0503/car_feat.py) - Python binary analysis tool used to perform Android Auto specific feature checks.

### Data Files
- [Corpus-L](https://anonymous.4open.science/r/carcompat-0503/RQs/RQ1/Corpus-L.csv) - dataset of 4,387 apps used in our formative study.
- [Corpus-R](https://anonymous.4open.science/r/carcompat-0503/RQs/RQ2/Corpus-R.csv) - dataset of 44 apps used in our formative study.
- [Corpus-G](https://anonymous.4open.science/r/carcompat-0503/RQs/RQ3/Corpus-G.csv) - dataset of 44 apps used in our evaluation of CarCompat.

### Application Resources
- [apks](https://anonymous.4open.science/r/carcompat-0503/apks) - directory containing the apks in corpus-g used for compatibility testing and analysis.
- [carcompat-0.3.0.jar](https://anonymous.4open.science/r/carcompat-0503/carcompat-0.3.0.jar) - our jar library tool for android auto compatibility testing, available for download on the releases page.

### Research Output
- [RQs](https://anonymous.4open.science/r/carcompat-0503/RQs/) - directory containing evaluation results organized by research questions. Includes statistical analysis, test outputs, and performance metrics used to validate project hypotheses.


## Requirements

- Java 17
- Python 3

## Setup

```shell
$ git clone <repo>
$ cd <repo>
$ git clone https://github.com/Sable/android-platforms
$ chmod +x setup.sh
$ ./setup.sh # Install dependencies
```

## Compile

Download our tool on the releases page or [here](https://anonymous.4open.science/r/carcompat-0503/carcompat-0.3.0.jar).

```shell
# or build manually
$ ./gradlew build
```

## Run

All **open source** apks used for the evaluation section of our paper is available [here](https://anonymous.4open.science/r/carcompat-0503/apks/).

```shell
# example usage
$ java -jar carcompat-0.3.0.jar -a apks/retromusicplayer.apk
```

## Evaluation Results

The reports for our research are available in the [RQs](https://anonymous.4open.science/r/carcompat-0503/RQs/) folder.
Detailed reports for each apk analysis has been saved and made available [here](https://anonymous.4open.science/r/carcompat-0503/RQs/RQ3/) and [here](https://anonymous.4open.science/r/carcompat-0503/RQs/RQ4/).

## License
This artifact is licensed under the GPL v3 License. See [LICENSE](https://anonymous.4open.science/r/carcompat-0503/LICENSE) for details.
