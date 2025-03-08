# CarCompat

CarCompat is the static analysis tool we present in our paper "Analyzing and Detecting Compatibility Issues in Android Auto Apps" available [here](https://arxiv.org/abs/2503.04003).

## Requirements

- Java 17
- Python 3

## Setup

```
pip install git+https://github.com/appknox/pyaxmlparser.git
pip install androguard==3.3.5
chmod +x car_feat.py
```

## Compile

```shell
./gradlew build
```

## Run

All open source apks used for the evaluation section of our paper is available [here](apks/) 


```shell
# basic usage
java -jar app/build/libs/carcompat-0.2.0.jar -a /path/to/your/app.apk -c <category>

# to run with more memory for larger apks
java -Xmx10g -jar app/build/libs/carcompat-0.2.0.jar -a /path/to/your/app.apk -c <category>

# example usage
java -jar app/build/libs/carcompat-0.3.0.jar -a apks/retromusicplayer.apk -c media
```

## License
This artifact is licensed under the GPL v3 License. See [LICENSE](LICENSE) for details.
