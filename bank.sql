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
acc_balance decimal(20,2) default(10000.0),
acc_type varchar(15),
mail_address varchar(250),
branch_name varchar(25) not null,
branch_code varchar(10) ,
created_date datetime2 ,
debitcardno char(16),
aadhar_no char(12),
status varchar(20) default('Applied')
);

drop table accountdetails;
select * from accountdetails;
delete from accountdetails;

create table depositdetails(
depositno char(10) primary key,
customerid char(7) references netbankusers(customerid),
deposit_amount decimal(20,2),
debit_acc char(16) references accountdetails(accountno) on delete cascade,
recur_months  char(2),
day_of_month char(2),
created_on datetime2
);
drop table depositdetails;
delete from depositdetails;
select * from depositdetails;


update accountdetails set acc_balance =acc_balance - 100.0 where accountno = '7318838545954363'
update accountdetails set acc_balance =acc_balance - 5000.00 where accountno = '7318838545954363'
