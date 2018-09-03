create table loanaccount(
    number char(16) primary key,
    name varchar(50),
    password varchar(50),
    ssn char(6),
    loantype varchar(20),
    loanamount varchar,
    duedate datetime
);
insert into loanaccount values('6969696969696969','Pratik Shetty','myloan1','454545','Personal','2400000','09/14/2018');
create table insurance(
    number char(16) primary key,
    name varchar(50),
    password varchar(50),
    ssn char(6),
    insurancetype varchar(20),
    premium varchar,
    duedate datetime,
    insurance_amount varchar(50)
);

insert into insurance(number,name,password,ssn,insurancetype,premium,duedate,insurance_amount) values('6666666666666666','Pratik Shetty','pratiks14','454545','Vehicle','500','09-14-2018','100000000');
create table creditcard(
    number char(16) primary key,
    name varchar(50),
    pin char(4) ,
    ssn char(6),
    credit_limit varchar,
    amountdue varchar
);
insert into creditcard(number,name,pin,ssn,credit_limit,amountdue) values('4545454545454545','Pratik Shetty','4545','454545','10000.00','6000.00');
insert into creditcard(number,name,pin,ssn,credit_limit,amountdue) values('4545445454545454','Pratik Shetty','4545','454545','10000.00','6000.00');

delete from creditcard;
delete from sqlite_sequence where name="creditcard";

create table debitcard(
    number char(16) primary key,
    accountno char(16),
    name varchar(50),
    pin char(4),
    ssn char(6),
    balance varchar,
    accounttype varchar(30)
);
insert into debitcard values('9696969696969696','4242424242424242','Pratik Shetty','4545','454545','200000.00','savings');
insert into debitcard values('9696969696964589','4242424256455665','Pratik Shetty','4545','454545','200000.00','current');

create table netbankusers(
    ssn char(6) primary key,
    username varchar(50) ,
    password varchar(50),
    securityquestion varchar(70),
    securityanswer varchar(30),
    email varchar(255),
    mobileno char(10)
);

create table linkedaccount(
    accountno char(16) primary key,
    accounttype varchar(30),
    ssn char(6) references netbankusers(ssn) on delete cascade
    
);

create table transactions
(
    tranxid varchar(50) primary key,
    account1 char(16),
    account1type varchar(30),
    account2 char(16),
    account2type varchar(30),
    amount varchar,
    tranxtype varchar,
    checked varchar(3) default('no'),
    tranx_time datetime,
    tranx_status varchar(20)
);

insert into transactions(tranxid,account1,account1type,account2,account2type,amount,tranxtype,tranx_time,tranx_status) values(
    '1026111b8645d113bcbf936b38e376c5e30f93b','4545454545454545','creditcard','5555555555555555','loanaccount','5000','debit','08:16:2018 13:02:35','Completed'
);
insert into transactions(tranxid,account1,account1type,account2,account2type,amount,tranxtype,tranx_time,tranx_status) values(
    '1026111b8645d113bcbf936b38e375e65e9a13b','4545454545454545','creditcard','5555555555555555','loanaccount','5000','credit','08:10:2018 13:02:35','Completed'
);insert into transactions(tranxid,account1,account1type,account2,account2type,amount,tranxtype,tranx_time,tranx_status) values(
    '1026111b8645d113bcbf936b38e37735a54a53b','4545454545454545','creditcard','5555555555555555','loanaccount','5000','debit','08:19:2018 13:02:35','Pending'
);
