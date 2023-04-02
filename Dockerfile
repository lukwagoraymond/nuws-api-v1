FROM python:3.10

LABEL maintainer="Raymond Lukwago A.R <lukwagoraraymond3@gmail.com>"

# Set up Container Working Directory
WORKDIR /nuws-api-v1
RUN pip install virtualenv
RUN virtualenv nuws_env
RUN source nuws_env/bin/activate
# Copy all files in the nuws-api-v1 project folder to the container working directory
COPY . .
# Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt


# Tell the port number the container needs to expose
EXPOSE 5000

CMD ["python3", "-m", "api.v1.app"]