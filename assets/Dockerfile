FROM public.ecr.aws/lambda/python:3.11

# Copy function code
COPY ./ ${LAMBDA_TASK_ROOT}

# Install the function's dependencies using file requirements.txt
# from your project folder.

RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Set WORKDIR to app
WORKDIR /var/task/

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "simplebot.lambda_handler" ] 