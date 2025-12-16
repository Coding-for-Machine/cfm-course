<!-- my compyuter -->
systemctl
```bash
sudo systemctl [status, stop, restart] servers
```bash
# PostgreSQL status
sudo systemctl status postgresql

# PostgreSQL ishga tushirish
sudo systemctl start postgresql

# PostgreSQL to‘xtatish
sudo systemctl stop postgresql

# PostgreSQL qayta ishga tushirish
sudo systemctl restart postgresql

# PostgreSQL konfiguratsiyasini qayta yuklash
sudo systemctl reload postgresql

# PostgreSQLni avtomatik ishga tushirishga sozlash
sudo systemctl enable postgresql

# Avtomatik ishga tushmasligini o‘chirib qo‘yish
sudo systemctl disable postgresql

# Servis hozir faolmi tekshirish
sudo systemctl is-active postgresql

# Servis avtomatik ishga tushishi tekshirish
sudo systemctl is-enabled postgresql
```


docker-posgrsql

```bash
# Ishlayotgan container’larni ko‘rish
docker ps

# PostgreSQL container ichiga kirish
docker exec -it <container_name> psql -U <username> -d <dbname>

# Misol:
docker exec -it pg_container psql -U myuser -d mydb
```
```bash
# Container ichida
psql -U cfm_course_asadbek -d cfm_course

# Barcha bazalarni ko‘rish
\l

# Jadvallar ro‘yxati
\dt

# Jadval strukturasini ko‘rish
\d table_name

# Chiqish
\q
```

