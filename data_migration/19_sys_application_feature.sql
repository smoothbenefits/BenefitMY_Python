DO $$
BEGIN

IF NOT EXISTS (select 1 from app_sysapplicationfeature where feature = 'FSA') THEN
    insert into app_sysapplicationfeature (feature) 
    values('FSA');
END IF;

IF NOT EXISTS (select 1 from app_sysapplicationfeature where feature = 'DD') THEN
    insert into app_sysapplicationfeature (feature) 
    values('DD');
END IF;

IF NOT EXISTS (select 1 from app_sysapplicationfeature where feature = 'MedicalBenefit') THEN
    insert into app_sysapplicationfeature (feature) 
    values('MedicalBenefit');
END IF;

IF NOT EXISTS (select 1 from app_sysapplicationfeature where feature = 'DentalBenefit') THEN
    insert into app_sysapplicationfeature (feature) 
    values('DentalBenefit');
END IF;

IF NOT EXISTS (select 1 from app_sysapplicationfeature where feature = 'VisionBenefit') THEN
    insert into app_sysapplicationfeature (feature) 
    values('VisionBenefit');
END IF;

IF NOT EXISTS (select 1 from app_sysapplicationfeature where feature = 'I9') THEN
    insert into app_sysapplicationfeature (feature) 
    values('I9');
END IF;

IF NOT EXISTS (select 1 from app_sysapplicationfeature where feature = 'Manager') THEN
    insert into app_sysapplicationfeature (feature) 
    values('Manager');
END IF;

IF NOT EXISTS (select 1 from app_sysapplicationfeature where feature = 'Deposit') THEN
    insert into app_sysapplicationfeature (feature) 
    values('Deposit');
END IF;

IF NOT EXISTS (select 1 from app_sysapplicationfeature where feature = 'BasicLife') THEN
    insert into app_sysapplicationfeature (feature) 
    values('BasicLife');
END IF;

IF NOT EXISTS (select 1 from app_sysapplicationfeature where feature = 'OptionalLife') THEN
    insert into app_sysapplicationfeature (feature) 
    values('OptionalLife');
END IF;

IF NOT EXISTS (select 1 from app_sysapplicationfeature where feature = 'STD') THEN
    insert into app_sysapplicationfeature (feature) 
    values('STD');
END IF;

IF NOT EXISTS (select 1 from app_sysapplicationfeature where feature = 'LTD') THEN
    insert into app_sysapplicationfeature (feature) 
    values('LTD');
END IF;

IF NOT EXISTS (select 1 from app_sysapplicationfeature where feature = 'HRA') THEN
    insert into app_sysapplicationfeature (feature) 
    values('HRA');
END IF;

IF NOT EXISTS (select 1 from app_sysapplicationfeature where feature = 'W4') THEN
    insert into app_sysapplicationfeature (feature) 
    values('W4');
END IF;

END
$$