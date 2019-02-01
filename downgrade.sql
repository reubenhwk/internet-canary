
begin transaction;

CREATE TABLE results2 (
    id integer primary key autoincrement not null,
    type text,
    target text,
    time real,
    result real);

insert into results2 (type, target, time, result)
    select type, targets.target, time, result from results inner join targets where targets.id = results.target_id
    order by time;

drop table targets;
drop table results;
alter table results2 rename to results;

commit transaction;

vacuum;

