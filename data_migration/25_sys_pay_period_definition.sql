DO $$
BEGIN

IF NOT EXISTS (select 1 from app_syspayperioddefinition where name = 'Weekly') THEN
    insert into app_syspayperioddefinition (name, month_factor)
    values('Weekly', 0.23076923076923);
END IF;

IF NOT EXISTS (select 1 from app_syspayperioddefinition where name = 'Bi-Weekly') THEN
    insert into app_syspayperioddefinition (name, month_factor)
    values('Bi-Weekly', 0.46153846153846);
END IF;

IF NOT EXISTS (select 1 from app_syspayperioddefinition where name = 'Semi-Monthly') THEN
    insert into app_syspayperioddefinition (name, month_factor)
    values('Semi-Monthly', 0.5);
END IF;

IF NOT EXISTS (select 1 from app_syspayperioddefinition where name = 'Monthly') THEN
    insert into app_syspayperioddefinition (name, month_factor)
    values('Monthly', 1);
END IF;

IF NOT EXISTS (select 1 from app_syspayperioddefinition where name = 'Quarterly') THEN
    insert into app_syspayperioddefinition (name, month_factor)
    values('Quarterly', 3);
END IF;

IF NOT EXISTS (select 1 from app_syspayperioddefinition where name = 'Annually') THEN
    insert into app_syspayperioddefinition (name, month_factor)
    values('Annually', 12);
END IF;

END
$$