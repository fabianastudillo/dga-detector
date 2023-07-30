FROM python:3.7.11-bullseye
LABEL Fabian Astudillo-Salinas <fabian.astudillos@ucuenca.edu.ec>

EXPOSE 9999

RUN mkdir /var/log/dgam
RUN apt-get update
RUN mkdir /dga
RUN mkdir /dga/models
RUN mkdir /dga/src
RUN mkdir /dga/others
RUN mkdir /dga/results
RUN mkdir /var/log/dga

## DGA
RUN python -m pip install scikit-learn==0.24.1
RUN python -m pip install joblib
RUN python -m pip install pandas
RUN python -m pip install numpy
RUN python -m pip install regex

CMD [ "python", "/dga/src/Detector.py" ]
