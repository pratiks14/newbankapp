
create table netbankusers(
customerid char(7) primary key,
emailid varchar(25) not null,
mobileno char(10) not null,
name varchar(25) not null,
password varchar(25) not null,
login_time datetime2
);

drop table netbankusers;
select * from netbankusers;
select login_time from netbankusers where customerid ='1141621'
