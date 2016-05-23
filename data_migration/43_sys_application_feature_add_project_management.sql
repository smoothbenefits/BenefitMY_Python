DO $$
BEGIN

IF NOT EXISTS (select 1 from app_sysapplicationfeature where feature = 'ProjectManagement') THEN
    insert into app_sysapplicationfeature (feature)
    values('ProjectManagement');
END IF;

END
$$
