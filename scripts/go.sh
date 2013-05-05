rm db.sql
python manage.py syncdb --noinput
#python ims.py

python importsl.py 130117sl.csv 130117slall.csv 130117sloud.csv 
#python manage.py createsuperuser --username 'bteeuwen' --email 'bteeuwen@gmail.com'
