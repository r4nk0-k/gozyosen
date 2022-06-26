FROM python:3.9
USER root
WORKDIR /app

COPY . /app
CMD ["/bin/bash"]