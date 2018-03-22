FROM ubuntu:16.04
LABEL Name=server_booking_system Version=0.0.1
RUN apt-get -y update && apt-get install -y python3 
RUN apt-get install -y mongodb
RUN apt-get install -y python3-pip 
RUN alias python=python3 && pip3 install --upgrade pip 
RUN pip3 install flask
ADD ./entrypoint.sh entrypoint.sh 
RUN chmod +x /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]