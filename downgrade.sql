
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

create index target_time on results (target, time);

commit transaction;

vacuum;

explain query plan select target, time, result from results where time >= 1549172399 and time <= 1549272399 and target = 'http://www.google.com' order by time;

