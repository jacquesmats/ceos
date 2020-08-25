FROM tensorflow/tensorflow:latest

RUN apt-get update

RUN apt-get -y install unzip

RUN apt -y install vim

RUN pip install pandas

RUN pip install influxdb==5.3.0

RUN apt -y install git

RUN mkdir /home/ceos

ADD main.py /home/ceos

ADD get_data.py /home/ceos

ADD write_pred.py /home/ceos

RUN curl -L -o /home/ceos/model.zip "https://drive.google.com/uc?export=download&id=1LYWy97b8MadFJer98RWKh-SDJrO-T1rz"

RUN unzip /home/ceos/model.zip -d /home/ceos

RUN rm /home/ceos/model.zip
