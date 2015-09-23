DO $$
BEGIN

IF NOT EXISTS (select 1 from app_sysapplicationfeature where feature = 'ADAD') THEN
    insert into app_sysapplicationfeature (feature)
    values('ADAD');
END IF;

END
$$
