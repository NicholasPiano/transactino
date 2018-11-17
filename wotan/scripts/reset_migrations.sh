
rm -rf apps/base/migrations/
rm -rf apps/bitcoin/migrations/
rm -rf apps/subscription/migrations/
rm -rf apps/transactino/migrations/

python manage.py makemigrations base
python manage.py makemigrations bitcoin
python manage.py makemigrations subscription
python manage.py makemigrations transactino
