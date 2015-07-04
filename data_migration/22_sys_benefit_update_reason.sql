DO $$
BEGIN

IF NOT EXISTS (select 1 from app_sysbenefitupdatereasoncategory where name = 'Other') THEN
    insert into app_sysbenefitupdatereasoncategory (name, description)
    values('Other', 'Reason that is not explicitly listed out by other options');
END IF;

IF NOT EXISTS (select 1 from app_sysbenefitupdatereasoncategory where name = 'New') THEN
    insert into app_sysbenefitupdatereasoncategory (name, description)
    values('New', 'New benefit enrollment');
END IF;

IF NOT EXISTS (select 1 from app_sysbenefitupdatereasoncategory where name = 'Change') THEN
    insert into app_sysbenefitupdatereasoncategory (name, description)
    values('Change', 'Change on existing benefit enrollment');
END IF;

IF NOT EXISTS (select 1 from app_sysbenefitupdatereasoncategory where name = 'Termination') THEN
    insert into app_sysbenefitupdatereasoncategory (name, description)
    values('Termination', 'Terminate an existing benefit enrollment');
END IF;

IF NOT EXISTS (select 1 from app_sysbenefitupdatereason where name = 'Other') THEN
    insert into app_sysbenefitupdatereason (name, description, category_id, detail_required)
    values('Other', 'Reason that is not explicitly listed out by other options', 1, True);
END IF;

IF NOT EXISTS (select 1 from app_sysbenefitupdatereason where name = 'Open Enrollment') THEN
    insert into app_sysbenefitupdatereason (name, description, category_id, detail_required)
    values('Open Enrollment', 'Annual company wide enrollment', 2, False);
END IF;

IF NOT EXISTS (select 1 from app_sysbenefitupdatereason where name = 'New Hire') THEN
    insert into app_sysbenefitupdatereason (name, description, category_id, detail_required)
    values('New Hire', 'Initial enrollment for new employee start', 2, False);
END IF;

IF NOT EXISTS (select 1 from app_sysbenefitupdatereason where name = 'Add Spouse') THEN
    insert into app_sysbenefitupdatereason (name, description, category_id, detail_required)
    values('Add Spouse', 'Add spouse to an existing benefit plan', 3, False);
END IF;

IF NOT EXISTS (select 1 from app_sysbenefitupdatereason where name = 'Add Dependent (Please specify dependent)') THEN
    insert into app_sysbenefitupdatereason (name, description, category_id, detail_required)
    values('Add Dependent (Please specify dependent)', 'Add dependent to an existing benefit plan', 3, True);
END IF;

IF NOT EXISTS (select 1 from app_sysbenefitupdatereason where name = 'Part-Time to Full-Time (Please specify date)') THEN
    insert into app_sysbenefitupdatereason (name, description, category_id, detail_required)
    values('Part-Time to Full-Time (Please specify date)', 'Update employment type from part-time to full-time', 3, True);
END IF;

IF NOT EXISTS (select 1 from app_sysbenefitupdatereason where name = 'Loss of Coverage') THEN
    insert into app_sysbenefitupdatereason (name, description, category_id, detail_required)
    values('Loss of Coverage', 'Lost of coverage on a certain benefit type', 4, False);
END IF;

IF NOT EXISTS (select 1 from app_sysbenefitupdatereason where name = 'Left Employment') THEN
    insert into app_sysbenefitupdatereason (name, description, category_id, detail_required)
    values('Left Employment', 'No longer employed in the position to receive benefits', 4, False);
END IF;

IF NOT EXISTS (select 1 from app_sysbenefitupdatereason where name = 'Voluntary Cancellation') THEN
    insert into app_sysbenefitupdatereason (name, description, category_id, detail_required)
    values('Voluntary Cancellation', 'Voluntary cancellation on benefit enrollment', 4, False);
END IF;

IF NOT EXISTS (select 1 from app_sysbenefitupdatereason where name = 'Move from Service Area') THEN
    insert into app_sysbenefitupdatereason (name, description, category_id, detail_required)
    values('Move from Service Area', 'Move out of benefit service area', 4, False);
END IF;

IF NOT EXISTS (select 1 from app_sysbenefitupdatereason where name = 'No Longer Eligible') THEN
    insert into app_sysbenefitupdatereason (name, description, category_id, detail_required)
    values('No Longer Eligible', 'Person enrolled has deceased', 4, False);
END IF;

IF NOT EXISTS (select 1 from app_sysbenefitupdatereason where name = 'Deceased') THEN
    insert into app_sysbenefitupdatereason (name, description, category_id, detail_required)
    values('Deceased', 'Initial enrollment into COBRA policy', 4, False);
END IF;

IF NOT EXISTS (select 1 from app_sysbenefitupdatereason where name = 'Terminate Dependent (Please specify dependent)') THEN
    insert into app_sysbenefitupdatereason (name, description, category_id, detail_required)
    values('Terminate Dependent (Please specify dependent)', 'Terminate dependent who is cover under an existing benefit plan', 4, True);
END IF;

END
$$;
