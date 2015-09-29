DO $$
BEGIN

IF NOT EXISTS (select 1 from app_sysapplicationfeature where feature = 'BenefitsForFullTimeOnly') THEN
    insert into app_sysapplicationfeature (feature)
    values('BenefitsForFullTimeOnly');
END IF;

END
$$