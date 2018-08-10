create table loanaccount(
    number char(16) primary key,
    name varchar(50),
    password varchar(50),
    ssn char(6),
    loantype varchar(20),
    loanamount integer
)

create table insurance(
    number char(16) primary key,
    name varchar(50),
    password varchar(50),
    ssn char(6),
    insurancetype varchar(20),
    premium integer,
    duedate datetime 
);

insert into insurance values('6666666666666666','Pratik Shetty','pratiks14','454545','Vehicle Insurance','1000000','14-09-2018');
create table creditcard(
    number char(16) primary key,
    name varchar(50),
    pin char(4) ,
    ssn char(6),
    credit_limit DECIMAL(10,2),
    amountdue currency
);
insert into creditcard values('4545454545454545','Pratik Shetty','4545','454545',10000.00,6000.00);
insert into creditcard values('4545445454545454','Pratik Shetty','4545','454545',10000.00,6000.00);


create table debitcard(
    number char(16) primary key,
    accountno char(16),
    name varchar(50),
    pin char(4),
    ssn char(6),
    balance decimal(29,2),
    accounttype varchar(30)
);

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

