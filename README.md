# CarCompat

CarCompat is the static analysis tool we introduce in our paper "Analyzing and Detecting Compatibility Issues in Android Auto Apps".


## Artifacts

### Python Scripts
- [github_code_search.py](/github_code_search.py) - Python script we used for searching GitHub repositories for android auto patterns. 
- [github_repo_details.py](/github_repo_details.py) - Python utility we used for extracting detailed metadata from the GitHub repositories we retrieved.
- [car_feat.py](/car_feat.py) - Python binary analysis tool used to perform Android Auto specific feature checks.

### Data Files
- [Corpus-L](/RQs/RQ1/Corpus-L.csv) - dataset of 4,387 apps used in our formative study.
- [Corpus-R](/RQs/RQ2/Corpus-R.csv) - dataset of 44 apps used in our formative study.
- [Corpus-G](/RQs/RQ3/Corpus-G.csv) - dataset of 44 apps used in our evaluation of CarCompat.
- [github_search_results.csv](/github_search_results.csv) - contains the GitHub code search results for Android Auto supported repositories used in our evaluation.
- [github_repo_details.csv](/github_repo_details.csv) - contains dataset of GitHub repository metadata including relevant metrics.

### Application Resources
- [apks](/apks) - directory containing the apks in corpus-g used for compatibility testing and analysis.
- [carcompat-0.3.0.jar](/carcompat-0.3.0.jar) - our jar library tool for android auto compatibility testing, available for download on the releases page.

### Research Output
- [Evaluation Results](/RQs/) - directory containing evaluation results organized by research questions. Includes statistical analysis, test outputs, and performance metrics used to validate project hypotheses.


## Requirements

- Java 17
- Python 3

## Setup

```shell
$ git clone <repo>
$ cd <repo>
$ git clone https://github.com/Sable/android-platforms
$ pip install git+https://github.com/appknox/pyaxmlparser.git
$ pip install androguard==3.3.5
$ chmod +x car_feat.py
```

## Compile

Download our tool on the releases page.

```shell
# or build manually
$ ./gradlew build
```

## Run

All **open source** apks used for the evaluation section of our paper is available [here](apks/).

```shell
# example usage
$ java -jar carcompat-0.3.0.jar -a apks/retromusicplayer.apk
```

## Evaluation Results

The reports for our research are available in the [RQs](/RQs/) folder.
Detailed reports for each apk analysis has been saved and made available [here](RQs/RQ3/) and [here](RQs/RQ4/).

## License
This artifact is licensed under the GPL v3 License. See [LICENSE](LICENSE) for details.
