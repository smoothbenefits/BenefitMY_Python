DO $$
BEGIN

IF NOT EXISTS (select 1 from app_sysapplicationfeature where feature = 'ExtraBenefit') THEN
    insert into app_sysapplicationfeature (feature)
    values('ExtraBenefit');
END IF;

END
$$
