DO $$
BEGIN

IF NOT EXISTS (select 1 from app_sysbenefitupdatereasoncategory where name = 'Other') THEN
    insert into app_sysbenefitupdatereasoncategory (name, description, rank)
    values('Other', 'Reason that is not explicitly listed out by other options', 5);
END IF;

IF NOT EXISTS (select 1 from app_sysbenefitupdatereasoncategory where name = 'New') THEN
    insert into app_sysbenefitupdatereasoncategory (name, description, rank)
    values('New', 'New benefit enrollment', 1);
END IF;

IF NOT EXISTS (select 1 from app_sysbenefitupdatereasoncategory where name = 'Change') THEN
    insert into app_sysbenefitupdatereasoncategory (name, description, rank)
    values('Change', 'Change on existing benefit enrollment', 2);
END IF;

IF NOT EXISTS (select 1 from app_sysbenefitupdatereasoncategory where name = 'Termination/Involuntary') THEN
    insert into app_sysbenefitupdatereasoncategory (name, description, rank)
    values('Termination/Involuntary', 'Terminate an existing benefit enrollment', 3);
END IF;

IF NOT EXISTS (select 1 from app_sysbenefitupdatereasoncategory where name = 'Termination/Voluntary') THEN
    insert into app_sysbenefitupdatereasoncategory (name, description, rank)
    values('Termination/Voluntary', 'Terminate an existing benefit enrollment', 4);
END IF;

IF NOT EXISTS (select 1 from app_sysbenefitupdatereason where name = 'Other') THEN
    insert into app_sysbenefitupdatereason (name, description, category_id, detail_required)
    values('Other', 'Reason that is not explicitly listed out by other options', 1, True);
END IF;

IF NOT EXISTS (select 1 from app_sysbenefitupdatereason where name = 'Open enrollment') THEN
    insert into app_sysbenefitupdatereason (name, description, category_id, detail_required)
    values('Open enrollment', 'Annual company wide enrollment', 2, False);
END IF;

IF NOT EXISTS (select 1 from app_sysbenefitupdatereason where name = 'New hire') THEN
    insert into app_sysbenefitupdatereason (name, description, category_id, detail_required)
    values('New hire', 'Initial enrollment for new employee start', 2, False);
END IF;

IF NOT EXISTS (select 1 from app_sysbenefitupdatereason where name = 'COBRA') THEN
    insert into app_sysbenefitupdatereason (name, description, category_id, detail_required)
    values('COBRA', 'Initial enrollment into COBRA policy', 2, False);
END IF;

IF NOT EXISTS (select 1 from app_sysbenefitupdatereason where name = 'Part-Time to Full-Time (Please specify date)') THEN
    insert into app_sysbenefitupdatereason (name, description, category_id, detail_required)
    values('Part-Time to Full-Time (Please specify date)', 'Update employment type from part-time to full-time', 2, True);
END IF;

IF NOT EXISTS (select 1 from app_sysbenefitupdatereason where name = 'Add spouse') THEN
    insert into app_sysbenefitupdatereason (name, description, category_id, detail_required)
    values('Add spouse', 'Add spouse to an existing benefit plan', 3, False);
END IF;

IF NOT EXISTS (select 1 from app_sysbenefitupdatereason where name = 'Add dependent (Please specify dependent)') THEN
    insert into app_sysbenefitupdatereason (name, description, category_id, detail_required)
    values('Add dependent (Please specify dependent)', 'Add dependent to an existing benefit plan', 3, True);
END IF;

IF NOT EXISTS (select 1 from app_sysbenefitupdatereason where name = 'Marriage') THEN
    insert into app_sysbenefitupdatereason (name, description, category_id, detail_required)
    values('Marriage', 'Marriage', 3, False);
END IF;

IF NOT EXISTS (select 1 from app_sysbenefitupdatereason where name = 'Newborn') THEN
    insert into app_sysbenefitupdatereason (name, description, category_id, detail_required)
    values('Newborn', 'Newborn', 3, False);
END IF;

IF NOT EXISTS (select 1 from app_sysbenefitupdatereason where name = 'Left employment') THEN
    insert into app_sysbenefitupdatereason (name, description, category_id, detail_required)
    values('Left employment', 'No longer employed in the position to receive benefits', 4, False);
END IF;

IF NOT EXISTS (select 1 from app_sysbenefitupdatereason where name = 'Reduction in work hours') THEN
    insert into app_sysbenefitupdatereason (name, description, category_id, detail_required)
    values('Reduction in work hours', 'Reduction in work hours', 4, False);
END IF;

IF NOT EXISTS (select 1 from app_sysbenefitupdatereason where name = 'Move out of service area') THEN
    insert into app_sysbenefitupdatereason (name, description, category_id, detail_required)
    values('Move out of service area', 'Move out of benefit service area', 4, False);
END IF;

