# Trainline GDPR

## What's this?
**Short:** generate a CSV file of trips you've booked through Trainline from your data you have requested thanks to the GDPR.

**Long:** I use [Trainline Europe](https://www.trainline.eu) to book my train tickets since it was called Capitaine Train. Thanks to the GDPR law and especially the portability section, you can request your personal data. I wrote a [blog post](https://blog.antoine-augusti.fr/2018/10/visualizing-my-train-journeys-thanks-to-gdpr-and-trainline/) about this.

The Trainline Europe team will gladly send you a JSON file by email. The goal of this repository is to get a single CSV file to analyse your personal trips (trips that you've actually done - not booked, cancelled or those who have expired).

## Installation
```sh
git clone git@github.com:AntoineAugusti/trainline-gdpr.git
cd trainline-gdpr
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage
```
$ python main.py -h
usage: main.py [-h] filepath

positional arguments:
  filepath    The full path to the Trainline JSON file

optional arguments:
  -h, --help  show this help message and exit
```

Therefore, you can call the script like this: `python main.py /tmp/trainline.json`

## Generated CSV
See the file [data_sample.csv](data_sample.csv) to look at a sample file!
