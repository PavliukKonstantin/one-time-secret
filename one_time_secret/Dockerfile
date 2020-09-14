#################
# BUILDER IMAGE #
#################

FROM python:3.8.5-alpine as builder

# Install dependecies
RUN apk update \
&& pip install -U setuptools pip \
&& apk add postgresql-dev gcc python3-dev musl-dev libffi-dev build-base
COPY requirements.txt /install/requirements.txt
RUN pip install --no-cache-dir --prefix=/install -r /install/requirements.txt


####################
# PRODUCTION IMAGE #
####################

FROM python:3.8.5-alpine

# Set enviroments variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create the app user
RUN addgroup -S app && adduser -S app -G app

# Change workdir
WORKDIR /home/app/one_time_secret

# Install dependecies
COPY --from=builder /install /usr/local
RUN apk --no-cache add libpq

# Copy project
COPY . .

# Chown all files to the app_user
RUN chown -R app:app .

# Run entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
