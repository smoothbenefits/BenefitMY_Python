DO $$
BEGIN

IF NOT EXISTS (select 1 from app_sysbenefitupdatereason where name = 'Other') THEN
    insert into app_sysbenefitupdatereason (name, description) 
    values('Other', 'Reason that is not explicitly listed out by other options');
END IF;

IF NOT EXISTS (select 1 from app_sysbenefitupdatereason where name = 'Annual Enrollment') THEN
    insert into app_sysbenefitupdatereason (name, description) 
    values('Annual Enrollment', 'Annual company wide enrollment');
END IF;

IF NOT EXISTS (select 1 from app_sysbenefitupdatereason where name = 'New Employee') THEN
    insert into app_sysbenefitupdatereason (name, description) 
    values('New Employee', 'Initial enrollment for new employee start');
END IF;

IF NOT EXISTS (select 1 from app_sysbenefitupdatereason where name = 'Life Event') THEN
    insert into app_sysbenefitupdatereason (name, description) 
    values('Life Event', 'Enrollment modification due to life events');
END IF;

END
$$