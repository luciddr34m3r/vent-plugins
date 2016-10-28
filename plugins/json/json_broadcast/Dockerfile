FROM python:3-alpine
MAINTAINER Curt Barnard <luciddr34m3r@gmail.com>

ADD requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
ADD json_broadcast.py json_broadcast.py

ENTRYPOINT ["python3", "json_broadcast.py"]
CMD [""]
