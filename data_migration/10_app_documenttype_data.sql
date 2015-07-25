DO $$
BEGIN
IF NOT EXISTS (select 1 from app_documenttype where name = 'Offer Letter') THEN
    insert into app_documenttype(name, default_content) values('Offer Letter', 'Hello {{Employee}}: We would like to offer you the {{Position}} for {{Annual_Salary}} per year at {{Company_name}}. We hope you would accept this offer and come onboard. {{HR Person}} {{Date}}');
END IF;
IF NOT EXISTS (select 1 from app_documenttype where name = 'Employment Agreement') THEN
    insert into app_documenttype(name, default_content) values('Employment Agreement', 'Hello {{Employee}}: We are here to formally agree with our employment at {{Company_Name}}. Best Regards. {{HR Person}} {{Date}}');
END IF;
IF NOT EXISTS (select 1 from app_documenttype where name = 'NDA') THEN
    insert into app_documenttype(name, default_content) values('NDA', 'Hello {{Employee}}: This is a Non Disclosure Agreement between {{Company_Name}} and you. Best Regards. {{HR Person}} {{Date}}');
END IF;
IF NOT EXISTS (select 1 from app_documenttype where name = 'COBRA') THEN
    insert into app_documenttype(name, default_content) values('COBRA', 'Hello {{Employee}}: This Letter is to inform you that after your employment with {{Company_Name}} has terminated, you are entitlement to receive benefit by COBRA for 60 days. {{HR Person}} {{Date}}');
END IF;
IF NOT EXISTS (select 1 from app_documenttype where name = 'Employee Handbook') THEN
    insert into app_documenttype(name, default_content) values('Employee Handbook', 'This is where you input your Employee Handbook template');
END IF;
IF NOT EXISTS (select 1 from app_documenttype where name = 'Privacy Policy') THEN
    insert into app_documenttype(name, default_content) values('Privacy Policy', 'This is where you input your Privacy Policy template');
END IF;
IF NOT EXISTS (select 1 from app_documenttype where name = 'Policies') THEN
    insert into app_documenttype(name, default_content) values('Policies', 'This is where you input your Policies');
END IF;
PERFORM setval(pg_get_serial_sequence('app_documenttype', 'id'),
              (select max(id) from app_documenttype));
END
$$
;
