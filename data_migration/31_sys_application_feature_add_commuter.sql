DO $$
BEGIN

IF NOT EXISTS (select 1 from app_sysapplicationfeature where feature = 'Commuter') THEN
    insert into app_sysapplicationfeature (feature)
    values('Commuter');
END IF;

END
$$
