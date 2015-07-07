DO $$
BEGIN

  UPDATE app_sysbenefitupdatereasoncategory
  SET rank = 1
  WHERE name = 'New';

  UPDATE app_sysbenefitupdatereasoncategory
  SET rank = 2
  WHERE name = 'Change';

  UPDATE app_sysbenefitupdatereasoncategory
  SET rank = 3
  WHERE name = 'Termination/Involuntary';

  UPDATE app_sysbenefitupdatereasoncategory
  SET rank = 4
  WHERE name = 'Termination/Voluntary';

  UPDATE app_sysbenefitupdatereasoncategory
  SET rank = 5
  WHERE name = 'Other';

END
$$;
