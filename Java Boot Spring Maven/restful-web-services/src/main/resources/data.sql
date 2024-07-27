
insert into user_details (id, birth_date, name)
values (1001, current_date(), 'Ran');


insert into user_details (id, birth_date, name)
values (1002, current_date(), 'Bob');


insert into user_details (id, birth_date, name)
values (1003, current_date(), 'Alice');

insert into posts (id, description, user_id )
values (2001,'I want to learn AWS', 1001);

insert into posts (id, description, user_id )
values (2002,'I want to learn devops', 1002);

insert into posts (id, description, user_id )
values (2003,'I want to learn K8', 1001);