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

create table accountdetails(
accountno char(16) primary key,
customerid char(7) references netbankusers(customerid) on delete cascade,
acc_balance decimal(40,4),
acc_type varchar(15),
mail_address varchar(100),
branch_name varchar(25) not null,
branch_code varchar(10) ,
created_date datetime2



);
