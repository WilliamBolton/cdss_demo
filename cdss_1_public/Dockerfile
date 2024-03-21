FROM continuumio/miniconda3

WORKDIR /cdss_1

# Create the environment:
COPY ./ ./
RUN conda env create -f environment.yml

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "cdss", "/bin/bash", "-c"]

# Demonstrate the environment is activated:
RUN echo "Make sure flask is installed:"

EXPOSE 8000

# Run the server
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "cdss", "python", "runserver_plus_resetdb.py"]

# Created docker image called cdss-django-app: 'docbuild -t cdss-django-app .'
# Run with 'docker run -p 8000:8000 cdss-django-app'
# View at 'http://172.17.0.2:8000'

# Pushed to private repo with:
# docker login
# docker tag cdss-django-app willbolton/wb_private_repo:cdss-django-app
# docker push willbolton/wb_private_repo:cdss-django-app