IF NOT EXISTS (select 1 from app_sysbenefitupdatereason where name = 'Subscriber/Member age over 65') THEN
    insert into app_sysbenefitupdatereason (name, description, category_id, detail_required)
    values('Subscriber/Member age over 65', 'Subscriber/Member age over 65', 4, False);
END IF;

IF NOT EXISTS (select 1 from app_sysbenefitupdatereason where name = 'Child over age not a student') THEN
    insert into app_sysbenefitupdatereason (name, description, category_id, detail_required)
    values('Child over age not a student', 'Child over age not a student', 4, False);
END IF;

IF NOT EXISTS (select 1 from app_sysbenefitupdatereason where name = 'Student over student age limit') THEN
    insert into app_sysbenefitupdatereason (name, description, category_id, detail_required)
    values('Student over student age limit', 'Student over student age limit', 4, False);
END IF;

IF NOT EXISTS (select 1 from app_sysbenefitupdatereason where name = 'Laid off more than 39 weeks') THEN
    insert into app_sysbenefitupdatereason (name, description, category_id, detail_required)
    values('Laid off more than 39 weeks', 'Laid off more than 39 weeks', 4, False);
END IF;

IF NOT EXISTS (select 1 from app_sysbenefitupdatereason where name = 'Divorce') THEN
    insert into app_sysbenefitupdatereason (name, description, category_id, detail_required)
    values('Divorce', 'Divorce', 4, False);
END IF;

IF NOT EXISTS (select 1 from app_sysbenefitupdatereason where name = 'Dependent child married') THEN
    insert into app_sysbenefitupdatereason (name, description, category_id, detail_required)
    values('Dependent child married', 'Dependent child married', 4, False);
END IF;

IF NOT EXISTS (select 1 from app_sysbenefitupdatereason where name = 'Student graduated') THEN
    insert into app_sysbenefitupdatereason (name, description, category_id, detail_required)
    values('Student graduated', 'Student graduated', 4, False);
END IF;

IF NOT EXISTS (select 1 from app_sysbenefitupdatereason where name = 'Cobra eligibility has expired') THEN
    insert into app_sysbenefitupdatereason (name, description, category_id, detail_required)
    values('Cobra eligibility has expired', 'Cobra eligibility has expired', 4, False);
END IF;

IF NOT EXISTS (select 1 from app_sysbenefitupdatereason where name = 'Continuation of Coverage (COC) has expired') THEN
    insert into app_sysbenefitupdatereason (name, description, category_id, detail_required)
    values('Continuation of Coverage (COC) has expired', 'Continuation of Coverage (COC) has expired', 4, False);
END IF;

IF NOT EXISTS (select 1 from app_sysbenefitupdatereason where name = 'Deceased') THEN
    insert into app_sysbenefitupdatereason (name, description, category_id, detail_required)
    values('Deceased', 'Initial enrollment into COBRA policy', 4, False);
END IF;

IF NOT EXISTS (select 1 from app_sysbenefitupdatereason where name = 'Terminate dependent (Please specify dependent)') THEN
    insert into app_sysbenefitupdatereason (name, description, category_id, detail_required)
    values('Terminate dependent (Please specify dependent)', 'Terminate dependent who is cover under an existing benefit plan', 4, True);
END IF;

IF NOT EXISTS (select 1 from app_sysbenefitupdatereason where name = 'Military service') THEN
    insert into app_sysbenefitupdatereason (name, description, category_id, detail_required)
    values('Military service', 'Military service', 5, False);
END IF;

IF NOT EXISTS (select 1 from app_sysbenefitupdatereason where name = 'Dissatisfied with plan') THEN
    insert into app_sysbenefitupdatereason (name, description, category_id, detail_required)
    values('Dissatisfied with plan', 'Dissatisfied with plan', 5, False);
END IF;

IF NOT EXISTS (select 1 from app_sysbenefitupdatereason where name = 'Transferred to an HMO') THEN
    insert into app_sysbenefitupdatereason (name, description, category_id, detail_required)
    values('Transferred to an HMO', 'Transferred to an HMO', 5, False);
END IF;

IF NOT EXISTS (select 1 from app_sysbenefitupdatereason where name = 'Transferred to other insurer') THEN
    insert into app_sysbenefitupdatereason (name, description, category_id, detail_required)
    values('Transferred to other insurer', 'Transferred to other insurer', 5, False);
END IF;

IF NOT EXISTS (select 1 from app_sysbenefitupdatereason where name = 'Covered under another policy') THEN
    insert into app_sysbenefitupdatereason (name, description, category_id, detail_required)
    values('Covered under another policy', 'Covered under another policy', 5, False);
END IF;

IF NOT EXISTS (select 1 from app_sysbenefitupdatereason where name = 'COBRA cancellation') THEN
    insert into app_sysbenefitupdatereason (name, description, category_id, detail_required)
    values('COBRA cancellation', 'COBRA cancellation', 5, False);
END IF;

END
$$;
