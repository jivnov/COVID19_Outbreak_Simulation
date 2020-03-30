# COVID-19_Outbreak_Simulation

Computer simulation of COVID-19 outbreak, which is based on the deterministic
differential equation model, complicated version of the SEIR-model,
which is based on the article ["The effectiveness of quarantine and isolation determine the trend of the COVID-19 epidemics
in the final phase of the current outbreak in China"](https://www.ijidonline.com/action/showPdf?pii=S1201-9712%2820%2930137-5) by Biao Tang, Fan Xia, Sanyi Tang, Nicola Luigi Bragazzi, Qian Li,
Xiaodan Sun, Juhua Liang, Yanni Xiao, Jianhong Wu.\
\
This model is calculated for each country separately when it becomes infected. A separate
algorithm simulates border crossings using data from csv-files and identifies
infected countries.\
This simulation has a web interface written with Django framework.

### Prerequisites

Use the package manager pip to install requirements

```
pip install requirements.txt
```

### How to run

```
python manage.py runserver
```

### Preview
WORK IN PROGRESS. PREVIEW IS NOT FINAL VERSION.

![](screenshots/Peek-2020-03-23-17-13.gif)