FROM public.ecr.aws/lambda/python:3.12

WORKDIR ${LAMBDA_TASK_ROOT}

COPY ./requirements.txt ./

# Install the specified packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy function code
COPY . .

RUN chmod +x lambda_entrypoint.sh

ENV RUN_MODE=lambda
EXPOSE 8000

# Use our entrypoint script
ENTRYPOINT ["./lambda_entrypoint.sh"]
