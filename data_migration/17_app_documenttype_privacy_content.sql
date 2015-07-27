DO $$
DECLARE content text;
BEGIN
content := 'Privacy Policy for Employees
Our company values each employee, and so has a commitment to protect the personal information which we handle on behalf of the employee.
It is our policy that:
1. Our company will collect only that information about employees which is needed and relevant.
2. Our company will strive to make certain that personal information about employees is kept accurate and up-to-date.
3. Our company will use appropriate controls to ensure that this information is kept secure, and is only viewed or used by the proper personnel.
4. Information about employees will not be disclosed to any external parties unless appropriate.
5. Employees will be told how they can review information about them, make updates, and report problems.
6. Our company will comply with applicable laws, regulations, and industry standards when protecting employee information.
7.  We hold our employees, vendors, contractors, suppliers, and trading partners to meet this same set of policies. ';

IF NOT EXISTS (select 1 from app_documenttype where name = 'Privacy Policy') THEN
    insert into app_documenttype(id, name, default_content) values(6, 'Privacy Policy', content);
ELSE
    update app_documenttype
    set default_content = content
    where name='Privacy Policy';
END IF;

END
$$
;
