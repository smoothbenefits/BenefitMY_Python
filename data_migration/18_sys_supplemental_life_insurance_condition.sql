DO $$
BEGIN

IF NOT EXISTS (select 1 from app_syssuppllifeinsurancecondition where name = 'Unknown') THEN
    insert into app_syssuppllifeinsurancecondition (name, description) 
    values('Unknown', 'Default value');
END IF;

IF NOT EXISTS (select 1 from app_syssuppllifeinsurancecondition where name = 'Tobacco') THEN
    insert into app_syssuppllifeinsurancecondition (name, description) 
    values('Tobacco', 'If the applicant is a smoker within the last 6 months');
END IF;

IF NOT EXISTS (select 1 from app_syssuppllifeinsurancecondition where name = 'Non-Tobacco') THEN
    insert into app_syssuppllifeinsurancecondition (name, description) 
    values('Non-Tobacco', 'If the applicant has not consume tobacco product within the last 6 months');
END IF;

IF NOT EXISTS (select 1 from app_syssuppllifeinsurancecondition where name = 'Other') THEN
    insert into app_syssuppllifeinsurancecondition (name, description) 
    values('Other', 'Any other conditions');
END IF;

END
$$