-- Use following commands to create new users and accounts

-- insert into auth_user (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) values ('', '2015-01-10', 'f', 'broker@labcentral.org', 'Krista', 'Licata', 'broker@labcentral.org', 'f', 't', '2015-01-10');
-- insert into auth_user (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) values ('', '2015-01-10', 'f', 'employer@labcentral.org', 'Krista', 'Licata', 'employer@labcentral.org', 'f', 't', '2015-01-10');
-- insert into auth_user (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) values ('', '2015-01-10', 'f', 'ajohnson@labcentral.org', 'Abby', 'Johnson', 'ajohnson@labcentral.org', 'f', 't', '2015-01-10');
-- insert into auth_user (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) values ('', '2015-01-10', 'f', 'apatterson@labcentral.org', 'Ashley', 'Patterson', 'apatterson@labcentral.org', 'f', 't', '2015-01-10');
-- insert into auth_user (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) values ('', '2015-01-10', 'f', 'cchang@labcentral.org', 'Celina', 'Chang', 'cchang@labcentral.org', 'f', 't', '2015-01-10');
-- insert into auth_user (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) values ('', '2015-01-10', 'f', 'csteele@labcentral.org', 'Clancy', 'Steele', 'csteele@labcentral.org', 'f', 't', '2015-01-10');
-- insert into auth_user (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) values ('', '2015-01-10', 'f', 'jfruehauf@labcentral.org', 'Johannes', 'Fruehauf', 'jfruehauf@labcentral.org', 'f', 't', '2015-01-10');
-- insert into auth_user (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) values ('', '2015-01-10', 'f', 'klicata@labcentral.org', 'Krista', 'Licata', 'klicata@labcentral.org', 'f', 't', '2015-01-10');
-- insert into auth_user (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) values ('', '2015-01-10', 'f', 'motoole@labcentral.org', 'Margaret', 'O''Toole', 'motoole@labcentral.org', 'f', 't', '2015-01-10');
-- insert into auth_user (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) values ('', '2015-01-10', 'f', 'mkeegan@labcentral.org', 'Megan', 'Keegan', 'mkeegan@labcentral.org', 'f', 't', '2015-01-10');
-- insert into auth_user (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) values ('', '2015-01-10', 'f', 'ptucker@labcentral.org', 'Patrick', 'Tucker', 'ptucker@labcentral.org', 'f', 't', '2015-01-10');
-- insert into auth_user (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) values ('', '2015-01-10', 'f', 'pparker@labcentral.org', 'Peter', 'Parker', 'pparker@labcentral.org', 'f', 't', '2015-01-10');
-- insert into auth_user (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) values ('', '2015-01-10', 'f', 'sredd@labcentral.org', 'Sandy', 'Redd', 'sredd@labcentral.org', 'f', 't', '2015-01-10');
-- insert into auth_user (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) values ('', '2015-01-10', 'f', 'kficarra@mfhf.com', 'Kathy', 'Ficarra', 'kficarra@mfhf.com', 'f', 't', '2015-01-10');
-- insert into auth_user (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) values ('', '2015-01-10', 'f', 'kficarra@baystatebenefits.com', 'Kathy', 'Ficarra', 'kficarra@baystatebenefits.com', 'f', 't', '2015-01-10');

-- insert into app_company (name) values ('BenefitMy Inc.'), ('Startup.Com');

-- insert into app_companyuser (company_user_type, company_id, user_id, new_employee) select 'admin', 1, u.id, 't' from auth_user u where u.id = 2;
-- insert into app_companyuser (company_user_type, company_id, user_id, new_employee) select 'broker', 1, u.id, 't' from auth_user u where u.id = 1;
-- insert into app_companyuser (company_user_type, company_id, user_id, new_employee) select 'employee', 9, u.id, 't' from auth_user u where u.id = 124;

-- update app_companyuser set company_user_type = 'broker' where user_id = 121;
-- update app_companyuser set company_user_type = 'admin' where user_id = 120;

-- SELECT setval('auth_user_id_seq', (SELECT MAX(id) from "auth_user"));

-- insert into app_benefittype (name) values ('Medical'), ('Dental'), ('Vision');

-- insert into app_documenttype (name) values ('Offer Letter'), ('Employment Agreement'), ('NDA'), ('COBRA');

-- from emailusernames.utils import migrate_usernames
-- migrate_usernames()

-- from app.models.user import User
-- for i in range(2):
--     key = 1 + i
--     user = User.objects.get(pk=key)
--     user.set_password('foobar')
--     user.save()

-- from app.models.user import User
-- for i in range(2):
--     key = 120 + i
--     user = User.objects.get(pk=key)
--     user.set_password('BSSKathy2015')
--     user.save()
