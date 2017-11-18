begin transaction;

drop table if exists transactions;

create table transactions (
    type varchar(255),
    amount float,
    description varchar(255),
    temporal timestamp
);

insert into transactions
    select 'Donation',amount,'Donation',temporal from donations;

insert into transactions
    select 'Purchase',amount,description,temporal from purchases;

select * from transactions
    order by temporal asc;

commit;
