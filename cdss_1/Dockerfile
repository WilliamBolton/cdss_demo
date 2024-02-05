FROM python:3.10.13

#FROM continuumio/anaconda3

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

#RUN conda install --name app_env --file requirements.txt

#RUN conda update -n base -c defaults conda \
#    && conda install --name app_env --file requirements.txt

#SHELL ["conda", "run", "-n", "app_env", "/bin/bash", "-c"]
#RUN conda activate --name app_env

COPY . .

EXPOSE 8000

CMD ["conda", "run", "-n", "app_env", "python", "manage.py", "runserver"]





