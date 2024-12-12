
insert into users (id, username, supervisor_id, hashed_password, is_active, is_superuser, created_time, updated_time)
values (1, 'admin', null, '$2b$12$br.OtyNBCiep7e5R5KzZDeOCBbBKD/W6txScrZH/eT3kxgPK2kIx6', true, false,  now(), now()),
       (2, 'manager', null, '$2b$12$br.OtyNBCiep7e5R5KzZDeOCBbBKD/W6txScrZH/eT3kxgPK2kIx6', true, false,  now(), now()),
       (3, 'user1', null, '$2b$12$br.OtyNBCiep7e5R5KzZDeOCBbBKD/W6txScrZH/eT3kxgPK2kIx6', true, false,  now(), now());

insert into users (id, username, supervisor_id, hashed_password, is_active, is_superuser, created_time, updated_time)
values (4, 'user2', 2, '$2b$12$br.OtyNBCiep7e5R5KzZDeOCBbBKD/W6txScrZH/eT3kxgPK2kIx6', true, false,  now(), now());

insert into roles (id, name, is_active, remark, created_time, updated_time)
values (1, 'ADMIN', true, '', now(), now()),
       (2, 'MANAGER', true, '', now(), now()),
       (3, 'USER', true, '', now(), now());

insert into user_roles (user_id, role_id)
values (1, 1),(1, 3),
       (2, 2),(2,3),
       (3, 3), (4, 3);


insert into records (id, bot_token, chat_id, message, sent_time, sent_response, user_id, created_time, updated_time)
values (1, '', '', '', null, '', 1, now(), now()),
       (2, '', '', '', null, '', 2, now(), now()),
       (3, '', '', '', null, '', 3, now(), now()),
       (4, '', '', '', null, '', 4, now(), now());