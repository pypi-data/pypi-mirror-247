# AbusifyID

Abusiveness Verification in Bahasa Indonesia. Predict the abusiveness level of a sentence, detect abusive words, and filter abusive words.

Live Demo: https://abusifyid.streamlit.app/

## Requirements

All requirements below have been installed automatically. Install manually if there are problems:

* [Python 2.6 or higher]
* [scikit-learn](https://pypi.org/project/scikit-learn/)
* [pandas](https://pypi.org/project/pandas/)
* [nltk](https://pypi.org/project/nltk/)
* [pymysql](https://pypi.org/project/pymysql/)
* [python-decouple](https://pypi.org/project/python-decouple/)
* [fuzzywuzzy](https://pypi.org/project/fuzzywuzzy/)
* [python-Levenshtein](https://pypi.org/project/python-Levenshtein/)

## Installation

Install using `pip`.

```
pip install abusify-id
```

## How to Use

### Predict Abusiveness

Predict the abusiveness level of a sentence, using text input or `.txt` file input.

```
import abusify_id as ai
text = "Anjing, lu tolol ya!"
level = ai.predict_abusiveness(text)
print(level)
... 99.59%
```

```
import abusify_id as ai
ai.predict_abusiveness_file("input.txt", "output.txt")
... The results have been saved in a file: output.txt
```

with `decimal_places`:

```
import abusify_id as ai
text = "Anjing, lu tolol ya!"
level = ai.predict_abusiveness(text, decimal_places=5)
print(level)
... 99.59093%
```

```
import abusify_id as ai
ai.predict_abusiveness_file("input.txt", "output.txt", decimal_places=4)
... The results have been saved in a file: output.txt
```

### Abusive Word Detector

```
import abusify_id as ai
text = "Anjing, lu tolol ya!"
detect = ai.abusiveword_detector(text)
print(detect)
... [Anjing](https://stopucapkasar.com/detail.php?id=9), [Tolol](https://stopucapkasar.com/detail.php?id=95)
```

### Abusive Word Filter

```
import abusify_id as ai
text = "Anjing, lu tolol ya!"
filter = ai.abusiveword_filter(text)
print(filter)
... Sialan, lu bebal ya!
```

## Website

Visit our website: https://stopucapkasar.com/