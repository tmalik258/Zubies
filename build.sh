# Build the project
echo "Building the project ..."
python3.12 -m pip install -r requirements.txt

echo "Make migrations ..."
python3.12 manage.py makemigrations --noinput
python3.12 manage.py migrate --noinput

echo "Collect static ..."
python3.12 manage.py collectstatic --noinput --clear