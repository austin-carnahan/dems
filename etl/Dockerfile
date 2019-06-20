# Pull python 3 image
FROM python:3
# Create a work dir
WORKDIR /usr/src/etl
# copy requirements.txt into workdir created above
COPY requirements.txt ./
# Install all requirements
RUN python3 -m pip install --user --no-cache-dir -r requirements.txt
# Copy entireproject into workdir
COPY . .
# Run our app
CMD ["python", "etl.py"]
