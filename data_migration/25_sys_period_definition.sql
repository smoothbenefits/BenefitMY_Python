DO $$
BEGIN

IF NOT EXISTS (select 1 from app_sysperioddefinition where name = 'Weekly') THEN
    insert into app_sysperioddefinition (name, month_factor)
    values('Weekly', 0.23076923076923);
END IF;

IF NOT EXISTS (select 1 from app_sysperioddefinition where name = 'Bi-Weekly') THEN
    insert into app_sysperioddefinition (name, month_factor)
    values('Bi-Weekly', 0.46153846153846);
END IF;

IF NOT EXISTS (select 1 from app_sysperioddefinition where name = 'Semi-Monthly') THEN
    insert into app_sysperioddefinition (name, month_factor)
    values('Semi-Monthly', 0.5);
END IF;

IF NOT EXISTS (select 1 from app_sysperioddefinition where name = 'Monthly') THEN
    insert into app_sysperioddefinition (name, month_factor)
    values('Monthly', 1);
END IF;

IF NOT EXISTS (select 1 from app_sysperioddefinition where name = 'Quarterly') THEN
    insert into app_sysperioddefinition (name, month_factor)
    values('Quarterly', 3);
END IF;

IF NOT EXISTS (select 1 from app_sysperioddefinition where name = 'Annually') THEN
    insert into app_sysperioddefinition (name, month_factor)
    values('Annually', 12);
END IF;

IF NOT EXISTS (select 1 from app_sysperioddefinition where name = 'Per Diem') THEN
    insert into app_sysperioddefinition (name)
    values('Per Diem');
END IF;

IF NOT EXISTS (select 1 from app_sysperioddefinition where name = 'Daily') THEN
    insert into app_sysperioddefinition (name)
    values('Daily');
END IF;

END
$$
