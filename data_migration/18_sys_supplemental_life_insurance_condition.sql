DO $$

IF NOT EXISTS (select 1 from app_syssuppllifeinsurancecondition where name = 'Unknown') THEN
    insert into app_syssuppllifeinsurancecondition (name, description) 
    values('Unknown', 'Default value');
END IF;

END
$$