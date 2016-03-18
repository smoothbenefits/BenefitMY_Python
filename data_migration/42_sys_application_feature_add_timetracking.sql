DO $$
BEGIN

IF NOT EXISTS (select 1 from app_sysapplicationfeature where feature = 'WorkTimeSheet') THEN
    insert into app_sysapplicationfeature (feature)
    values('WorkTimeSheet');
END IF;

IF NOT EXISTS (select 1 from app_sysapplicationfeature where feature = 'RangedTimeCard') THEN
    insert into app_sysapplicationfeature (feature)
    values('RangedTimeCard');
END IF;

END
$$
